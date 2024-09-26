import os
from typing import List, Optional

import yaml
from pydantic import BaseModel, Field

from morph.constants import MorphConstant
from morph.task.utils.profile import (
    CONNECTION_DETAIL_TYPE,
    CONNECTION_TYPE,
    BigqueryConnectionServiceAccount,
    BigqueryConnectionServiceAccountJson,
    DatabaseConnection,
    MorphConnection,
    MysqlConnection,
    PostgresqlConnection,
    RedshiftConnection,
    SnowflakeConnectionKeyPair,
    SnowflakeConnectionUserPassword,
)


class MorphProject(BaseModel):
    source_paths: List[str] = Field(default_factory=lambda: ["src"])
    knowledge_paths: List[str] = Field(default_factory=lambda: ["knowledge"])
    template_paths: List[str] = Field(default_factory=lambda: ["templates"])
    default_connection: Optional[DatabaseConnection] = None

    class Config:
        arbitrary_types_allowed = True  # DatabaseConnection などのクラスを使うため


def default_initial_project() -> MorphProject:
    return MorphProject()


def load_project(project_root: str) -> Optional[MorphProject]:
    config_path = os.path.join(project_root, MorphConstant.MORPH_PROJECT_YAML)
    if not os.path.exists(config_path):
        return None

    with open(config_path, "r") as f:
        data = yaml.safe_load(f)

    if "default_connection" in data and isinstance(data["default_connection"], dict):
        connection_data = data["default_connection"]
        connection_type = connection_data.get("type")
        connection_method = connection_data.get("method", None)

        if connection_type == CONNECTION_TYPE.morph.value:
            data["default_connection"] = MorphConnection(**connection_data)
        elif connection_type == CONNECTION_TYPE.postgres.value:
            data["default_connection"] = PostgresqlConnection(**connection_data)
        elif connection_type == CONNECTION_TYPE.mysql.value:
            data["default_connection"] = MysqlConnection(**connection_data)
        elif connection_type == CONNECTION_TYPE.redshift.value:
            data["default_connection"] = RedshiftConnection(**connection_data)
        elif connection_type == CONNECTION_TYPE.snowflake:
            if connection_method == CONNECTION_DETAIL_TYPE.snowflake_user_password:
                data["default_connection"] = SnowflakeConnectionUserPassword(
                    **connection_data
                )
            elif connection_method == CONNECTION_DETAIL_TYPE.snowflake_key_pair:
                data["default_connection"] = SnowflakeConnectionKeyPair(
                    **connection_data
                )
        elif connection_type == CONNECTION_TYPE.bigquery:
            if connection_method == CONNECTION_DETAIL_TYPE.bigquery_service_account:
                data["default_connection"] = BigqueryConnectionServiceAccount(
                    **connection_data
                )
            elif (
                connection_method
                == CONNECTION_DETAIL_TYPE.bigquery_service_account_json
            ):
                data["default_connection"] = BigqueryConnectionServiceAccountJson(
                    **connection_data
                )
        else:
            raise ValueError(f"Unknown connection type: {connection_type}")

    return MorphProject(**data)


def save_project(project_root: str, project: MorphProject) -> None:
    config_path = os.path.join(project_root, MorphConstant.MORPH_PROJECT_YAML)
    with open(config_path, "w") as f:
        yaml.safe_dump(project.model_dump(), f)
