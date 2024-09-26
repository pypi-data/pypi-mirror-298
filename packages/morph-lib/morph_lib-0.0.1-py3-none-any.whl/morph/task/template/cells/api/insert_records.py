from typing import Dict, Optional

import pandas as pd
from morph_lib.annotations import morph
from morph_lib.api import create_table, execute_sql, insert_records, load_data, ref

# The `data` variable prepares the data for processing in the main functions.
# For more information, please read the documentation at https://docs.morphdb.io/dbutils
data: Dict[str, Optional[pd.DataFrame]] = {
    "example": load_data(ref("example_python_cell"))
}


# The main function runs on the cloud when you click "Run".
# It's used by the data pipeline on the canvas to execute your Directed Acyclic Graph (DAG).
@morph.csv
def main(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    # This is where you write your code.
    df = pd.DataFrame(
        {
            "Name": ["John Doe", "Jane Smith", "Emily Zhang"],
            "Age": [28, 34, 22],
            "Occupation": ["Software Engineer", "Data Scientist", "Marketing Manager"],
        }
    )
    print("====================================")
    print('execute_sql("DROP TABLE IF EXISTS test_table;")')
    execute_sql("DROP TABLE IF EXISTS test_table;")

    print("====================================")
    print('create_table(df, table_name="test_table")')
    create_table(df, table_name="test_table")

    print("====================================")
    insert_df = pd.DataFrame(
        {
            "Name": ["oginokairan"],
            "Age": [32],
            "Occupation": ["Software Engineer"],
        }
    )
    insert_records(insert_df, table_name="test_table")

    print("====================================")
    print('execute_sql("SELECT * FROM test_table;")')
    result: pd.DataFrame = execute_sql("SELECT * FROM test_table;")
    print(result)

    return result
