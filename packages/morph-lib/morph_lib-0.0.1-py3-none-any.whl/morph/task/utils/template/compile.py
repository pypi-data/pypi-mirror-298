import json
from enum import Enum
from pathlib import Path
from typing import Any

import click
import pydantic
from pydantic import BaseModel

from morph.cli.flags import Flags
from morph.config.project import load_project
from morph.task.base import BaseTask
from morph.task.utils.morph import find_project_root_dir
from morph.task.utils.run_backend.errors import MorphFunctionLoadError
from morph.task.utils.template.inspection import get_checksum
from morph.task.utils.template.state import MorphTemplateManager, load_cache


class CompileTemplateTask(BaseTask):
    def __init__(self, args: Flags, force: bool = False):
        super().__init__(args)
        self.args = args
        self.force = force

    def run(self):
        try:
            project_root = find_project_root_dir()
        except FileNotFoundError as e:
            click.echo(click.style(str(e), fg="red"))
            raise e

        try:
            cache = load_cache(project_root)
        except (pydantic.ValidationError, json.decoder.JSONDecodeError):
            click.echo(
                click.style(
                    "Warning: Morph-cli template cache is corrupted. Recompiling...",
                    fg="yellow",
                )
            )
            cache = None

        if cache is None:
            needs_compile = True
        elif len(cache.errors) > 0:
            needs_compile = True
        else:
            needs_compile = False
            project = load_project(project_root)
            if project is not None:
                template_paths = project.template_paths
            else:
                template_paths = []

            compare_dirs = []
            if len(template_paths) == 0:
                compare_dirs.append(Path(project_root))
            else:
                for template_path in template_paths:
                    compare_dirs.append(Path(f"{project_root}/{template_path}"))

            for compare_dir in compare_dirs:
                if cache.directory_checksums.get(
                    compare_dir.as_posix(), ""
                ) != get_checksum(Path(compare_dir)):
                    needs_compile = True
                    break

        if self.force:
            needs_compile = True

        if needs_compile:
            manager = MorphTemplateManager.get_instance()
            errors = manager.load(project_root)
            manager.dump()

            if len(errors) > 0:
                click.echo(
                    click.style(
                        "Error: Failed to load user defined template.", fg="red"
                    )
                )
                for error in errors:
                    click.echo(
                        click.style(
                            f"""Error occurred in {error.file_path}:{error.name} [{error.category}] {error.error}""",
                            fg="red",
                            bg="yellow",
                        )
                    )

        if self.args.VERBOSE:

            def serialize(obj: Any) -> Any:
                if isinstance(obj, BaseModel):
                    return obj.model_dump()
                elif isinstance(obj, Enum):
                    return obj.value
                elif isinstance(obj, MorphFunctionLoadError):
                    return {
                        "category": obj.category.value,
                        "file_path": obj.file_path,
                        "name": obj.name,
                        "error": obj.error,
                    }
                return str(obj)

            info: dict = {
                "needs_compile": needs_compile,
            }
            if needs_compile:
                info["errors"] = [serialize(error) for error in errors]
            elif cache is not None:
                info["errors"] = [serialize(error) for error in cache.errors]

            click.echo(json.dumps(info, indent=2))
