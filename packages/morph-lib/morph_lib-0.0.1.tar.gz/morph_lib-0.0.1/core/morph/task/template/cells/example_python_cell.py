import pandas as pd

import morph
from morph import MorphGlobalContext


# Morph decorators
# The `@morph.func` decorator required to be recognized as a function in morph.
# All paramerers are optional
# @param name: The alias of the file. If not provided, the function name will be used.
# @param description: The description of the function.
# @param output_paths: The file paths where the execution results will be saved.
# @param output_type: The type of the execution result. If no value is provided, it will be automatically estimated.
# The `@morph.load_data` decorator required to load data from parent file or function.
# the parent is executed before the current function and the data is passed to the current function as `context.data``.
# For more information: https://www.morphdb.io/docs
@morph.func(
    name="example_python_cell",
    description="Example Python cell",
    output_paths=["_private/{name}/{now()}{ext()}"],
    output_type="dataframe",
)
@morph.load_data("example_sql_cell")
def main(context: MorphGlobalContext) -> pd.DataFrame:
    # Load data from the previous cell
    sql_result_df = context.data["example_sql_cell"]
    return sql_result_df
