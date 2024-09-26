import duckdb
from jinja2 import Environment

context = {}


def config(**kwargs):
    global context
    context.update(kwargs)
    return ""


sql_template = """{{
config(
    name="get_users",
    description="get user list",
    columns=[{
        "name": "column_name1",
        "description": "description of column 1"
    },{
        "name": "column_name2",
        "description": "description of column 2"
    }]
)
}}
select
    *
from
    '~/Desktop/salesforce_records.csv'
limit
    {{ limit }};
;
"""

env = Environment()
env.globals["config"] = config

template = env.from_string(sql_template)
sql = template.render(limit=10)
print(f"Context: \n{context}\n")
print(f"SQL: \n{sql}\n")

df = duckdb.sql(sql)
print(df)
