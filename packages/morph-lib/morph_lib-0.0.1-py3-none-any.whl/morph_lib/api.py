from __future__ import annotations

import glob
import os
import urllib.parse
from typing import Dict, List, Optional, Union, cast

import pandas as pd
import requests
import urllib3
from morph_lib.type import (
    EnvVars,
    ListStorageDirectoryResponse,
    LoadDataParams,
    MorphApiError,
    RefResponse,
    SignedUrlResponse,
)
from morph_lib.utils.response import (
    convert_filepath_to_df,
    convert_signed_url_response_to_dataframe,
    handle_morph_response,
)
from morph_lib.utils.sql import SQLUtils
from pandas import DataFrame
from requests.exceptions import Timeout
from urllib3.exceptions import InsecureRequestWarning

from morph.config.project import MorphProject, load_project
from morph.constants import MorphConstant
from morph.task.utils.connections.connector import Connector
from morph.task.utils.morph import find_project_root_dir
from morph.task.utils.os import OsUtils
from morph.task.utils.profile import (
    CONNECTION_TYPE,
    Connection,
    DatabaseConnection,
    MorphConnection,
    ProfileYaml,
)
from morph.task.utils.run_backend.state import MorphGlobalContext

urllib3.disable_warnings(InsecureRequestWarning)


# ===============================================
#
# Implementation
#
# ===============================================
def _canonicalize_base_url(base_url: str) -> str:
    if base_url.startswith("http"):
        return base_url
    else:
        return f"https://{base_url}"


def _read_configuration_from_env() -> EnvVars:
    """
    Read configuration from environment variables
    These variables are loaded from ini file when the morph run command is executed
    """
    database_id_value = os.getenv("MORPH_DATABASE_ID", "")
    base_url_value = os.getenv("MORPH_BASE_URL", "")
    team_slug_value = os.getenv("MORPH_TEAM_SLUG", "")
    api_key_value = os.getenv("MORPH_API_KEY", "")
    canvas_value = os.getenv("MORPH_CANVAS")

    return EnvVars(
        database_id=database_id_value,
        base_url=base_url_value,
        team_slug=team_slug_value,
        api_key=api_key_value,
        canvas=canvas_value,
    )


def _get_cell_type(filepath: str) -> str:
    ext = filepath.split(".")[-1]
    if ext == "py":
        return "python"
    elif ext == "sql":
        return "sql"
    return "file"


def __execute_sql_impl(
    sql: str,
    connection_slug: str | None = None,
) -> pd.DataFrame:
    config_from_env = _read_configuration_from_env()
    database_id = config_from_env.database_id

    cloud_connection: Optional[Union[Connection, DatabaseConnection]] = None

    if connection_slug is not None:
        cloud_connection = ProfileYaml.find_cloud_connection(connection_slug)
        if (
            cloud_connection.type == CONNECTION_TYPE.bigquery
            or cloud_connection.type == CONNECTION_TYPE.snowflake
            or cloud_connection.type == CONNECTION_TYPE.redshift
            or cloud_connection.type == CONNECTION_TYPE.mysql
            or cloud_connection.type == CONNECTION_TYPE.postgres
        ):
            try:
                connector = Connector(
                    connection_slug if connection_slug is not None else "",
                    cloud_connection,
                    is_cloud=True,
                )
                content = connector.execute_sql(sql)
                return content
            except Exception as e:
                raise MorphApiError(f"SQL error: {e}")
        else:
            raise MorphApiError(
                f"Connection type {cloud_connection.type} is not supported"
            )
    else:
        project: Optional[MorphProject] = load_project(find_project_root_dir())
        if project and project.default_connection:
            cloud_connection = project.default_connection
            if isinstance(cloud_connection, MorphConnection):
                if cloud_connection.connection_slug is None:
                    profile = ProfileYaml.load_yaml()
                    cloud_connection = ProfileYaml.find_connection(profile, database_id)
                    if cloud_connection is None:
                        db, cloud_connection = ProfileYaml.find_builtin_db_connection()
                        profile.add_connections({db: cloud_connection})
                        profile.save_yaml(True)
                else:
                    cloud_connection = ProfileYaml.find_cloud_connection(
                        cloud_connection.connection_slug
                    )
        else:
            profile = ProfileYaml.load_yaml()
            cloud_connection = ProfileYaml.find_connection(profile, database_id)
            if cloud_connection is None:
                db, cloud_connection = ProfileYaml.find_builtin_db_connection()
                profile.add_connections({db: cloud_connection})
                profile.save_yaml(True)

        connector = Connector(
            connection_slug or "",
            cloud_connection,
            is_cloud=True,
        )
        return connector.execute_sql(sql)


def __get_data_path_impl(
    filepath: str,
    specific_dirpath: str | None = None,
    specific_filepath: str | None = None,
) -> str | None:
    config_from_env = _read_configuration_from_env()
    database_id = config_from_env.database_id
    team_slug = config_from_env.team_slug

    project_root = find_project_root_dir()

    context = MorphGlobalContext.get_instance()
    errors = context.load(project_root)
    if len(errors) > 0:
        raise MorphApiError(f"Failed to load morph functions: {errors}")

    resources = context.search_meta_objects_by_path(filepath)
    if not resources or len(resources) < 1:
        raise MorphApiError(f"Reference cell {filepath} not found")
    resource = resources[0]
    filepath = resource.id.split(":")[0] if resource.id else ""
    cell_type = _get_cell_type(filepath)

    if cell_type == "file":
        if specific_dirpath is not None:
            abs_dir_path = os.path.abspath(specific_dirpath)
            if specific_filepath is not None:
                abs_specific_filepath = os.path.abspath(specific_filepath)
                if os.path.exists(abs_specific_filepath):
                    return abs_specific_filepath
                storage_path = _get_pre_signed_url_path(
                    abs_specific_filepath, team_slug, database_id
                )
                return __get_presigned_url(storage_path)
            if os.path.exists(abs_dir_path):
                latest_filepath = __get_latest_file(abs_dir_path)
                if latest_filepath is not None:
                    return latest_filepath
                storage_data = __list_storage_dirs(abs_dir_path)
                if storage_data is not None and len(storage_data.files) > 0:
                    storage_path = _get_pre_signed_url_path(
                        storage_data.files[0].path, team_slug, database_id
                    )
                    return __get_presigned_url(storage_path)
            return None
        abs_file_path = os.path.abspath(filepath)
        if os.path.exists(abs_file_path):
            return abs_file_path
        return None
    elif cell_type == "directory":
        abs_dir_path = os.path.abspath(filepath)
        if specific_filepath is not None:
            abs_specific_filepath = os.path.abspath(specific_filepath)
            if os.path.exists(abs_specific_filepath):
                return abs_specific_filepath
            storage_path = _get_pre_signed_url_path(
                abs_specific_filepath, team_slug, database_id
            )
            return __get_presigned_url(storage_path)
        if os.path.exists(abs_dir_path):
            latest_filepath = __get_latest_file(abs_dir_path)
            if latest_filepath is not None:
                return latest_filepath
            storage_data = __list_storage_dirs(abs_dir_path)
            if storage_data is not None and len(storage_data.files) > 0:
                storage_path = _get_pre_signed_url_path(
                    storage_data.files[0].path, team_slug, database_id
                )
                return __get_presigned_url(storage_path)
        return None
    else:
        if specific_dirpath is not None:
            abs_dir_path = os.path.abspath(specific_dirpath)
            if specific_filepath is not None:
                abs_specific_filepath = os.path.abspath(specific_filepath)
                if os.path.exists(abs_specific_filepath):
                    return abs_specific_filepath
                storage_path = _get_pre_signed_url_path(
                    abs_specific_filepath, team_slug, database_id
                )
                return __get_presigned_url(storage_path)
            if os.path.exists(abs_dir_path):
                latest_filepath = __get_latest_file(abs_dir_path)
                if latest_filepath is not None:
                    return latest_filepath
                storage_data = __list_storage_dirs(abs_dir_path)
                if storage_data is not None and len(storage_data.files) > 0:
                    storage_path = _get_pre_signed_url_path(
                        storage_data.files[0].path, team_slug, database_id
                    )
                    return __get_presigned_url(storage_path)
            return None
        else:
            if specific_filepath is not None:
                abs_specific_filepath = os.path.abspath(specific_filepath)
                if os.path.exists(abs_specific_filepath):
                    return abs_specific_filepath
                storage_path = _get_pre_signed_url_path(
                    abs_specific_filepath, team_slug, database_id
                )
                return __get_presigned_url(storage_path)
            abs_dir_path_ = (
                resource.output_paths[0]
                if resource.output_paths and len(resource.output_paths) > 0
                else None
            )
            if abs_dir_path_ is None:
                abs_dir_path_ = os.path.join(
                    project_root, MorphConstant.PRIVATE_DIR, resource.name or ""
                )
            if abs_dir_path_.endswith("{ext()}"):
                abs_dir_path_ = os.path.dirname(abs_dir_path_)
                if abs_dir_path_.endswith("{name}"):
                    abs_dir_path_ = abs_dir_path_.replace("{name}", resource.name or "")
                abs_dir_path_ = os.path.abspath(abs_dir_path_)
            if os.path.exists(abs_dir_path_):
                latest_filepath = __get_latest_file(abs_dir_path_)
                if latest_filepath is not None:
                    return latest_filepath
                storage_data = __list_storage_dirs(abs_dir_path_)
                if storage_data is not None and len(storage_data.files) > 0:
                    storage_path = _get_pre_signed_url_path(
                        storage_data.files[0].path, team_slug, database_id
                    )
                    return __get_presigned_url(storage_path)
            return None


def __get_file_impl(
    filepath: str,
) -> str:
    config_from_env = _read_configuration_from_env()
    database_id = config_from_env.database_id
    team_slug = config_from_env.team_slug

    expanded_filepath = os.path.expanduser(filepath)
    abs_path = OsUtils.get_abs_path(expanded_filepath, find_project_root_dir())
    if os.path.exists(abs_path):
        return abs_path

    storage_path = _get_pre_signed_url_path(abs_path, team_slug, database_id)
    return __get_presigned_url(storage_path)


# ===============================================
#
# Utils
#
# ===============================================
def __get_presigned_url(storage_path: str) -> str:
    config_from_env = _read_configuration_from_env()
    base_url = config_from_env.base_url
    team_slug = config_from_env.team_slug
    api_key = config_from_env.api_key

    headers = {
        "teamSlug": team_slug,
        "X-Api-Key": api_key,
    }

    split_url = urllib.parse.urlsplit(base_url)
    request_url = urllib.parse.urljoin(
        _canonicalize_base_url(base_url),
        f"{split_url.path}/resource/morph-storage/download-url",
    )

    query_params = {
        "filename": storage_path,
    }

    request_url += f"?{urllib.parse.urlencode(query_params)}"

    try:
        response = requests.get(request_url, headers=headers)
    except Timeout:
        raise MorphApiError("Process Timeout while executing get url")
    except Exception as e:
        raise MorphApiError(f"{e}")

    response_body = handle_morph_response(response)
    if "preSignedDownloadUrl" not in response_body:
        raise MorphApiError("preSignedDownloadUrl is not in response body")
    if not response_body["preSignedDownloadUrl"]:
        raise MorphApiError("preSignedDownloadUrl is empty")
    if not isinstance(response_body["preSignedDownloadUrl"], str):
        raise MorphApiError("preSignedDownloadUrl is invalid")
    return response_body["preSignedDownloadUrl"]


def __get_latest_file(abs_path: str) -> str | None:
    if os.path.isfile(abs_path):
        return abs_path

    files = glob.glob(os.path.join(abs_path, "*"))

    if not files:
        return None

    latest_file = max(files, key=os.path.getmtime)

    return latest_file


def __list_storage_dirs(
    prefix: str,
    depth: int = 2,
) -> ListStorageDirectoryResponse | None:
    config_from_env = _read_configuration_from_env()
    database_id = config_from_env.database_id
    base_url = config_from_env.base_url
    api_key = config_from_env.api_key

    headers = {
        "X-Api-Key": api_key,
    }

    split_url = urllib.parse.urlsplit(base_url)
    request_url = urllib.parse.urljoin(
        _canonicalize_base_url(base_url),
        f"{split_url.path}/resource/morph-storage/directory",
    )

    query_params = {
        "databaseId": database_id,
        "depth": depth,
        "path": prefix,
    }
    request_url += f"?{urllib.parse.urlencode(query_params)}"

    try:
        response = requests.get(request_url, headers=headers)
    except Timeout:
        raise MorphApiError("Process Timeout while executing list_storage_dirs")
    except Exception as e:
        raise MorphApiError(f"{e}")

    response_body = handle_morph_response(response)

    try:
        return ListStorageDirectoryResponse(**response_body)
    except Exception as e:
        raise MorphApiError(f"list_storage_dirs error: {e}")


def __process_records(
    action: str,
    *args: Union[RefResponse, pd.DataFrame],
    **kwargs: Union[str, int, bool, List[str], Dict[str, str]],
) -> None:
    # Validate action
    if action not in {"create", "insert", "update"}:
        raise MorphApiError(
            "Invalid action provided. Must be 'create', 'insert', or 'update'."
        )

    # Validate *args
    if not args or (
        not isinstance(args[0], RefResponse) and not isinstance(args[0], pd.DataFrame)
    ):
        raise MorphApiError(
            "Invalid *args provided: RefResponse or pd.DataFrame is required."
        )

    # Validate **kwargs
    if "table_name" not in kwargs:
        raise MorphApiError("Invalid **kwargs provided: 'table_name' is required.")
    table_name_value = kwargs.pop("table_name")
    if not isinstance(table_name_value, str):
        raise MorphApiError("Invalid **kwargs provided: 'table_name' must be a string.")
    table_name: str = table_name_value

    column_types_value = kwargs.pop("column_types", None)
    if column_types_value is not None and not isinstance(column_types_value, dict):
        raise MorphApiError(
            "Invalid **kwargs provided: 'column_types' must be a dictionary."
        )
    column_types: Optional[Dict[str, str]] = column_types_value

    # DataFrame to be processed
    data: pd.DataFrame
    if isinstance(args[0], RefResponse):
        if args[0].cell_type != "sql":
            raise MorphApiError(f"Cell {args[0].alias} is not a SQL cell")
        if args[0].cell_type != "sql":
            raise MorphApiError(f"Cell {args[0].alias} is not a SQL cell")
        if not args[0].code:
            raise MorphApiError("SQL code is empty")
        sql = args[0].code
        connection_slug = args[0].connection_slug
        data = __execute_sql_impl(sql, connection_slug)
    else:
        data = args[0]
    if not isinstance(data, pd.DataFrame):
        raise MorphApiError("Invalid data type provided. pd.DataFrame is required.")

    sql_utils = SQLUtils(data, table_name, column_types)

    if action == "create":
        sqls = sql_utils.generate_replace_sql()
        __execute_sql_impl(sqls["create_table_sql"])
        if not data.empty:
            __execute_sql_impl(sqls["insert_sql"])
    elif action == "insert":
        __execute_sql_impl(sql_utils.generate_insert_sql())
    elif action == "update":
        if not kwargs.get("key_columns") or not isinstance(kwargs["key_columns"], list):
            raise MorphApiError(
                "Invalid **kwargs provided: key_columns is required for update."
            )
        __execute_sql_impl(sql_utils.generate_update_sql(kwargs["key_columns"]))


def __load_data_impl(
    filepath: str | None = None,
    timestamp: int | None = None,
) -> pd.DataFrame:
    config_from_env = _read_configuration_from_env()
    base_url = config_from_env.base_url
    team_slug = config_from_env.team_slug
    api_key = config_from_env.api_key

    headers = {
        "teamSlug": team_slug,
        "X-Api-Key": api_key,
    }

    split_url = urllib.parse.urlsplit(base_url)
    request_url = urllib.parse.urljoin(
        _canonicalize_base_url(base_url),
        f"{split_url.path}/resource/morph-storage/download-url",
    )

    query_params = {}
    if filepath is not None:
        query_params["filename"] = filepath
    if timestamp is not None:
        query_params["timestamp"] = str(timestamp)
    request_url += f"?{urllib.parse.urlencode(query_params)}"

    try:
        response = requests.get(request_url, headers=headers)
    except Timeout:
        raise MorphApiError("Process Timeout while executing load_data")
    except Exception as e:
        raise MorphApiError(f"{e}")

    response_body = handle_morph_response(response)

    try:
        structured_response_body = SignedUrlResponse(
            url=response_body["preSignedDownloadUrl"]
        )
        df = convert_signed_url_response_to_dataframe(structured_response_body)
        return df
    except Exception as e:
        raise MorphApiError(f"load_data error: {e}")


MORPH_STORAGE_PREFIX = "morph-storage://"


def _get_pre_signed_url_path(file_path: str, team_slug: str, database_id: str) -> str:
    if file_path.startswith(MORPH_STORAGE_PREFIX):
        return file_path
    return "{}vm/{}/{}/{}".format(
        MORPH_STORAGE_PREFIX,
        team_slug,
        database_id,
        file_path if not file_path.startswith("/") else file_path[1:],
    )


# ===============================================
#
# Functions
#
# ===============================================
def execute_sql(*args: Union[RefResponse, str]) -> pd.DataFrame:
    """
    Execute SQL query
    """
    sql: str = args[0] if isinstance(args[0], str) else ""
    connection_slug: str | None = None

    # If the first argument is a RefResponse, extract the SQL code and connection slug
    if args and isinstance(args[0], RefResponse):
        if args[0].cell_type != "sql":
            raise MorphApiError(f"Cell {args[0].alias} is not a SQL cell")
        if not args[0].code:
            raise MorphApiError("SQL code is empty")
        sql = args[0].code
        connection_slug = args[0].connection_slug

    if len(args) > 1 and isinstance(args[1], str):
        connection_slug = args[1]

    return __execute_sql_impl(sql, connection_slug)


def ref(reference: str) -> RefResponse:
    """
    Get the reference cell information
    @param: reference: The name of the reference cell alias
    """
    project_root = find_project_root_dir()
    context = MorphGlobalContext.get_instance()
    errors = context.load(project_root)
    if len(errors) > 0:
        raise MorphApiError(f"Failed to load morph functions: {errors}")

    resource = context.search_meta_object_by_name(reference)
    if not resource:
        raise MorphApiError(f"Reference cell {reference} not found")

    filepath = resource.id.split(":")[0] if resource.id else ""
    cell_type = _get_cell_type(filepath)

    return RefResponse(
        cell_type=cell_type,
        filepath=filepath,
        alias=reference,
        code=open(filepath, "r").read(),
        connection_slug=resource.connection if resource.connection else None,
    )


def read_dir(target_dir: str = "/") -> List[str]:
    """
    Read directories
    if the directory is in the data directory, it will also list the storage directories
    """
    project_root = find_project_root_dir()
    expanded_target_dir = os.path.expanduser(target_dir)
    abs_dir_path = OsUtils.get_abs_path(expanded_target_dir, project_root)

    dirs = os.listdir(abs_dir_path)
    if abs_dir_path.startswith(os.path.join(project_root, "data")):
        storage_dirs = __list_storage_dirs(abs_dir_path, 1)
        if storage_dirs is not None:
            for storage_dir in storage_dirs.directories:
                dirs.append(storage_dir.name)
            for storage_file in storage_dirs.files:
                dirs.append(storage_file.name)

    return list(set(dirs))


def get_file(*args, **kwargs):
    """
    Get the file path or URL of the file
    """
    if args and isinstance(args[0], RefResponse):
        ref_dict = {
            "filepath": args[0].filepath,
        }
        return __get_file_impl(**ref_dict, **kwargs)
    else:
        return __get_file_impl(*args, **kwargs)


def get_data_path(*args, **kwargs):
    """
    Get the data path or URL of the data
    @param: args: RefResponse or filepath, specific_dirpath, specific_filepath
    """
    if args and isinstance(args[0], RefResponse):
        ref_dict = {
            "filepath": args[0].filepath,
        }
        if len(args) > 1:
            ref_dict["specific_dirpath"] = args[1]
        if len(args) > 2:
            ref_dict["specific_filepath"] = args[2]
        return __get_data_path_impl(**ref_dict, **kwargs)
    else:
        return __get_data_path_impl(*args, **kwargs)


def create_table(
    *args: Union[RefResponse, pd.DataFrame],
    **kwargs: Union[str, int, bool],
) -> None:
    """
    Create a table and insert data
    """
    __process_records("create", *args, **kwargs)


def insert_records(
    *args: Union[RefResponse, pd.DataFrame],
    **kwargs: Union[str, int, bool],
) -> None:
    """
    Insert records into the table
    """
    __process_records("insert", *args, **kwargs)


def update_records(
    *args: Union[RefResponse, pd.DataFrame],
    **kwargs: Union[str, int, bool, List[str]],
) -> None:
    """
    Update records in the table
    """
    __process_records("update", *args, **kwargs)


def generate_report(
    refs: list[RefResponse],
    prompt: Optional[str] = None,
    language: Optional[str] = None,
) -> str:
    """
    Generate report from the references
    """
    config_from_env = _read_configuration_from_env()
    database_id = config_from_env.database_id
    base_url = config_from_env.base_url
    team_slug = config_from_env.team_slug
    api_key = config_from_env.api_key
    canvas = config_from_env.canvas

    if "dashboard-api" not in base_url:
        base_url = base_url.replace("api", "dashboard-api")

    for ref in refs:
        if ref.cell_type != "python":
            raise MorphApiError(f"Cell {ref.alias} is not a Python cell")

    headers = {
        "teamSlug": team_slug,
        "X-Api-Key": api_key,
    }

    url = urllib.parse.urljoin(
        _canonicalize_base_url(base_url),
        "/agent/chat/report",
    )

    request = {
        "databaseId": database_id,
        "canvas": canvas,
        "files": [ref.alias for ref in refs],
        "prompt": prompt,
        "language": language,
    }
    try:
        response = requests.post(url, headers=headers, json=request, verify=True)
    except Timeout:
        raise MorphApiError("Process Timeout while executing generate_report")
    except Exception as e:
        raise MorphApiError(f"generate_report error: {e}")

    response_body = handle_morph_response(response)
    return response_body["report"]  # type: ignore


def send_email(
    refs: list[RefResponse],
    emails: list[str],
    subject: str,
    body: str,
) -> None:
    """
    Send email with attachments
    """
    config_from_env = _read_configuration_from_env()
    database_id = config_from_env.database_id
    base_url = config_from_env.base_url
    team_slug = config_from_env.team_slug
    api_key = config_from_env.api_key

    attchments: List[Dict[str, str]] = []
    for ref in refs:
        if ref.cell_type != "python":
            raise MorphApiError(f"Cell {ref.alias} is not a Python cell")
        url = get_data_path(ref.filepath)
        if url is None:
            continue
        if not url.startswith("http"):
            storage_path = _get_pre_signed_url_path(url, team_slug, database_id)
            url = __get_presigned_url(storage_path)
        filename = os.path.basename(ref.filepath)
        attchments.append({"path": url, "filename": filename})

    if len(attchments) < 1:
        raise MorphApiError("No attachments found")

    headers = {
        "teamSlug": team_slug,
        "X-Api-Key": api_key,
    }

    url = f"{_canonicalize_base_url(base_url)}/{database_id}/python/email"

    request = {
        "attachments": attchments,
        "emails": emails,
        "subject": subject,
        "body": body,
    }

    try:
        response = requests.post(url, headers=headers, json=request, verify=True)
    except Timeout:
        raise MorphApiError("Process Timeout while executing send_email")
    except Exception as e:
        raise MorphApiError(f"send_email error: {e}")

    handle_morph_response(response)


def load_data(
    *args: LoadDataParams, **kwargs: Dict[str, Union[str, int, bool]]
) -> Optional[DataFrame]:
    project_root = find_project_root_dir()

    if args and isinstance(args[0], RefResponse):
        ref = args[0]
        if ref.cell_type == "sql":
            ref_dict = {
                "sql": ref.code,
                "connection_slug": ref.connection_slug,
            }
            return __execute_sql_impl(**ref_dict, **kwargs)  # type: ignore
        elif ref.cell_type == "file":
            if not ref.filepath.startswith(MORPH_STORAGE_PREFIX):
                return convert_filepath_to_df(ref.filepath)
            ref_dict = {
                "filepath": ref.filepath,
            }
            return __load_data_impl(**ref_dict, **kwargs)  # type: ignore
        elif ref.cell_type == "python":
            filepath = __get_data_path_impl(ref.filepath)
            if filepath is None:
                return filepath
            if not filepath.startswith(MORPH_STORAGE_PREFIX):
                return convert_filepath_to_df(filepath)
            return __load_data_impl(filepath, **kwargs)  # type: ignore
        else:
            raise MorphApiError(f"Cell {ref.filepath} is not a valid cell type")
    elif "type" in args[0]:  # type: ignore
        arg_dict = args[0]
        config_from_env = _read_configuration_from_env()
        team_slug = config_from_env.team_slug
        database_id = config_from_env.database_id

        if arg_dict["type"] == "sql":  # type: ignore
            omitted_args = {k: v for k, v in arg_dict.items() if k != "type"}  # type: ignore
            return __execute_sql_impl(**omitted_args, **kwargs)  # type: ignore
        elif arg_dict["type"] == "file":  # type: ignore
            omitted_args = {k: v for k, v in arg_dict.items() if k != "type"}  # type: ignore
            if not omitted_args["filepath"].startswith(MORPH_STORAGE_PREFIX):
                filepath = os.path.join(
                    project_root,
                    os.path.realpath(omitted_args["filepath"]),
                )
                if os.path.exists(filepath):
                    return convert_filepath_to_df(filepath)
                else:
                    storage_path = _get_pre_signed_url_path(
                        filepath, team_slug, database_id
                    )
                    return __load_data_impl(storage_path, **kwargs)  # type: ignore
            return __load_data_impl(**omitted_args, **kwargs)  # type: ignore
        elif arg_dict["type"] == "python":  # type: ignore
            omitted_args = {k: v for k, v in arg_dict.items() if k != "type"}  # type: ignore
            reference = omitted_args["reference"]
            if not reference:
                return None
            context = MorphGlobalContext.get_instance()
            errors = context.load(project_root)
            if len(errors) > 0:
                raise MorphApiError(f"Failed to load morph functions: {errors}")
            resource = context.search_meta_object_by_name(str(reference))
            filepath = resource.id.split(":")[0] if resource and resource.id else None
            if not filepath:
                return None
            if not filepath.startswith(MORPH_STORAGE_PREFIX):
                filepath = os.path.join(project_root, os.path.realpath(filepath))
                if os.path.exists(filepath):
                    return convert_filepath_to_df(filepath)
                else:
                    storage_path = _get_pre_signed_url_path(
                        filepath, team_slug, database_id
                    )
                    return __load_data_impl(storage_path, **kwargs)  # type: ignore
            return __load_data_impl(filepath, **kwargs)  # type: ignore
        else:
            raise ValueError("Invalid data cell type provided.")
    else:
        raise ValueError("Invalid data cell type provided.")


def get_auth_token(connection_slug: str) -> str:
    """
    Get and refresh the authentication token from environment variables.
    Make sure to set the environment variables before calling this function.
    @param: connection_slug: The connection slug on morph app
    """
    config_from_env = _read_configuration_from_env()
    base_url = config_from_env.base_url
    team_slug = config_from_env.team_slug
    api_key = config_from_env.api_key

    headers = {
        "teamSlug": team_slug,
        "X-Api-Key": api_key,
    }

    url = f"{_canonicalize_base_url(base_url)}/external-connection/{connection_slug}"

    try:
        response = requests.get(url, headers=headers, verify=True)
    except Timeout:
        raise MorphApiError("Process Timeout while executing get_auth_token")
    except Exception as e:
        raise MorphApiError(f"get_auth_token error: {e}")

    response_body = handle_morph_response(response)
    if (
        response_body["connectionType"] == "mysql"
        or response_body["connectionType"] == "postgres"
        or response_body["connectionType"] == "redshift"
    ):
        raise MorphApiError(f"No auth token in db connection {connection_slug}")
    elif (
        "accessToken" not in response_body["data"]
        or response_body["data"]["accessToken"] is None
    ):
        raise MorphApiError("Failed to get auth token")

    return cast(str, response_body["data"]["accessToken"])


def get_service_connection(
    connection_slug: str,
) -> Connection:
    """
    Get the service connection
    Use `to_dict` method to get the connection class as dictionary
    @param: connection_slug: The connection slug on morph app
    """
    connection = ProfileYaml.find_cloud_connection(connection_slug)
    if connection is None:
        raise MorphApiError(f"Connection {connection_slug} not found")
    return connection
