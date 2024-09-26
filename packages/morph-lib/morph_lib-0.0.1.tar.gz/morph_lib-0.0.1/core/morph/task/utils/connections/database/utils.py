import sqlglot


def is_sql_returning_result(sql: str) -> bool:
    is_select = True
    try:
        parsed = sqlglot.parse_one(sql)
        is_select = parsed.key == "select"
    except Exception:  # noqa
        pass
    return is_select
