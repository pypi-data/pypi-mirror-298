from estecopy._internal.utils import connection
from estecopy._utils.arg_parse import ensure_correct_args


def get_xml_layout():
    return connection.get("/charts/xml-layout")


def create_charts_from_xml(xml_string):
    ensure_correct_args(("xml_string", "string", xml_string))
    return connection.post_json("/charts/from-xml",
                                json={"xml": xml_string})


def create_chart_from_table(chart_name, table_name, xml_string):
    ensure_correct_args(("chart_name", "string", chart_name),
                        ("table_name", "string", table_name),
                        ("xml_string", "?string", xml_string))
    return connection.post("/charts/from-table",
                           json={"chart": chart_name,
                                 "table": table_name,
                                 "xml": xml_string})


def create_chart_from_table_and_single_variable(chart_name, table_name, variable, xml_string):
    ensure_correct_args(("chart_name", "string", chart_name),
                        ("table_name", "string", table_name),
                        ("variable", "string", variable),
                        ("xml_string", "?string", xml_string))
    return connection.post("/charts/from-table-and-variable",
                           json={"chart": chart_name,
                                 "table": table_name,
                                 "variable": variable,
                                 "xml": xml_string})


def create_chart_from_rsm(chart_name, rsm_names, xml_string):
    ensure_correct_args(("chart_name", "string", chart_name),
                        ("rsm_names", "[string]", rsm_names),
                        ("xml_string", "?string", xml_string))
    return connection.post("/charts/from-rsm-list",
                           json={"chart": chart_name,
                                 "rsm_list": rsm_names,
                                 "xml": xml_string})


def create_chart_from_table_and_variables(chart_name, table_name, var_names, xml_string):
    ensure_correct_args(("chart_name", "string", chart_name),
                        ("table_name", "string", table_name),
                        ("var_names", "[string]", var_names),
                        ("xml_string", "?string", xml_string))
    return connection.post("/charts/from-table-and-variable-list",
                           json={"chart": chart_name,
                                 "table": table_name,
                                 "variables": var_names,
                                 "xml": xml_string})


def create_multi_history_on_two_tables(table_name, var_names, second_table_name, second_table_var_names, xml_string):
    ensure_correct_args(("table_name", "string", table_name),
                        ("var_names", "[string]", var_names),
                        ("second_table_name", "string", second_table_name),
                        ("second_table_var_names", "[string]", second_table_var_names),
                        ("xml_string", "?string", xml_string))
    return connection.post("/charts/multi-history-on-two-tables",
                           json={"table": table_name,
                                 "variables": var_names,
                                 "other_table": second_table_name,
                                 "other_variables": second_table_var_names,
                                 "xml": xml_string})


def create_chart_from_rsm_and_table(chart_name, rsm_names, table_name, xml_string):
    ensure_correct_args(("chart_name", "string", chart_name),
                        ("rsm_names", "[string]", rsm_names),
                        ("table_name", "?string", table_name),
                        ("xml_string", "?string", xml_string))
    json = {"chart": chart_name,
            "rsm_list": rsm_names,
            "table": table_name,
            "xml": xml_string}
    return connection.post("/charts/from-rsm-list-and-table",
                           json=json)


def create_chart_from_rsm_and_variables(chart_name, rsm_names, variable_names, xml_string):
    ensure_correct_args(("chart_name", "string", chart_name),
                        ("rsm_names", "[string]", rsm_names),
                        ("variable_names", "[string]", variable_names),
                        ("xml_string", "?string", xml_string))
    return connection.post("/charts/from-rsm-list-and-variable-list",
                           json={"chart": chart_name,
                                 "rsm_list": rsm_names,
                                 "variables": variable_names,
                                 "xml": xml_string})
