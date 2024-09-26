import pandas as pd

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
    return pd.DataFrame({{"key1": [1, 2, 3], "key2": [3, 4, 5]}})
