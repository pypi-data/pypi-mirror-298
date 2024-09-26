import hashlib
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

import yaml
from pydantic import BaseModel, Field
from pydantic_core import ValidationError

from morph.task.utils.run_backend.errors import (
    MorphFunctionLoadError,
    MorphFunctionLoadErrorCategory,
)


class MorphTemplateLanguage(str, Enum):
    PYTHON = "python"
    SQL = "sql"
    JSON = "json"


class MorphTemplateBase(BaseModel):
    name: str = Field(..., description="Template name")
    title: Optional[str] = Field(..., description="Template title")
    description: Optional[str] = Field(..., description="Description of the template")
    language: MorphTemplateLanguage = Field(..., description="Language of the template")


class MorphTemplateMetaObject(MorphTemplateBase):
    id: str = Field(..., description="Template ID")
    src: str = Field(..., description="Template file path")


class MorphRegistryTemplateItem(MorphTemplateBase):
    code: str = Field(..., description="Template code")


class MorphRegistryTemplateResponse(BaseModel):
    templates: list[MorphRegistryTemplateItem]
    count: int


class TemplateScanResult(BaseModel):
    spec: MorphTemplateMetaObject
    file_path: str
    checksum: str


class DirectoryTemplateScanResult(BaseModel):
    directory: str
    directory_checksums: Dict[str, str]
    items: List[TemplateScanResult]
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
            # NOTE: Check all files to avoid caching compile errors when a new file is created.
            # if file.is_file() and (file.suffix == ".yml" or file.suffix == ".yaml"):
            if file.is_file():
                with open(str(file), "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_func.update(chunk)

        return hash_func.hexdigest()
    else:
        raise ValueError(f"Path {path} is not a file or directory.")


def _import_template_file(
    file_path: Path,
) -> tuple[List[TemplateScanResult], List[MorphFunctionLoadError]]:
    """import a template file."""
    with open(file_path, "r") as f:
        yaml_data = yaml.load(f, Loader=yaml.FullLoader)
        if not yaml_data or "templates" not in yaml_data:
            return [], [
                MorphFunctionLoadError(
                    category=MorphFunctionLoadErrorCategory.INVALID_SYNTAX,
                    file_path=file_path.as_posix(),
                    name="",
                    error="templates is not found in the file.",
                )
            ]
        results: list[TemplateScanResult] = []
        errors: list[MorphFunctionLoadError] = []

        for template in yaml_data["templates"] or []:
            try:
                src = template.get("src")
                template_file = (
                    Path(src)
                    if Path(src).is_absolute()
                    else file_path.parent / Path(src)
                )

                meta = MorphTemplateMetaObject(
                    id=f"{file_path}:{template['name']}",
                    name=template.get("name"),
                    title=template.get("title"),
                    description=template.get("description"),
                    src=template_file.as_posix(),
                    language=MorphTemplateLanguage(template.get("language")),
                )

                if not template_file.exists():
                    errors.append(
                        MorphFunctionLoadError(
                            category=MorphFunctionLoadErrorCategory.INVALID_SYNTAX,
                            file_path=file_path.as_posix(),
                            name=meta.name,
                            error=f"Template file {template_file} is not found.",
                        )
                    )
                    continue

                results.append(
                    TemplateScanResult(
                        spec=meta,
                        file_path=file_path.as_posix(),
                        checksum=get_checksum(template_file),
                    )
                )
            except ValidationError as e:
                for error in e.errors():
                    for loc in error.get("loc") or []:
                        errors.append(
                            MorphFunctionLoadError(
                                category=MorphFunctionLoadErrorCategory.INVALID_SYNTAX,
                                file_path=file_path.as_posix(),
                                name=str(loc),
                                error=str(error.get("msg")),
                            )
                        )
            except ValueError as e:
                errors.append(
                    MorphFunctionLoadError(
                        category=MorphFunctionLoadErrorCategory.INVALID_SYNTAX,
                        file_path=file_path.as_posix(),
                        name="",
                        error=str(e),
                    )
                )
        return results, errors


def import_files(
    directory: str, template_paths: List[str]
) -> DirectoryTemplateScanResult:
    """import template files."""
    p = Path(directory)
    results: list[TemplateScanResult] = []
    errors: list[MorphFunctionLoadError] = []
    # ignore_dirs = [".local", ".git", ".venv", "__pycache__"]

    search_paths: list[Path] = []
    if len(template_paths) == 0:
        search_paths.append(p)
    else:
        for template_path in template_paths:
            search_paths.append(p / template_path)

    directory_checksums: dict[str, str] = {}
    for search_path in search_paths:
        file_path: Optional[Path] = None
        for f in search_path.glob("*.yml"):
            file_path = f
            break
        for f in search_path.glob("*.yaml"):
            file_path = f
            break
        if file_path is None:
            continue

        scan_results, scan_errors = _import_template_file(file_path)
        if scan_results is not None:
            results.extend(scan_results)
        if scan_errors is not None:
            errors.extend(scan_errors)

        directory_checksums[search_path.as_posix()] = get_checksum(search_path)

    return DirectoryTemplateScanResult(
        directory=directory,
        directory_checksums=directory_checksums,
        items=results,
        errors=errors,
    )
