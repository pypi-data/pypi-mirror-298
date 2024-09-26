import click

log_format = click.option(
    "--log-format",
    envvar="MORPH_LOG_FORMAT",
    help="Specify the format of logging to the console and the log file. Use --log-format-file to configure the format for the log file differently than the console.",
    type=click.Choice(["text", "debug", "json", "default"], case_sensitive=False),
    default="default",
)


def require_canvas_if_dag(ctx, param, value):
    if ctx.params.get("dag") and not value:
        raise click.BadParameter("--canvas is required when --dag is specified.")
    return value


def parse_key_value(ctx, param, value):
    data_dict = {}
    for item in value:
        try:
            key, val = item.split("=", 1)
            data_dict[key] = val
        except ValueError:
            raise click.BadParameter(f"'{item}' is not a valid key=value pair")
    return data_dict


data = click.option(
    "-d",
    "--data",
    multiple=True,
    callback=parse_key_value,
    help="Key-value pairs in the form key=value",
)

run_id = click.option(
    "--run-id",
    "-c",
    help="Specify the run id.",
)

canvas = click.option(
    "--canvas",
    "-c",
    help="Specify the canvas name.",
    callback=require_canvas_if_dag,
)

dag = click.option(
    "--dag",
    is_flag=True,
    help="Run as a Directed Acyclic Graph (DAG).",
)

no_cache = click.option(
    "--no-cache",
    is_flag=True,
    help="Do not use the cache.",
)

is_debug = click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode.",
)

dry_run = click.option(
    "--dry-run",
    "-n",
    is_flag=True,
    help="Perform a dry run without executing the tasks.",
)

verbose = click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose mode.",
)

file = click.option(
    "--file",
    "-f",
    type=click.Path(exists=True),
    help="Specify the path to the resource.",
)

alias = click.option(
    "--alias",
    "-a",
    type=str,
    help="Specify the alias of the resource.",
)

all = click.option(
    "--all",
    is_flag=True,
    help="Select all resources.",
)

connection = click.option(
    "--connection",
    "-c",
    type=str,
    help="Specify the connection slug.",
)

output_paths = click.option(
    "--output-paths",
    "-o",
    type=click.Path(exists=False),
    multiple=True,
    help="Specify the output paths.",
)

parent_output_path = click.option(
    "--parent-output-path",
    "-po",
    multiple=True,
    callback=parse_key_value,
    help="Key-value pairs in the form key=value",
)

tmp = click.option(
    "--tmp",
    is_flag=True,
    help="Whether to save output to a temporary file.",
)

template = click.option(
    "--template",
    "-t",
    type=str,
    required=True,
    help="Specify the path or alias to the template.",
)
