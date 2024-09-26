import json
import os
import sqlite3
from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import BaseModel

from morph.constants import MorphConstant


class RunStatus(str, Enum):
    DONE = "done"
    TIMEOUT = "timeout"
    IN_PROGRESS = "inProgress"
    FAILED = "failed"


class StackTraceFrame(BaseModel):
    filename: str
    lineno: Optional[int] = None
    name: str
    line: Optional[str] = None


class PythonError(BaseModel):
    type: str
    message: str
    code: str
    stacktrace: str
    structured_stacktrace: List[StackTraceFrame]


GeneralError = str


class CliError(BaseModel):
    type: Literal["python", "general"]
    details: Union[PythonError, GeneralError]


class SqliteDBManager:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.db_path = os.path.join(self.project_root, MorphConstant.MORPH_PROJECT_DB)

    def initialize_database(self):
        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create "runs" table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT,
                canvas TEXT,
                cell_alias TEXT,
                is_dag BOOLEAN,
                status TEXT,
                error TEXT,
                started_at TEXT,
                ended_at TEXT,
                log TEXT,
                outputs TEXT,
                PRIMARY KEY (run_id, canvas, cell_alias)
            )
            """
        )

        # Create indexes for "runs" table
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_runs_cell_alias ON runs(cell_alias)
            """
        )

        # Commit changes and close the connection
        conn.commit()
        conn.close()

    def insert_run_record(
        self, run_id: str, canvas: str, cell_alias: str, is_dag: bool, log_path: str
    ) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("BEGIN TRANSACTION")
            cursor.execute(
                """
                INSERT INTO runs (run_id, canvas, cell_alias, is_dag, status, started_at, ended_at, log, outputs)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    canvas,
                    cell_alias,
                    is_dag,
                    RunStatus.IN_PROGRESS.value,
                    datetime.now().isoformat(),
                    None,
                    log_path,
                    None,
                ),
            )
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def update_run_record(
        self,
        run_id: str,
        canvas: Optional[str],
        cell_alias: str,
        new_status: str,
        error: Optional[CliError],
        outputs: Optional[Union[str, dict, List[str]]] = None,
    ) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        ended_at = datetime.now().isoformat()

        # Ensure error and outputs are JSON serializable strings
        error_str: Optional[str] = None
        if error:
            error_str = error.model_dump_json()
        if outputs and not isinstance(outputs, str):
            outputs = json.dumps(outputs)

        try:
            cursor.execute("BEGIN TRANSACTION")
            if canvas is None:
                cursor.execute(
                    """
                    UPDATE runs
                    SET status = ?, error = ?, ended_at = ?, outputs = ?
                    WHERE run_id = ? AND cell_alias = ?
                    """,
                    (new_status, error_str, ended_at, outputs, run_id, cell_alias),
                )
            else:
                cursor.execute(
                    """
                    UPDATE runs
                    SET status = ?, error = ?, ended_at = ?, outputs = ?
                    WHERE run_id = ? AND canvas = ? AND cell_alias = ?
                    """,
                    (
                        new_status,
                        error_str,
                        ended_at,
                        outputs,
                        run_id,
                        canvas,
                        cell_alias,
                    ),
                )
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
