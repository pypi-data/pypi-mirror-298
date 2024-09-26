from __future__ import annotations

import json
from pathlib import Path

from typing_extensions import Self

from morph.config.project import load_project
from morph.task.utils.run_backend.errors import MorphFunctionLoadError
from morph.task.utils.template.inspection import (
    DirectoryTemplateScanResult,
    TemplateScanResult,
    import_files,
)


def _cache_path(directory: str) -> str:
    return f"{directory}/.morph/template.json"


def load_cache(project_root: str) -> DirectoryTemplateScanResult | None:
    cache_path = _cache_path(project_root)
    if not Path(cache_path).exists():
        return None

    with open(cache_path, "r") as f:
        data = json.load(f)

    return DirectoryTemplateScanResult.model_validate(data)


def dump_cache(cache: DirectoryTemplateScanResult) -> None:
    cache_path = _cache_path(cache.directory)
    if not Path(cache_path).parent.exists():
        Path(cache_path).parent.mkdir(parents=True)

    with open(cache_path, "w") as f:
        json.dump(cache.model_dump(), f, indent=2)


class MorphTemplateManager:
    __scans: list[DirectoryTemplateScanResult]

    def __init__(self):
        self.__scans = []

    @classmethod
    def get_instance(cls) -> Self:
        if not hasattr(cls, "_instance"):
            cls._instance = cls()  # type: ignore
        return cls._instance  # type: ignore

    def find(self, name: str) -> TemplateScanResult | None:
        for scan in self.__scans:
            for item in scan.items:
                if item.spec.name == name:
                    return item
        return None

    def load(self, directory: str) -> list[MorphFunctionLoadError]:
        project = load_project(directory)
        if project is not None:
            template_paths = project.template_paths
        else:
            template_paths = []

        result = import_files(directory, template_paths)
        self.__scans.append(result)
        return result.errors

    def dump(self) -> DirectoryTemplateScanResult:
        if len(self.__scans) == 0:
            raise ValueError("No files are loaded.")

        scan = self.__scans[-1]
        cache_items: list[TemplateScanResult] = []
        for scan_item in scan.items:
            item = TemplateScanResult(
                spec=scan_item.spec,
                file_path=scan_item.file_path,
                checksum=scan_item.checksum,
            )
            cache_items.append(item)

        cache = DirectoryTemplateScanResult(
            directory=scan.directory,
            directory_checksums=scan.directory_checksums,
            items=cache_items,
            errors=scan.errors,
        )
        dump_cache(cache)
        return cache
