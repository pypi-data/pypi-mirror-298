from __future__ import annotations

import copy
import json
import os
import sys
from pathlib import Path
from typing import Any, Callable, List, Literal, Optional

import pandas as pd
from pydantic import BaseModel
from typing_extensions import Self

from morph.config.project import load_project
from morph.constants import MorphConstant
from morph.task.utils.knowledge.inspection import (
    MorphKnowledgeMetaObjectGlossaryTerm,
    MorphKnowledgeMetaObjectSchema,
)

from .errors import MorphFunctionLoadError, MorphFunctionLoadErrorCategory
from .inspection import (
    DirectoryScanResult,
    _import_python_file,
    _import_sql_file,
    _import_vg_json_file,
    get_checksum,
    import_files,
)


class MorphFunctionMetaObject(BaseModel):
    id: str
    name: str
    function: Optional[Callable[..., Any]]
    description: Optional[str] = None
    title: Optional[str] = None
    schemas: Optional[List[MorphKnowledgeMetaObjectSchema]] = []
    terms: Optional[List[MorphKnowledgeMetaObjectGlossaryTerm]] = []
    arguments: Optional[List[str]] = []
    data_requirements: Optional[List[str]] = []
    output_paths: Optional[List[str]] = []
    output_type: Optional[
        Literal["dataframe", "csv", "visualization", "markdown", "json"]
    ]
    connection: Optional[str]

    def find_output_cache_path(self) -> Optional[str]:
        if self.output_paths is None or len(self.output_paths) == 0:
            return None

        def _find_file_recursively(directory: str) -> Optional[str]:
            latest_file = None
            for root, _, files in os.walk(directory):
                files_with_paths = [
                    os.path.join(root, file)
                    for file in files
                    if os.path.isfile(os.path.join(root, file))
                ]
                if files_with_paths:
                    latest_in_dir = max(files_with_paths, key=os.path.getmtime)
                    if latest_file is None:
                        latest_file = latest_in_dir
            return latest_file

        place_holders = ["{name}", "{now()}", "{unix()}", "{ext()}"]

        for output_path in self.output_paths:
            if "{name}" in output_path:
                output_path = output_path.replace("{name}", self.name)
            for placeholder in place_holders:
                if placeholder in output_path:
                    directory = os.path.dirname(output_path.split(placeholder)[0])
                    if os.path.exists(directory):
                        file_path = _find_file_recursively(directory)
                        if file_path:
                            return file_path
                    break
            if os.path.exists(output_path) and os.path.isfile(output_path):
                return output_path

        return None


class MorphFunctionMetaObjectCacheItem(BaseModel):
    spec: MorphFunctionMetaObject
    file_path: str
    checksum: str


class MorphFunctionMetaObjectCache(BaseModel):
    directory: str
    directory_checksums: dict[str, str]
    items: List[MorphFunctionMetaObjectCacheItem]
    errors: List[MorphFunctionLoadError]


def _cache_path(directory: str) -> str:
    return f"{directory}/.morph/meta.json"


def load_cache(project_root: str) -> MorphFunctionMetaObjectCache | None:
    cache_path = _cache_path(project_root)
    if not Path(cache_path).exists():
        return None

    with open(cache_path, "r") as f:
        data = json.load(f)

    return MorphFunctionMetaObjectCache.model_validate(data)


def dump_cache(cache: MorphFunctionMetaObjectCache) -> None:
    cache_path = _cache_path(cache.directory)
    if not Path(cache_path).parent.exists():
        Path(cache_path).parent.mkdir(parents=True)

    with open(cache_path, "w") as f:
        json.dump(cache.model_dump(), f, indent=2)


class MorphGlobalContext:
    __data: dict[str, pd.DataFrame]
    __var: dict[str, Any]
    __meta_objects: list[MorphFunctionMetaObject]
    __scans: list[DirectoryScanResult]

    def __init__(self):
        self.__data = {}
        self.__var = {}
        self.__meta_objects = []
        self.__scans = []

    @classmethod
    def get_instance(cls) -> Self:
        if not hasattr(cls, "_instance"):
            cls._instance = cls()  # type: ignore
        return cls._instance  # type: ignore

    @property
    def data(self) -> dict[str, pd.DataFrame]:
        return self.__data

    @property
    def var(self) -> dict[str, Any]:
        return self.__var

    def load(self, directory: str) -> list[MorphFunctionLoadError]:
        project = load_project(directory)
        if project is not None:
            source_paths = project.source_paths
        else:
            source_paths = []

        extra_paths = [MorphConstant.TMP_MORPH_DIR]

        for parent in Path.cwd().parents:
            if str(parent) not in sys.path:
                sys.path.append(str(parent))

        result = import_files(directory, source_paths, extra_paths)
        for key, value in result.sql_contexts.items():
            meta_obj = MorphFunctionMetaObject(
                id=value["id"] if "id" in value else None,
                name=value["name"] if "name" in value else None,
                function=value["function"] if "function" in value else None,
                description=value["description"] if "description" in value else None,
                title=value["title"] if "title" in value else None,
                schemas=value["schemas"] if "schemas" in value else [],
                terms=value["terms"] if "terms" in value else [],
                arguments=value["arguments"] if "arguments" in value else [],
                data_requirements=(
                    value["data_requirements"] if "data_requirements" in value else []
                ),
                output_paths=value["output_paths"] if "output_paths" in value else [],
                output_type=value["output_type"] if "output_type" in value else None,
                connection=value["connection"] if "connection" in value else None,
            )
            self.update_meta_object(key, meta_obj)
        for key, value in result.vg_json_contexts.items():
            meta_obj = MorphFunctionMetaObject(
                id=value["id"] if "id" in value else None,
                name=value["name"] if "name" in value else None,
                function=value["function"] if "function" in value else None,
                description=value["description"] if "description" in value else None,
                title=value["title"] if "title" in value else None,
                schemas=value["schemas"] if "schemas" in value else [],
                terms=value["terms"] if "terms" in value else [],
                arguments=value["arguments"] if "arguments" in value else [],
                data_requirements=(
                    value["data_requirements"] if "data_requirements" in value else []
                ),
                output_paths=value["output_paths"] if "output_paths" in value else [],
                output_type=value["output_type"] if "output_type" in value else None,
                connection=value["connection"] if "connection" in value else None,
            )
            self.update_meta_object(key, meta_obj)

        entirety_errors = self._check_entirety_errors()
        result.errors += entirety_errors
        self.__scans.append(result)
        return result.errors

    def partial_load(
        self, directory: str, target_name: str
    ) -> list[MorphFunctionLoadError]:
        """load required functions only, using cache.
        This function is meant to be used in runtime, where all the necessary analysis functions are already loaded
        except loading actual functions.
        """
        cache = load_cache(directory)
        if cache is None:
            errors = self.load(directory)
            if len(errors) == 0:
                self.dump()

            return errors

        project = load_project(directory)
        if project is not None:
            source_paths = project.source_paths
        else:
            source_paths = []

        extra_paths = [MorphConstant.TMP_MORPH_DIR]
        checksum_matched = True
        compare_dirs = []
        if len(source_paths) == 0:
            compare_dirs.append(Path(directory))
        else:
            for source_path in source_paths:
                compare_dirs.append(Path(f"{directory}/{source_path}"))

        for epath in extra_paths:
            epath_p = Path(epath)
            if not epath_p.exists() or not epath_p.is_dir():
                continue
            compare_dirs.append(epath_p)

        for compare_dir in compare_dirs:
            if cache.directory_checksums.get(
                compare_dir.as_posix(), ""
            ) != get_checksum(Path(compare_dir)):
                checksum_matched = False
                break

        if not checksum_matched:
            errors = self.load(directory)
            if len(errors) == 0:
                self.dump()

            return errors

        for parent in Path.cwd().parents:
            if str(parent) not in sys.path:
                sys.path.append(str(parent))

        return self._partial_load(target_name, cache)

    def _partial_load(
        self, target_name: str, cache: MorphFunctionMetaObjectCache
    ) -> list[MorphFunctionLoadError]:
        target_item: MorphFunctionMetaObjectCacheItem | None = None
        for item in cache.items:
            if item.spec.name == target_name or (
                item.spec.id and item.spec.id.startswith(target_name)
            ):
                target_item = item
                break
        if target_item is None:
            return [
                MorphFunctionLoadError(
                    category=MorphFunctionLoadErrorCategory.IMPORT_ERROR,
                    file_path="",
                    name=target_name,
                    error="Not found",
                )
            ]

        suffix = target_item.file_path.split(".")[-1]
        if suffix == "py":
            _, error = _import_python_file(target_item.file_path)
        elif suffix == "sql":
            _, context, error = _import_sql_file(target_item.file_path)
            for key, value in context.items():
                meta = MorphFunctionMetaObject(
                    id=value["id"] if "id" in value else None,
                    name=value["name"] if "name" in value else None,
                    function=value["function"] if "function" in value else None,
                    description=(
                        value["description"] if "description" in value else None
                    ),
                    title=value["title"] if "title" in value else None,
                    schemas=value["schemas"] if "schemas" in value else [],
                    terms=value["terms"] if "terms" in value else [],
                    arguments=value["arguments"] if "arguments" in value else [],
                    data_requirements=(
                        value["data_requirements"]
                        if "data_requirements" in value
                        else []
                    ),
                    output_paths=(
                        value["output_paths"] if "output_paths" in value else []
                    ),
                    output_type=(
                        value["output_type"] if "output_type" in value else None
                    ),
                    connection=value["connection"] if "connection" in value else None,
                )
                self.update_meta_object(key, meta)
        elif target_item.file_path.endswith(".vg.json"):
            _, context, error = _import_vg_json_file(target_item.file_path)
            for key, value in context.items():
                meta = MorphFunctionMetaObject(
                    id=value["id"] if "id" in value else None,
                    name=value["name"] if "name" in value else None,
                    function=value["function"] if "function" in value else None,
                    description=(
                        value["description"] if "description" in value else None
                    ),
                    title=value["title"] if "title" in value else None,
                    schemas=value["schemas"] if "schemas" in value else [],
                    terms=value["terms"] if "terms" in value else [],
                    arguments=value["arguments"] if "arguments" in value else [],
                    data_requirements=(
                        value["data_requirements"]
                        if "data_requirements" in value
                        else []
                    ),
                    output_paths=(
                        value["output_paths"] if "output_paths" in value else []
                    ),
                    output_type=(
                        value["output_type"] if "output_type" in value else None
                    ),
                    connection=value["connection"] if "connection" in value else None,
                )
                self.update_meta_object(key, meta)
        else:
            return [
                MorphFunctionLoadError(
                    category=MorphFunctionLoadErrorCategory.IMPORT_ERROR,
                    file_path=target_item.file_path,
                    name=target_name,
                    error="Unknown file type",
                )
            ]

        errors = []
        if error is not None:
            errors.append(error)

        requirements = target_item.spec.data_requirements or []
        for requirement in requirements:
            errors += self._partial_load(requirement, cache)

        return errors

    def dump(self) -> MorphFunctionMetaObjectCache:
        if len(self.__scans) == 0:
            raise ValueError("No files are loaded.")

        scan = self.__scans[-1]
        cache_items: list[MorphFunctionMetaObjectCacheItem] = []
        for scan_item in scan.items:
            for obj in self.__meta_objects:
                # id is formatted as {filename}:{function_name}
                obj_filepath = obj.id.split(":")[0] if obj.id else ""
                if scan_item.file_path == obj_filepath:
                    cache_obj = copy.deepcopy(obj)
                    if cache_obj.function:
                        cache_obj.function = None
                    item = MorphFunctionMetaObjectCacheItem(
                        spec=cache_obj,
                        file_path=scan_item.file_path,
                        checksum=scan_item.checksum,
                    )
                    cache_items.append(item)

        cache = MorphFunctionMetaObjectCache(
            directory=scan.directory,
            directory_checksums=scan.directory_checksums,
            items=cache_items,
            errors=scan.errors,
        )
        dump_cache(cache)
        return cache

    def _add_data(self, key: str, value: pd.DataFrame) -> None:
        self.__data[key] = value

    def _clear_var(self) -> None:
        self.__var = {}

    def _add_var(self, key: str, value: Any) -> None:
        self.__var[key] = value

    def update_meta_object(self, fid: str, obj: MorphFunctionMetaObject) -> None:
        MorphFunctionMetaObject.model_validate(obj)
        current_obj = self.search_meta_object(fid)
        if current_obj is None:
            obj.id = fid
            self.__meta_objects.append(obj)
        else:
            current_obj.id = obj.id
            current_obj.name = obj.name
            current_obj.function = current_obj.function or obj.function
            current_obj.description = current_obj.description or obj.description
            current_obj.arguments = list(
                set((current_obj.arguments or []) + (obj.arguments or []))
            )
            current_obj.data_requirements = list(
                set(
                    (current_obj.data_requirements or [])
                    + (obj.data_requirements or [])
                )
            )
            current_obj.output_paths = list(
                set((current_obj.output_paths or []) + (obj.output_paths or []))
            )
            current_obj.output_type = current_obj.output_type or obj.output_type
            current_obj.connection = current_obj.connection or obj.connection

    def search_meta_object(self, fid: str) -> MorphFunctionMetaObject | None:
        for obj in self.__meta_objects:
            if obj.id and obj.id == fid:
                return obj
        return None

    def search_meta_object_by_name(self, name: str) -> MorphFunctionMetaObject | None:
        for obj in self.__meta_objects:
            if obj.name and obj.name == name:
                return obj
        return None

    def search_meta_objects_by_path(
        self, file_path: str
    ) -> list[MorphFunctionMetaObject]:
        objects = []
        for obj in self.__meta_objects:
            if obj.id and obj.id.startswith(file_path):
                objects.append(obj)
        return objects

    def _check_entirety_errors(self) -> list[MorphFunctionLoadError]:
        # check is there's any missing or cyclic alias
        errors: list[MorphFunctionLoadError] = []
        names: list[str] = []
        ids: list[str] = []
        for obj in self.__meta_objects:
            if obj.name in names:
                obj_filepath = obj.id.split(":")[0] if obj.id else ""
                errors.append(
                    MorphFunctionLoadError(
                        category=MorphFunctionLoadErrorCategory.DUPLICATED_ALIAS,
                        file_path=obj_filepath,
                        name=obj.name,
                        error=f"Alias {obj.name} is also defined in {ids[names.index(obj.name)]}",
                    )
                )
                continue
            else:
                names.append(str(obj.name))
                ids.append(str(obj.id))

            requirements = obj.data_requirements or []
            for requirement in requirements:
                dependency = self.search_meta_object_by_name(requirement)
                if dependency is None:
                    obj_filepath = obj.id.split(":")[0] if obj.id else ""
                    errors.append(
                        MorphFunctionLoadError(
                            category=MorphFunctionLoadErrorCategory.MISSING_ALIAS,
                            file_path=obj_filepath,
                            name=requirement,
                            error=f"Requirement {requirement} is not found",
                        )
                    )
                elif obj.name in (dependency.data_requirements or []):
                    obj_filepath = obj.id.split(":")[0] if obj.id else ""
                    errors.append(
                        MorphFunctionLoadError(
                            category=MorphFunctionLoadErrorCategory.MISSING_ALIAS,
                            file_path=obj_filepath,
                            name=requirement,
                            error=f"Requirement {requirement} is cyclic",
                        )
                    )

        return errors
