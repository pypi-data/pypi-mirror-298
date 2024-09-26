from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

from jinja2 import Environment, nodes
from pydantic import BaseModel

from .errors import MorphFunctionLoadError, MorphFunctionLoadErrorCategory


class ScanResult(BaseModel):
    file_path: str
    checksum: str


class DirectoryScanResult(BaseModel):
    directory: str
    directory_checksums: Dict[str, str]
    items: List[ScanResult]
    sql_contexts: Dict[str, Any]
    vg_json_contexts: Dict[str, Any]
    errors: List[MorphFunctionLoadError]


def get_checksum(path: Path) -> str:
    """get checksum of file or directory."""
    hash_func = hashlib.sha256()

    if path.is_file():
        with open(str(path), "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)

        return hash_func.hexdigest()
    elif path.is_dir():
        for file in sorted(path.glob("**/*")):
            if file.is_file() and (
                file.suffix == ".py"
                or file.suffix == ".sql"
                or (str(file)).endswith(".vg.json")
            ):
                with open(str(file), "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_func.update(chunk)

        return hash_func.hexdigest()
    else:
        raise ValueError(f"Path {path} is not a file or directory.")


def _import_python_file(
    file_path: str,
) -> tuple[Optional[ScanResult], Optional[MorphFunctionLoadError]]:
    file = Path(file_path)
    if file.suffix != ".py" or file.name == "__init__.py":
        # just skip files that are not python files or __init__.py
        # so it doesn't return neither ScanResult nor MorphFunctionLoadError
        return None, None

    module_name = file.stem
    module_path = file.as_posix()
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        return None, MorphFunctionLoadError(
            category=MorphFunctionLoadErrorCategory.IMPORT_ERROR,
            file_path=module_path,
            name=module_name,
            error="Failed to load module.",
        )

    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        return None, MorphFunctionLoadError(
            category=MorphFunctionLoadErrorCategory.IMPORT_ERROR,
            file_path=module_path,
            name=module_name,
            error="Failed to load module.",
        )

    try:
        spec.loader.exec_module(module)
    except Exception as e:
        return None, MorphFunctionLoadError(
            category=MorphFunctionLoadErrorCategory.IMPORT_ERROR,
            file_path=module_path,
            name=module_name,
            error=f"Fail to evaluate module: {e}",
        )

    return ScanResult(file_path=module_path, checksum=get_checksum(file)), None


def _import_sql_file(
    file_path: str,
) -> tuple[ScanResult | None, dict[str, Any], MorphFunctionLoadError | None]:
    file = Path(file_path)
    if file.suffix != ".sql":
        # just skip files that are not sql files
        # so it doesn't return neither ScanResult nor MorphFunctionLoadError
        return None, {}, None

    module_path = file_path
    sql_contexts: dict[str, Any] = {}
    result = ScanResult(file_path=file.as_posix(), checksum=get_checksum(file))
    with open(file_path, "r") as f:
        content = f.read()
        errors = None
        calls = _parse_jinja_sql(content)
        config = calls["config"][0] if "config" in calls else None
        args = []
        for argument in calls["argument"] if "argument" in calls else []:
            args.append(argument["args"][0])
        name = None
        description = None
        output_paths = None
        output_type = None
        kwargs = {}
        if config is not None:
            if "kwargs" in config:
                kwargs = config["kwargs"]
                if "name" in kwargs:
                    name = kwargs["name"]
                if "description" in kwargs:
                    description = kwargs["description"]
                if "output_paths" in kwargs:
                    output_paths = kwargs["output_paths"]
                if "output_type" in kwargs:
                    output_type = kwargs["output_type"]

        if name is None:
            name = file.stem
        if output_paths is None:
            output_paths = ["_private/{name}/{now()}{ext()}"]
        if output_type is None:
            output_type = "dataframe"
        sql_contexts.update(
            {
                module_path: {
                    "id": module_path,
                    "name": name,
                    "description": description,
                    "output_paths": output_paths,
                    "output_type": output_type,
                    "arguments": args,
                    **kwargs,
                },
            }
        )

        sql_content = calls["sql"] if "sql" in calls else content
        if ";" in sql_content:
            errors = MorphFunctionLoadError(
                category=MorphFunctionLoadErrorCategory.INVALID_SYNTAX,
                file_path=module_path,
                name=name,
                error="SQL file includes ';'. It's prohibited not to use multiple statements.",
            )

        return result, sql_contexts, errors


def _import_vg_json_file(
    file_path: str,
) -> tuple[ScanResult | None, dict[str, Any], MorphFunctionLoadError | None]:
    file = Path(file_path)
    if not file_path.endswith(".vg.json"):
        return None, {}, None

    module_path = file_path
    vg_json_contexts: dict[str, Any] = {}
    result = ScanResult(file_path=file.as_posix(), checksum=get_checksum(file))
    with open(file_path, "r") as f:
        content = f.read()
        errors = None
        name = None

        try:
            data = json.loads(content)
            name = data["morph_name"] if "morph_name" in data else None
        except json.JSONDecodeError as e:  # noqa
            return (
                None,
                {},
                MorphFunctionLoadError(
                    category=MorphFunctionLoadErrorCategory.IMPORT_ERROR,
                    file_path=module_path,
                    name=file.stem,
                    error="JSON decode error.",
                ),
            )

        if name is None:
            return (
                None,
                {},
                MorphFunctionLoadError(
                    category=MorphFunctionLoadErrorCategory.IMPORT_ERROR,
                    file_path=module_path,
                    name=file.stem,
                    error="morph_name is not defined.",
                ),
            )

        vg_json_contexts.update(
            {
                module_path: {
                    "id": module_path,
                    "name": name,
                    "description": None,
                    "output_paths": None,
                    "output_type": None,
                    "arguments": None,
                }
            }
        )

        return result, vg_json_contexts, errors


def import_files(
    directory: str, source_paths: list[str] = [], extra_paths: list[str] = []
) -> DirectoryScanResult:
    """import python and sql files from the directory and evaluate morph functions.
    Args:
        directory (str): directory path to scan.
        source_paths (list[str]): list of source paths to scan, which are relative to the directory.
        extra_paths (list[str]): list of extra paths to scan. These paths are absolute paths.
    """
    p = Path(directory)
    results: list[ScanResult] = []
    errors: list[MorphFunctionLoadError] = []
    ignore_dirs = [".local", ".git", ".venv", "__pycache__"]

    search_paths: list[Path] = []
    if len(source_paths) == 0:
        search_paths.append(p)
    else:
        for source_path in source_paths:
            search_paths.append(p / source_path)

    if len(extra_paths) > 0:
        for epath in extra_paths:
            epath_p = Path(epath)
            if not epath_p.exists() or not epath_p.is_dir():
                continue
            search_paths.append(epath_p)

    directory_checksums: dict[str, str] = {}
    sql_contexts: Dict[str, Any] = {}
    vg_json_contexts: Dict[str, Any] = {}
    for search_path in search_paths:
        for file in search_path.glob("**/*.py"):
            if any(ignore_dir in file.parts for ignore_dir in ignore_dirs):
                continue

            result, error = _import_python_file(file.as_posix())
            if result is not None:
                results.append(result)
            if error is not None:
                errors.append(error)

        for file in search_path.glob("**/*.sql"):
            if any(ignore_dir in file.parts for ignore_dir in ignore_dirs):
                continue

            module_path = file.as_posix()
            result, context, error = _import_sql_file(module_path)
            if result is not None:
                results.append(result)
                sql_contexts.update(context)
            if error is not None:
                errors.append(error)

        for file in search_path.glob("**/*.vg.json"):
            if any(ignore_dir in file.parts for ignore_dir in ignore_dirs):
                continue

            module_path = file.as_posix()
            result, context, error = _import_vg_json_file(module_path)
            if result is not None:
                results.append(result)
                vg_json_contexts.update(context)
            if error is not None:
                errors.append(error)

        directory_checksums[search_path.as_posix()] = get_checksum(search_path)

    return DirectoryScanResult(
        directory=directory,
        directory_checksums=directory_checksums,
        items=results,
        sql_contexts=sql_contexts,
        vg_json_contexts=vg_json_contexts,
        errors=errors,
    )


def _parse_jinja_sql(template):
    env = Environment()
    parsed_content = env.parse(template)
    calls: Dict[str, Any] = {}
    sqls = []

    def visit_node(node):
        if isinstance(node, nodes.TemplateData):
            sql_query = "\n".join(
                line
                for line in node.data.splitlines()
                if not line.strip().startswith("--")
            )
            if sql_query.strip():
                sqls.append(sql_query.strip())

        if isinstance(node, nodes.Call) and hasattr(node.node, "name"):
            func_name = cast(str, node.node.name)

            args = {
                "args": [arg.as_const() for arg in node.args],
                "kwargs": {kw.key: kw.value.as_const() for kw in node.kwargs},
            }

            if func_name in calls:
                calls[func_name].append(args)
            else:
                calls[func_name] = [args]

        for child in node.iter_child_nodes():
            visit_node(child)

    visit_node(parsed_content)

    if len(sqls) > 0:
        calls["sql"] = sqls[-1]

    return calls
