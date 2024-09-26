import json
import sys
from pathlib import Path
from typing import List, Optional

import click
import pydantic

from morph.cli.flags import Flags
from morph.task.base import BaseTask
from morph.task.utils.morph import find_project_root_dir
from morph.task.utils.template.inspection import (
    DirectoryTemplateScanResult,
    MorphRegistryTemplateItem,
    MorphRegistryTemplateResponse,
)
from morph.task.utils.template.state import load_cache


class SearchTemplateTask(BaseTask):
    def __init__(self, args: Flags):
        super().__init__(args)
        self.args = args

    def run(self):
        try:
            project_root = find_project_root_dir()
        except FileNotFoundError as e:
            click.echo(click.style(str(e), fg="red"))
            raise e

        name: Optional[str] = self.args.NAME
        language: Optional[str] = self.args.LANGUAGE
        query: Optional[str] = self.args.QUERY
        limit: int = self.args.LIMIT
        skip: int = self.args.SKIP

        # Load user defined templates from cache
        try:
            cache = load_cache(project_root)
        except (pydantic.ValidationError, json.decoder.JSONDecodeError):
            click.echo(
                click.style(
                    "Warning: User defined template cache is corrupted. Please recompile the templates.",
                    fg="yellow",
                )
            )
            result = MorphRegistryTemplateResponse(templates=[], count=0)
            click.echo(result.model_dump_json(indent=2))
            sys.exit(0)

        if not cache:
            click.echo(
                click.style(
                    "Warning: No user defined template cache found in the project. Please compile the templates first.",
                    fg="yellow",
                )
            )
            result = MorphRegistryTemplateResponse(templates=[], count=0)
            click.echo(result.model_dump_json(indent=2))
            sys.exit(0)

        # Filter and paginate the filtered templates
        filtered_templates = filter_user_defined_templates(
            project_root, cache, name=name, language=language, query=query
        )
        total_count = len(filtered_templates)
        paginated_templates = filtered_templates[skip : skip + limit]

        result = MorphRegistryTemplateResponse(
            templates=paginated_templates,
            count=total_count,
        )
        click.echo(result.model_dump_json(indent=2))


def filter_user_defined_templates(
    project_root: str,
    cache: DirectoryTemplateScanResult,
    name: Optional[str] = None,
    language: Optional[str] = None,
    query: Optional[str] = None,
) -> List[MorphRegistryTemplateItem]:
    filtered_templates = []
    for item in cache.items:
        if name and item.spec.name != name:
            continue
        if language and item.spec.language != language:
            continue
        if query and not (
            query in item.spec.name
            or (item.spec.description and query in item.spec.description)
        ):
            continue

        filtered_templates.append(
            MorphRegistryTemplateItem(
                name=item.spec.name,
                title=item.spec.title,
                description=item.spec.description,
                code=Path(item.spec.src).read_text(),
                language=item.spec.language,
            )
        )

    return filtered_templates


def find_user_defined_template(
    project_root: str,
    cache: DirectoryTemplateScanResult,
    name: str,
) -> Optional[MorphRegistryTemplateItem]:
    for item in cache.items:
        if item.spec.name == name:
            return MorphRegistryTemplateItem(
                name=item.spec.name,
                title=item.spec.title,
                description=item.spec.description,
                code=Path(item.spec.src).read_text(),
                language=item.spec.language,
            )

    return None
