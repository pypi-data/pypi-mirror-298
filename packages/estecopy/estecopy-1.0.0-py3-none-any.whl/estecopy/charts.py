from estecopy._internal import _charts
from estecopy._utils.arg_parse import ensure_correct_args, get_as_list

def create_parallel_coordinates(table_name, var_names, xml_file=None, xml_string=None):
    """Creates a Parallel coordinates chart on the specified table with the specified variables in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    var_names:
        list of variables you want to plot in string format.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("var_names", "[string]", var_names),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    var_names = get_as_list(var_names, "Second argument has to be a list of distinct variable names")
    return _charts.create_chart_from_table_and_variables("PARALLEL_COORDINATES", table_name, var_names, __get_xml_as_string(xml_file, xml_string))


def create_multi_history(table_name, var_names, second_table_name=None, second_table_var_names=None, xml_file=None, xml_string=None):
    """Creates a Multi-history chart on one or more specified tables with the specified variables in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    var_names:
        list of variables you want to plot in string format.
    second_table_name:
        name of the second table with the data you want to plot (optional).
    second_table_var_names:
        names of variables from the second table you want to plot in string format (optional).
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("var_names", "[string]", var_names),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    var_names = get_as_list(var_names, "Second argument has to be a list of distinct variable names")
    if second_table_name is None or second_table_var_names is None:
        ensure_correct_args(("second_table_name", "?!string", second_table_name),
                            ("second_table_var_names", "?[string]", second_table_var_names))
        return _charts.create_chart_from_table_and_variables("MULTI_HISTORY", table_name, var_names, __get_xml_as_string(xml_file, xml_string))
    else:
        ensure_correct_args(("second_table_name", "!string", second_table_name),
                            ("second_table_var_names", "[string]", second_table_var_names))
        second_table_var_names = get_as_list(second_table_var_names, "second_table_var_names has to be a list of distinct variable names")
        return _charts.create_multi_history_on_two_tables(table_name, var_names, second_table_name, second_table_var_names, __get_xml_as_string(xml_file, xml_string))


def create_multi_history_3D(table_name, var_names, xml_file=None, xml_string=None):
    """Creates a Multi-history 3D chart on the specified table with the specified variables in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    var_names:
        list of variables you want to plot in string format.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("var_names", "[string]", var_names),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    var_names = get_as_list(var_names, "Second argument has to be a list of distinct variable names")
    return _charts.create_chart_from_table_and_variables("MULTI_HISTORY_3D", table_name, var_names, __get_xml_as_string(xml_file, xml_string))


def create_multi_vector(table_name, vector_names, xml_file=None, xml_string=None):
    """Creates a Multi-vector chart on the specified table with the specified vectors in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    vector_names:
        list of vectors you want to plot in string format. The vectors must have the same dimension.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("vector_names", "[string]", vector_names),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    if len(set(vector_names)) != len(vector_names):
        raise ValueError("Second argument has to be a list of distinct vectors names")
    vector_names = get_as_list(vector_names, "Second argument has to be a list of distinct vectors names")
    return _charts.create_chart_from_table_and_variables("MULTI_VECTOR", table_name, vector_names, __get_xml_as_string(xml_file, xml_string))


def create_scatter(table_name, var_names, xml_file=None, xml_string=None):
    """Creates a Scatter chart on the specified table with the specified variables in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    var_names:
        list of variables you want to plot in string format.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("var_names", "[string]", var_names),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    var_names = get_as_list(var_names, "Second argument has to be a list of distinct variable names")
    return _charts.create_chart_from_table_and_variables("SCATTER", table_name, var_names, __get_xml_as_string(xml_file, xml_string))


def create_scatter_3D(table_name, var_names, xml_file=None, xml_string=None):
    """Creates a Scatter 3D chart on the specified table with the specified variables in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    var_names:
        list of variables you want to plot in string format.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("var_names", "[string]", var_names),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    var_names = get_as_list(var_names, "Second argument has to be a list of distinct variable names")
    return _charts.create_chart_from_table_and_variables("SCATTER_3D", table_name, var_names, __get_xml_as_string(xml_file, xml_string))


def create_bubble(table_name, var_names, xml_file=None, xml_string=None):
    """Creates a Bubble chart on the specified table with the specified variables in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    var_names:
        list of variables you want to plot in string format.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("var_names", "[string]", var_names),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    var_names = get_as_list(var_names, "Second argument has to be a list of distinct variable names")
    return _charts.create_chart_from_table_and_variables("BUBBLE", table_name, var_names, __get_xml_as_string(xml_file, xml_string))


def create_bubble_4D(table_name, var_names, xml_file=None, xml_string=None):
    """Creates a Bubble 4D chart on the specified table with the specified variables in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    var_names:
        list of variables you want to plot in string format.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("var_names", "[string]", var_names),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    var_names = get_as_list(var_names, "Second argument has to be a list of distinct variable names")
    return _charts.create_chart_from_table_and_variables("BUBBLE_4D", table_name, var_names, __get_xml_as_string(xml_file, xml_string))


def create_design_distribution(table_name, var_names, xml_file=None, xml_string=None):
    """Creates a Design distribution chart on the specified table with the specified variables in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    var_names:
        list of variables you want to plot in string format.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("var_names", "[string]", var_names),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    var_names = get_as_list(var_names, "Second argument has to be a list of distinct variable names")
    return _charts.create_chart_from_table_and_variables("DESIGN_DISTRIBUTION", table_name, var_names, __get_xml_as_string(xml_file, xml_string))


def create_broken_constraints(table_name, constraints, xml_file=None, xml_string=None):
    """Creates a Broken constraints chart on the specified table with the specified constraints in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    constraints:
        list of constraints you want to plot in string format.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("constraints", "[string]", constraints),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    constraints = get_as_list(constraints, "Second argument has to be a list of distinct constraints names")
    return _charts.create_chart_from_table_and_variables("BROKEN_CONSTRAINTS", table_name, constraints, __get_xml_as_string(xml_file, xml_string))


def create_box_whiskers(table_name, var_names, xml_file=None, xml_string=None):
    """Creates a Box whiskers chart on the specified table with the specified variables in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    var_names:
        list of variables you want to plot in string format.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("var_names", "[string]", var_names),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    var_names = get_as_list(var_names, "Second argument has to be a list of distinct variable names")
    return _charts.create_chart_from_table_and_variables("BOX_WHISKERS", table_name, var_names, __get_xml_as_string(xml_file, xml_string))


def create_history(table_name, variable, xml_file=None, xml_string=None):
    """Creates an History chart on the specified table with the specified variable in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    variable:
        variable you want to plot in string format.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("variable", "!string", variable),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    return _charts.create_chart_from_table_and_single_variable("HISTORY", table_name, variable, __get_xml_as_string(xml_file, xml_string))


def create_PDF(table_name, variable, xml_file=None, xml_string=None):
    """Creates a PDF chart on the specified table with the specified variable in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    variable:
        variable you want to plot in string format.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("variable", "!string", variable),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))    
    return _charts.create_chart_from_table_and_single_variable("PDF", table_name, variable, __get_xml_as_string(xml_file, xml_string))


def create_CDF(table_name, variable, xml_file=None, xml_string=None):
    """Creates a CDF chart on the specified table with the specified variable in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    variable:
        variable you want to plot in string format.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("variable", "!string", variable),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))    
    return _charts.create_chart_from_table_and_single_variable("CDF", table_name, variable, __get_xml_as_string(xml_file, xml_string))


def create_normal_quantile(table_name, variable, xml_file=None, xml_string=None):
    """Creates a Normal-quantile plot on the specified table with the specified variable in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    variable:
        variable you want to plot in string format.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("variable", "!string", variable),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))    
    return _charts.create_chart_from_table_and_single_variable("NORMAL_QUANTILE", table_name, variable, __get_xml_as_string(xml_file, xml_string))


def create_distribution_fitting(table_name, variable, xml_file=None, xml_string=None):
    """Creates a Distribution fitting chart on the specified table with the specified variable in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    variable:
        variable you want to plot in string format.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("variable", "!string", variable),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))    
    return _charts.create_chart_from_table_and_single_variable("DISTRIBUTION_FITTING", table_name, variable, __get_xml_as_string(xml_file, xml_string))


def create_distribution_summary(table_name, variable, xml_file=None, xml_string=None):
    """Creates a Distribution summary chart on the specified table with the specified variable in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    variable:
        variable you want to plot in string format.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("variable", "!string", variable),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))    
    return _charts.create_chart_from_table_and_single_variable("DISTRIBUTION_SUMMARY", table_name, variable, __get_xml_as_string(xml_file, xml_string))


def create_design_summary(table_name, xml_file=None, xml_string=None):
    """Creates a Design summary chart on the specified table in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))    
    return _charts.create_chart_from_table("DESIGN_SUMMARY", table_name, __get_xml_as_string(xml_file, xml_string))


def create_categories_summary(table_name, xml_file=None, xml_string=None):
    """Creates a Categories summary chart on the specified table in the Design Space.

    table_name:
        name of the table with the data you want to plot.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("table_name", "!string", table_name),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))    
    return _charts.create_chart_from_table("CATEGORIES_SUMMARY", table_name, __get_xml_as_string(xml_file, xml_string))


def create_rsm_coefficients(rsm_name, xml_file=None, xml_string=None):
    """Creates an RSM coefficients chart on the specified RSM in the Design Space.

    rsm_name:
        name of the RSM you want to plot.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("rsm_name", "!string", rsm_name),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    return _charts.create_chart_from_rsm("RSM_COEFFICIENTS", [rsm_name], __get_xml_as_string(xml_file, xml_string))


def create_rsm_explore_bars(rsm_names, xml_file=None, xml_string=None):
    """Creates an RSM explore bars chart on the specified RSMs in the Design Space.

    rsm_names:
        list of names of the RSMs you want to plot.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("rsm_names", "[string]", rsm_names),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    rsm_names = get_as_list(rsm_names, "First argument has to be a list of distinct RSM names")
    if len(rsm_names) != len(set(rsm_names)):
        raise ValueError("First argument has to be a list of distinct RSM names")
    return _charts.create_chart_from_rsm("RSM_EXPLORE_BARS", rsm_names, __get_xml_as_string(xml_file, xml_string))


def create_rsm_summary(rsm_name, table_name=None, xml_file=None, xml_string=None):
    """Creates an RSM summary chart on the specified RSM with the specified table in the Design Space.

    rsm_name:
        name of the RSM you want to plot.
    table_name:
        optional name of the table with the data you want to plot.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("rsm_name", "!string", rsm_name),
                        ("table_name", "?!string", table_name),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    return _charts.create_chart_from_rsm_and_table("RSM_SUMMARY", [rsm_name], table_name, __get_xml_as_string(xml_file, xml_string))


def create_rsm_residuals(rsm_name, table_name, xml_file=None, xml_string=None):
    """Creates an RSM residuals chart on the specified RSM with the specified table in the Design Space.

    rsm_name:
        name of the RSM you want to plot.
    table_name:
        name of the table with the data you want to plot.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("rsm_name", "!string", rsm_name),
                        ("table_name", "!string", table_name),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    return _charts.create_chart_from_rsm_and_table("RSM_RESIDUALS", [rsm_name], table_name, __get_xml_as_string(xml_file, xml_string))


def create_rsm_distance(rsm_name, table_name, xml_file=None, xml_string=None):
    """Creates an RSM distance chart on the specified RSM with the specified table in the Design Space.

    rsm_name:
        name of the RSM you want to plot.
    table_name:
        name of the table with the data you want to plot.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("rsm_name", "!string", rsm_name),
                        ("table_name", "!string", table_name),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    return _charts.create_chart_from_rsm_and_table("RSM_DIST", [rsm_name], table_name, __get_xml_as_string(xml_file, xml_string))


def create_rsm_multiple_distances(rsm_names, table_name, xml_file=None, xml_string=None):
    """Creates an RSM distance chart on the specified RSMs with the specified table in the Design Space.

    rsm_names:
        list of names of the RSMs you want to plot.
    table_name:
        name of the table with the data you want to plot.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("rsm_names", "[string]", rsm_names),
                        ("table_name", "!string", table_name),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    rsm_names = get_as_list(rsm_names, "First argument has to be a list of distinct RSM names")
    return _charts.create_chart_from_rsm_and_table("RSM_MULTIPLE_DIST", rsm_names, table_name, __get_xml_as_string(xml_file, xml_string))


def create_rsm_comparison(rsm_names, table_name):
    """Creates an RSM comparison chart on the specified RSMs with the specified table in the Design Space.

    rsm_names:
        list of names of the RSMs you want to plot.
    table_name:
        name of the table with the data you want to plot.

    Returns the title of the chart."""
    ensure_correct_args(("rsm_names", "[string]", rsm_names),
                        ("table_name", "string", table_name))
    rsm_names = get_as_list(rsm_names, "First argument has to be a list of distinct RSM names")
    return _charts.create_chart_from_rsm_and_table("RSM_COMPARISON", rsm_names, table_name, None)


def create_rsm_validation_table(rsm_names, table_name, xml_file=None, xml_string=None):
    """Creates an RSM validation table on the specified RSMs with the specified table in the Design Space.

    rsm_names:
        list of names of the RSMs you want to plot.
    table_name:
        name of the table with the data you want to plot.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("rsm_names", "[string]", rsm_names),
                        ("table_name", "!string", table_name),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    rsm_names = get_as_list(rsm_names, "First argument has to be a list of distinct RSM names")
    return _charts.create_chart_from_rsm_and_table("RSM_VALIDATION_TABLE", rsm_names, table_name, __get_xml_as_string(xml_file, xml_string))


def create_rsm_function(rsm_names, variable_names):
    """Creates an RSM function chart on the specified RSMs with the specified variables in the Design Space.

    rsm_names:
        list of names of the RSMs you want to plot.
    variable_names:
        list of names of the RSM input variables you want to plot.

    Returns the title of the chart."""
    ensure_correct_args(("rsm_names", "[string]", rsm_names),
                        ("variable_names", "[string]", variable_names))
    rsm_names = get_as_list(rsm_names, "First argument has to be a list of distinct RSM names")
    variable_names = get_as_list(variable_names, "Second argument has to be a list of distinct variable names")
    chart_name = __get_rsm_function_chart_name(rsm_names, variable_names)
    return _charts.create_chart_from_rsm_and_variables(chart_name, rsm_names, variable_names, None)


def create_rsm_explore_3D(rsm_name, variable_names, xml_file=None, xml_string=None):
    """Creates an RSM explore 3D chart on the specified RSM with the specified variables in the Design Space.

    rsm_name:
        name of the RSM you want to plot.
    variable_names:
        list of names of 2 RSM input variables you want to plot.
    xml_file:
        optional XML file with the chart layout.
    xml_string:
        optional XML in string format with the chart layout.

    Returns the title of the chart."""
    ensure_correct_args(("rsm_name", "!string", rsm_name),
                        ("variable_names", "[string]", variable_names),
                        ("xml_file", "?string", xml_file),
                        ("xml_string", "?string", xml_string))
    variable_names = get_as_list(variable_names, "Second argument has to be a list of 2 distinct variables names")
    return _charts.create_chart_from_rsm_and_variables("RSM_EXPLORE_3D", [rsm_name], variable_names, __get_xml_as_string(xml_file, xml_string))


def create_charts_from_xml(xml_file=None, xml_string=None):
    """Import a modeFRONTIER XML layout.

    xml_file:
        optional XML file with the layout.
    xml_string:
        optional XML in string format with the layout.

    Returns a tuple with the titles of all created charts."""
    if (xml_file, xml_string) == (None, None):
        raise RuntimeError("You have to pass at least one argument")
    return _charts.create_charts_from_xml(__get_xml_as_string(xml_file, xml_string))


def get_xml_layout():
    """Export the current modeFRONTIER XML layout.

    Returns the XML in string format."""
    return _charts.get_xml_layout()


__all__ = ["create_parallel_coordinates", "create_parallel_coordinates", "create_multi_history",
           "create_multi_history_3D", "create_multi_vector", "create_scatter", "create_scatter_3D", "create_bubble",
           "create_bubble_4D", "create_design_distribution", "create_broken_constraints", "create_box_whiskers",
           "create_history", "create_PDF", "create_CDF", "create_normal_quantile", "create_distribution_fitting",
           "create_distribution_summary", "create_design_summary", "create_categories_summary", "create_charts_from_xml",
           "get_xml_layout", "create_rsm_coefficients", "create_rsm_explore_bars", "create_rsm_summary",
           "create_rsm_residuals", "create_rsm_distance", "create_rsm_multiple_distances", "create_rsm_comparison",
           "create_rsm_validation_table", "create_rsm_function", "create_rsm_explore_3D"]


def __get_xml_as_string(xml_file, xml_string):
    if None not in (xml_file, xml_string):
        raise RuntimeError("Too many arguments: define either xml_file or xml_string but not both.")
    if xml_file is not None:
        with open(xml_file) as f:
            return f.read()
    return xml_string


def __get_rsm_function_chart_name(rsm_names, variable_names):
    if len(rsm_names) == 1 and len(variable_names) == 1:
        return "RSM_CHART"
    elif len(rsm_names) == 1 and len(variable_names) > 1:
        return "RSM_MATRIX"
    elif len(rsm_names) > 1 and len(variable_names) == 1:
        return "RSM_OVERLAP"
    elif len(rsm_names) > 1 and len(variable_names) > 1:
        return "RSM_OVERLAP_MATRIX"
    else:
        raise ValueError("You have to specify at least 1 RSM name and 1 variable name")
