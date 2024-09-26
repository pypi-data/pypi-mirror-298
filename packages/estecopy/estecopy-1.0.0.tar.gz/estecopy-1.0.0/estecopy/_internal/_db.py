from estecopy._internal.utils import connection
from estecopy._utils.arg_parse import ensure_correct_args


def get_table_types():
    return ("all",)


def get_table_names(unused_type):
    return tuple(connection.get_json("/db/tables"))


def create_table(table_name, spec):
    ensure_correct_args(("table_name", "!string", table_name))
    return connection.post_json("/db/tables/{table name}",
                                parameters={"table name": table_name},
                                json=spec)


def supply_table_rows(table_name, append_row_f):
    ensure_correct_args(("table_name", "!string", table_name))
    rows = get_table_rows(table_name)
    for row in rows:
        append_row_f(len(rows), row)


def __get_table_content(table_name, content_type):
    return connection.get_json("/db/tables/{table name}",
                               parameters={"table name": table_name},
                               query_parameters={"content-type": content_type})


def get_table_metadata(table_name):
    ensure_correct_args(("table_name", "!string", table_name))
    return __get_table_content(table_name, "metadata")


def get_table_data(table_name):
    ensure_correct_args(("table_name", "!string", table_name))
    return __get_table_content(table_name, "data")


def get_table_rows(table_name):
    ensure_correct_args(("table_name", "!string", table_name))
    return __get_table_content(table_name, "rows")
