import plotly.express as px

import morph
from morph import MorphGlobalContext


# morph.func is a decorator that takes in the following parameters:
# name: The identifier for the file alias. The function name will be used if not provided.
# description: The description for the function.
# output_paths: The destination paths for the output.
# output_type: The return type of the function
@morph.func(
    name="${MORPH_NAME}",
    description="${MORPH_DESCRIPTION}",
    output_paths=["_private/{name}/{now()}{ext()}"],
    output_type="visualization",
)
# morph.load_data is a decorator that takes in the following parameters:
# ${MORPH_PARENT_NAME}: The alias of another parent file. The function will be executed before the main function.
@morph.load_data("${MORPH_PARENT_NAME}")
def main(context: MorphGlobalContext) -> px.line:
    data = context.data["${MORPH_PARENT_NAME}"]
    # This is where you write your code.
    # The `px.line` function creates a line plot using Plotly Express.
    # The `update_layout` function updates the layout of the plot.
    fig = px.line(data, x="X Axis", y="Y Axis", markers=True)
    fig.update_layout(title="Plotly Plot")
    return fig
