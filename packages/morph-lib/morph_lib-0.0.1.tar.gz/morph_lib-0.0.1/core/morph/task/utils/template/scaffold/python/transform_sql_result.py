from typing import Dict

import pandas as pd
from morph_lib.api import execute_sql

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
    output_type="dataframe",
)
def main(context: MorphGlobalContext) -> pd.DataFrame:
    # This is where you write your code.
    # The `execute_sql` function executes the specified SQL query and returns the result as a pandas dataframe.
    data: Dict[str, pd.DataFrame] = {"sql_cell": execute_sql("SELECT 1 as test")}
    return pd.DataFrame(data["sql_cell"])
