from typing import Dict, Optional

import pandas as pd
from morph_lib.api import load_data

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
def main(context: MorphGlobalContext) -> Optional[pd.DataFrame]:
    # The `data` variable prepares the data for processing in the main functions.
    # For more information, please read the documentation at https://www.morphdb.io/docs
    # The `load_data` function loads the data from the specified cell and returns the result as a pandas dataframe.
    data: Dict[str, Optional[pd.DataFrame]] = {
        "csv_cell": load_data(
            {"type": "file", "filepath": "path/to/file.csv"}  # type: ignore
        )  # replace `path/to/file.csv` with the path to your file
    }
    return data["csv_cell"]
