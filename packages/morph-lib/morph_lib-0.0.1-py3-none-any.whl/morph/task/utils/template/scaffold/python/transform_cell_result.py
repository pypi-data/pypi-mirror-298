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
# morph.load_data is a decorator that takes in the following parameters:
# ${MORPH_PARENT_NAME}: The alias of another parent file. The function will be executed before the main function.
@morph.load_data("${MORPH_PARENT_NAME}")
def main(context: MorphGlobalContext) -> pd.DataFrame:
    # This is where you write your code.
    data = context.data["${MORPH_PARENT_NAME}"]
    return pd.DataFrame(data)
