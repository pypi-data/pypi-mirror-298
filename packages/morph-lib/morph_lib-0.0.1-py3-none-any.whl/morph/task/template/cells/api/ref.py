from typing import Dict

import pandas as pd
from morph_lib.annotations import morph
from morph_lib.api import ref

# The `data` variable prepares the data for processing in the main functions.
# For more information, please read the documentation at https://docs.morphdb.io/dbutils
data: Dict[str, pd.DataFrame] = {}


# The main function runs on the cloud when you click "Run".
# It's used by the data pipeline on the canvas to execute your Directed Acyclic Graph (DAG).
@morph.csv
def main(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    # This is where you write your code.
    print(ref("example_python_cell"))
    print(ref("execute_sql"))
    # print(ref("invalid"))
    return pd.DataFrame()
