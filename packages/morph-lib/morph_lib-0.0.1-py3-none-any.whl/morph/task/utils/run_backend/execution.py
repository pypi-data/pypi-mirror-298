from __future__ import annotations

import logging
import os
from typing import Any, List, Optional, Union

import duckdb
import pandas as pd
from jinja2 import BaseLoader, Environment
from pandas.errors import EmptyDataError

from morph.config.project import MorphProject, load_project
from morph.task.utils.connections.connector import Connector
from morph.task.utils.morph import find_project_root_dir
from morph.task.utils.profile import (
    CONNECTION_TYPE,
    Connection,
    DatabaseConnection,
    MorphConnection,
    ProfileYaml,
)

from .state import MorphFunctionMetaObject, MorphGlobalContext


def run_cell(
    cell: str | MorphFunctionMetaObject,
    database_id: str,
    vars: dict[str, dict[str, Any]] = {},
    parent_output_path: dict[str, str] = {},
    use_cache: bool = False,
    dry_run: bool = False,
    logger: logging.Logger | None = None,
) -> Any:
    if dry_run and logger:
        cell_name = cell if isinstance(cell, str) else cell.name
        logger.info("Dry run mode enabled. Running cell: %s", cell_name)

    context = MorphGlobalContext.get_instance()
    if isinstance(cell, str):
        meta_obj = context.search_meta_object_by_name(cell)
        if meta_obj is None:
            raise ValueError("not registered as a morph function.")
    else:
        meta_obj = cell

    if meta_obj.id is None:
        raise ValueError(f"Invalid metadata: {meta_obj}")

    ext = meta_obj.id.split(".")[-1]
    sql = ""
    if ext == "sql":
        sql = _regist_sql_data_requirements(meta_obj, vars)
        meta_obj = context.search_meta_object_by_name(meta_obj.name or "")
        if meta_obj is None:
            raise ValueError("not registered as a morph function.")

    required_data = meta_obj.data_requirements or []
    for data_name in required_data:
        required_meta_obj = context.search_meta_object_by_name(data_name)
        if required_meta_obj is None:
            raise ValueError(
                f"required data '{data_name}' is not registered as a morph function."
            )

        has_cache = False

        parent_output_path_ = parent_output_path.get(data_name, "")
        if parent_output_path_ != "":
            if not os.path.exists(parent_output_path_):
                raise FileNotFoundError(
                    f"parent output path '{parent_output_path_}' not found."
                )
            try:
                result = (
                    pd.read_parquet(parent_output_path_)
                    if parent_output_path_.split(".")[-1] == "parquet"
                    else pd.read_csv(parent_output_path_)
                )
            except EmptyDataError:
                result = pd.DataFrame()
            finally:
                has_cache = True

        if use_cache and not has_cache:
            cache_path = required_meta_obj.find_output_cache_path()
            if cache_path:
                result = (
                    pd.read_parquet(cache_path)
                    if cache_path.split(".")[-1] == "parquet"
                    else pd.read_csv(cache_path)
                )
                has_cache = True

        if not has_cache:
            result = run_cell(
                required_meta_obj.name or "",
                database_id,
                vars,
                parent_output_path,
                use_cache,
            )
        context._add_data(data_name, result)

    context._clear_var()
    vars_for_this = vars.get(meta_obj.name or "", {})
    for var_name, var_value in vars_for_this.items():
        context._add_var(var_name, var_value)

    if meta_obj.arguments:
        for arg in meta_obj.arguments:
            if arg not in context.var:
                pass
                # TODO: add variable validation
                # raise ValueError(f"argument '{arg}' is not provided.")

    if not dry_run:
        if ext == "sql":
            return run_sql(meta_obj, sql, database_id)
        else:
            if not meta_obj.function:
                raise ValueError(f"Invalid metadata: {meta_obj}")
            return meta_obj.function(context)


def _regist_sql_data_requirements(
    resource: MorphFunctionMetaObject, vars: dict[str, dict[str, Any]] = {}
) -> str:
    if not resource.id or not resource.name:
        raise ValueError("resource id or name is not set.")

    context = MorphGlobalContext.get_instance()
    filepath = resource.id
    vars_for_this = vars.get(resource.name, {})

    def _config(**kwargs):
        return ""

    def _argument(v: Optional[str] = None) -> str:
        return ""

    def _connection(v: Optional[str] = None) -> str:
        return ""

    load_data: List[str] = []

    def _load_data(v: Optional[str] = None) -> str:
        nonlocal load_data
        if v is not None and v != "":
            _resource = context.search_meta_object_by_name(v)
            if _resource is None:
                raise FileNotFoundError(f"A resource with alias {v} not found.")
            load_data.append(v)
            output_paths = _resource.output_paths[0] if _resource.output_paths else ""
            return f"'{output_paths}'"
        return ""

    env = Environment(loader=BaseLoader())
    env.globals["config"] = _config
    env.globals["argument"] = _argument
    env.globals["connection"] = _connection
    env.globals["load_data"] = _load_data

    sql = open(filepath, "r").read()
    template = env.from_string(sql)
    sql = template.render(vars_for_this)
    if len(load_data) > 0:
        meta = MorphFunctionMetaObject(
            id=resource.id,
            name=resource.name,
            function=resource.function,
            description=resource.description,
            title=resource.title,
            schemas=resource.schemas,
            terms=resource.terms,
            arguments=resource.arguments,
            data_requirements=load_data,
            output_paths=resource.output_paths,
            output_type=resource.output_type,
            connection=resource.connection,
        )
        context.update_meta_object(filepath, meta)

    return str(sql)


def run_sql(
    resource: MorphFunctionMetaObject,
    sql: str,
    database_id: str,
) -> pd.DataFrame:
    load_data = resource.data_requirements or []
    connection = resource.connection

    if load_data:
        return duckdb.sql(sql).to_df()  # type: ignore

    cloud_connection: Optional[Union[Connection, DatabaseConnection]] = None

    if connection:
        cloud_connection = ProfileYaml.find_cloud_connection(connection)
        if (
            cloud_connection.type == CONNECTION_TYPE.bigquery
            or cloud_connection.type == CONNECTION_TYPE.snowflake
            or cloud_connection.type == CONNECTION_TYPE.postgres
            or cloud_connection.type == CONNECTION_TYPE.redshift
            or cloud_connection.type == CONNECTION_TYPE.mysql
        ):
            connector = Connector(
                connection,
                cloud_connection,
                is_cloud=True,
            )
            return connector.execute_sql(sql)
        else:
            raise ValueError(
                f"Unsupported connection type to query: {cloud_connection.type}"
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
            connection or "",
            cloud_connection,
            is_cloud=True,
        )
        return connector.execute_sql(sql)
