import linecache
import logging
from enum import Enum

from pydantic import BaseModel


class MorphFunctionLoadErrorCategory(str, Enum):
    IMPORT_ERROR = "IMPORT_ERROR"
    DUPLICATED_ALIAS = "DUPLICATED_ALIAS"
    MISSING_ALIAS = "MISSING_ALIAS"
    CYCLIC_ALIAS = "CYCLIC_ALIAS"
    INVALID_SYNTAX = "INVALID_SYNTAX"


class MorphFunctionLoadError(BaseModel):
    category: MorphFunctionLoadErrorCategory
    file_path: str
    name: str
    error: str


def logging_file_error_exception(
    exc: BaseException, target_file: str, logger: logging.Logger
) -> str:
    tb = exc.__traceback__
    filtered_traceback = []
    error_txt = ""

    while tb is not None:
        frame = tb.tb_frame
        code = frame.f_code
        if target_file in code.co_filename:
            filtered_traceback.append(
                {
                    "filename": code.co_filename,
                    "lineno": tb.tb_lineno,
                    "name": code.co_name,
                    "line": linecache.getline(code.co_filename, tb.tb_lineno).strip(),
                }
            )
        tb = tb.tb_next

    for entry in filtered_traceback:
        entry_txt = f"""
'File "{entry["filename"]}", line {entry["lineno"]}, in {entry["name"]}'
    {entry["line"]}
"""
        error_txt += entry_txt
    return error_txt
