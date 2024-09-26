import json
import os.path
import re
import sys
from pathlib import Path
from typing import Optional

import click
import pydantic

from morph import MorphGlobalContext
from morph.cli.flags import Flags
from morph.task.base import BaseTask
from morph.task.utils.morph import find_project_root_dir
from morph.task.utils.template.inspection import (
    DirectoryTemplateScanResult,
    MorphTemplateLanguage,
)
from morph.task.utils.template.search import find_user_defined_template
from morph.task.utils.template.state import MorphTemplateManager, load_cache


def to_snake_case(text):
    text = re.sub("([A-Z]+)", r"_\1", text)
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    snake_case_text = (
        text.lower().strip("_").replace(" ", "_").replace("__", "_").replace("-", "_")
    )
    return snake_case_text


class CreateTask(BaseTask):
    def __init__(self, args: Flags, force: bool = False):
        super().__init__(args)
        self.args = args
        self.force = force

    def run(self):
        try:
            project_root = find_project_root_dir()
        except FileNotFoundError as e:
            click.echo(click.style(f"Error: {str(e)}", fg="red"))
            raise e

        filename: Path = (
            Path(self.args.FILENAME)
            if Path(self.args.FILENAME).is_absolute()
            else Path(project_root).joinpath(self.args.FILENAME)
        )
        template: Optional[str] = (
            to_snake_case(self.args.TEMPLATE) if self.args.TEMPLATE else None
        )
        name: str = (
            to_snake_case(self.args.NAME)
            if self.args.NAME
            else to_snake_case(filename.stem)
        )
        description: str = (
            self.args.DESCRIPTION or "Auto-generated via morph-cli template."
        )
        parent_name: Optional[str] = (
            to_snake_case(self.args.PARENT_NAME) if self.args.PARENT_NAME else None
        )
        connection: Optional[str] = self.args.CONNECTION

        # Validate filename
        if filename.is_file():
            click.echo(
                click.style(
                    f'Error: specified file "{filename.as_posix()}" already exists.',
                    fg="red",
                )
            )
            sys.exit(1)

        # Retrieve template code
        language: MorphTemplateLanguage = MorphTemplateLanguage.PYTHON
        ext = "".join(filename.suffixes)
        if ext == ".py":
            language = MorphTemplateLanguage.PYTHON
            if not template:
                template = (
                    "transform_cell_result"
                    if parent_name
                    else "python_starter_template"
                )
        elif ext == ".sql":
            language = MorphTemplateLanguage.SQL
            template = template or "sql_starter_template"
        elif ext == ".vg.json":
            language = MorphTemplateLanguage.JSON
            click.echo(
                click.style(
                    f'Warning: template option is ignored for "*{ext}" files.',
                    fg="red",
                )
            )
            template = "vg_json_template"

        template_code = ""
        if template:
            if Path(template).is_file():
                local_template = (
                    Path(template)
                    if Path(template).is_absolute()
                    else Path(project_root) / template
                )
                if not local_template.exists():
                    click.echo(
                        click.style(
                            f'Error: specified local template "{local_template.as_posix()}" does not exist.',
                            fg="red",
                        )
                    )
                    sys.exit(1)
                template_code = local_template.read_text()
            else:
                # Search user defined local template -> morph-cli global template
                cache: Optional[DirectoryTemplateScanResult] = None
                try:
                    cache = load_cache(project_root)
                except (pydantic.ValidationError, json.decoder.JSONDecodeError):
                    click.echo(
                        click.style(
                            "Warning: User defined template cache is corrupted. Please recompile the templates.",
                            fg="yellow",
                        )
                    )

                if not cache:
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
                        sys.exit(1)  # General errors

                user_defined_template = (
                    find_user_defined_template(project_root, cache, template)
                    if cache
                    else None
                )
                user_defined_code = (
                    user_defined_template.code if user_defined_template else None
                )

                global_template_path = Path(os.path.dirname(__file__)).joinpath(
                    f"utils/template/scaffold/{language.value}/{template}{ext}"
                )
                global_code = (
                    global_template_path.read_text()
                    if global_template_path.exists()
                    else None
                )

                if user_defined_code and global_code:
                    click.echo(
                        click.style(
                            f'Warning: specified template "{template}" appears in both user defined and global templates. Using user defined template.',
                        )
                    )
                    template_code = user_defined_code
                elif user_defined_code:
                    template_code = user_defined_code
                elif global_code:
                    template_code = global_code
                else:
                    click.echo(
                        click.style(
                            f'Error: specified template "{template}" does not exist in user defined nor global templates.',
                            fg="red",
                        )
                    )
                    sys.exit(2)  # 2: Misuse of shell builtins

        # Replace placeholders in template code according to other arguments
        # - name: ${MORPH_NAME} and "def main("
        template_code = template_code.replace("${MORPH_NAME}", name)
        template_code = template_code.replace("def main(", f"def {name}(")
        # - description: ${MORPH_DESCRIPTION}
        template_code = template_code.replace("${MORPH_DESCRIPTION}", description)
        # - parent_name: ${MORPH_PARENT_NAME}
        template_code = template_code.replace("${MORPH_PARENT_NAME}", parent_name or "")
        # - connection: ${MORPH_CONNECTION}
        if connection:
            template_code = template_code.replace("${MORPH_CONNECTION}", connection)
        else:
            template_code = template_code.replace(
                'connection_slug="${MORPH_CONNECTION}"', "connection_slug=None"
            )

        # Write the template code to the file
        with open(filename.as_posix(), "w") as f:
            f.write(template_code)

        # Compile the project
        context = MorphGlobalContext.get_instance()
        errors = context.load(project_root)
        if len(errors) > 0:
            for error in errors:
                click.echo(
                    click.style(
                        f"""Error occurred in {error.file_path}:{error.name} [{error.category}] {error.error}""",
                        fg="red",
                    )
                )
            click.echo(
                click.style(
                    "Error: Please check your options and try again.",
                    fg="red",
                    bg="yellow",
                )
            )
            os.remove(filename.as_posix())
        else:
            context.dump()
