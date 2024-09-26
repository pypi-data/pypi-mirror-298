# type: ignore

from __future__ import annotations

import functools
from typing import Callable, Dict, Tuple, Union

import click

from morph.cli import params, requires


def global_flags(
    func: Callable[..., Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]]
) -> Callable[..., Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]]:
    @params.log_format
    @functools.wraps(func)
    def wrapper(
        *args: Tuple[Union[Dict[str, Union[str, int, bool]], None], bool],
        **kwargs: Dict[str, Union[str, int, bool]],
    ) -> Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]:
        return func(*args, **kwargs)

    return wrapper


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
    no_args_is_help=True,
    epilog="Specify one of these sub-commands and you can find more help from there.",
)
@click.pass_context
@global_flags
def cli(ctx: click.Context, **kwargs: Dict[str, Union[str, int, bool]]) -> None:
    """An data analysis tool for transformations, visualization by using SQL and Python.
    For more information on these commands, visit: docs.morphdb.io
    """


@cli.command("init")
@click.pass_context
@global_flags
@requires.preflight
@requires.postflight
def init(
    ctx: click.Context, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]:
    """Initialize credentials to run morph project."""
    from morph.task.init import InitTask

    task = InitTask(ctx.obj["flags"])
    results = task.run()
    return results, True


@cli.command("new")
@click.argument("directory_name", required=True)
@click.pass_context
@global_flags
@requires.preflight
@requires.postflight
def new(
    ctx: click.Context, directory_name: str, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]:
    """Create a new morph project."""
    from morph.task.new import NewTask

    task = NewTask(ctx.obj["flags"], directory_name)
    results = task.run()
    return results, True


@cli.command("compile")
@click.option("--force", "-f", is_flag=True, help="Force compile.")
@click.pass_context
@global_flags
@params.verbose
@requires.preflight
@requires.postflight
def compile(
    ctx: click.Context, force: bool, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[None, bool]:
    """Analyse morph functions into indexable objects."""
    from morph.task.compile import CompileTask

    task = CompileTask(ctx.obj["flags"], force=force)
    task.run()
    return None, True


@cli.command("run")
@click.argument("filename", required=True)
@click.pass_context
@global_flags
@params.data
@params.run_id
@params.canvas
@params.dag
@params.dry_run
@params.is_debug
@params.no_cache
@params.connection
@params.output_paths
@params.parent_output_path
@params.tmp
@requires.preflight
@requires.postflight
def run(
    ctx: click.Context, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]:
    """Run sql and python file and bring the results in output file."""
    from morph.task.run import RunTask

    task = RunTask(ctx.obj["flags"])
    results = task.run()
    return results, True


@cli.command("print")
@click.pass_context
@global_flags
@params.file
@params.alias
@params.all
@params.verbose
@requires.preflight
@requires.postflight
def print_resource(
    ctx: click.Context, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]:
    """Print details for the specified resource by path or alias."""
    from morph.task.resource import PrintResourceTask

    task = PrintResourceTask(ctx.obj["flags"])
    results = task.run()
    return results, True


@cli.group("knowledge")
@click.pass_context
@global_flags
def knowledge(ctx: click.Context, **kwargs: Dict[str, Union[str, int, bool]]) -> None:
    """Manage knowledge.
    Knowledge is a collection of data that is used to store information about data schemas.
    It improves the performance of Morph AI and help your teams understand the data.
    """


@knowledge.command("compile")
@click.option("--force", "-f", is_flag=True, help="Force compile.")
@click.pass_context
@global_flags
@params.verbose
@requires.preflight
@requires.postflight
def compile_knowledge(
    ctx: click.Context, force: bool, **kwargs: Dict[str, Union[str, int, bool]]
) -> None:
    """Compile knowledge."""
    from morph.task.compile import CompileTask
    from morph.task.utils.knowledge.compile import CompileKnowledgeTask

    src_compile_task = CompileTask(ctx.obj["flags"], force=force)
    src_compile_task.run()

    task = CompileKnowledgeTask(ctx.obj["flags"], force=force)
    task.run()
    return None, True


@knowledge.command("find")
@click.option("--select-source", "-s", is_flag=True, help="Select source.")
@click.option("--connection", "-c", required=False, default=None)
@click.option("--type", "-c", required=False, default="datasource")
@click.argument("knowledge_name", required=True)
@click.pass_context
@global_flags
@params.no_cache
@params.verbose
@requires.preflight
@requires.postflight
def find_knowledge(
    ctx: click.Context,
    select_source: bool,
    connection: str | None,
    type: str,
    **kwargs: Dict[str, Union[str, int, bool]],
) -> Tuple[Union[Dict[str, Union[str, int, bool]], None], bool]:
    """Find a knowledge."""
    from morph.task.compile import CompileTask
    from morph.task.utils.knowledge.find import FindKnowledgeTask

    src_compile_task = CompileTask(ctx.obj["flags"])
    src_compile_task.run()

    task = FindKnowledgeTask(
        ctx.obj["flags"], select_source=select_source, connection=connection, type=type
    )
    results = task.run()
    return results, True


@cli.group("template")
@click.pass_context
@global_flags
@params.verbose
@requires.preflight
@requires.postflight
def template(
    ctx: click.Context, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[None, bool]:
    """Manage templates.
    Templates are used to create new morph canvas cells.
    """
    return None, True


@template.command("compile")
@click.option("--force", "-f", is_flag=True, help="Force compile.")
@click.pass_context
@global_flags
@params.verbose
@requires.preflight
@requires.postflight
def template_compile(
    ctx: click.Context, force: bool, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[None, bool]:
    """Compile templates."""
    from morph.task.utils.template.compile import CompileTemplateTask

    task = CompileTemplateTask(ctx.obj["flags"], force=force)
    task.run()
    return None, True


@template.command("search")
@click.option("--name", type=str, help="Specify the local template name.")
@click.option("--language", type=str, help="Specify the local template language.")
@click.option("--query", type=str, help="Specify the search query.")
@click.option("--limit", type=int, default=20, help="Specify the limit. [default: 20]")
@click.option("--skip", type=int, default=0, help="Specify the skip. [default: 0]")
@click.pass_context
@global_flags
@params.verbose
@requires.preflight
@requires.postflight
def template_search(
    ctx: click.Context, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[None, bool]:
    """Search templates."""
    from morph.task.utils.template.search import SearchTemplateTask

    task = SearchTemplateTask(ctx.obj["flags"])
    task.run()
    return None, True


@cli.command("create")
@click.argument("filename", required=True)
@click.option("--template", type=str, help="Specify the template name.")
@click.option("--name", type=str, help="Specify the function name.")
@click.option("--description", type=str, help="Specify the function description.")
@click.option("--parent-name", type=str, help="Specify the parent function name.")
@click.option("--connection", type=str, help="Specify the connection name.")
@params.verbose
@click.pass_context
@global_flags
@requires.preflight
@requires.postflight
def create(
    ctx: click.Context, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[None, bool]:
    """Morph-cli create command."""
    from morph.task.create import CreateTask

    task = CreateTask(ctx.obj["flags"])
    task.run()

    return None, True


@cli.command("clean")
@params.verbose
@click.pass_context
@global_flags
@requires.preflight
@requires.postflight
def clean(
    ctx: click.Context, **kwargs: Dict[str, Union[str, int, bool]]
) -> Tuple[None, bool]:
    """Clean all the cache and garbage in Morph project."""
    from morph.task.clean import CleanTask

    task = CleanTask(ctx.obj["flags"])
    task.run()

    return None, True
