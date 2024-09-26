from estecopy._internal.utils import connection
from estecopy._utils.arg_parse import ensure_correct_args


def list():
    return tuple(connection.get_json("/plan/list"))


def get_current_mode():
    return "process" if connection.get_json("/plan/", query_parameters={"param": "enabled"}) else "scheduling"


def get_as_json(plan_name):
    ensure_correct_args(("plan_name", "!string", plan_name))
    return connection.get("/plan/{plan_name}", parameters={"plan_name": plan_name})


def export(plan_json):
    ensure_correct_args(("plan_json", "!string", plan_json))
    return connection.post("/plan/export", json=plan_json)


def get_plan_notifications(plan_name, notification_type):
    ensure_correct_args(("plan_name", "!string", plan_name),
                        ("notification_type", "!string", notification_type))
    return tuple(connection.get_json("/plan/{plan_name}/notifications", parameters={"plan_name": plan_name}, query_parameters={"param": notification_type}))


def get_workflow_notifications(notification_type):
    ensure_correct_args(("notification_type", "!string", notification_type))
    return tuple(connection.get_json("/workflow/notifications", query_parameters={"param": notification_type}))


def validate(plan_json):
    ensure_correct_args(("plan_json", "string", plan_json))
    if not plan_json:
        raise ValueError("The plan you're trying to import is in the wrong format or contains incorrect keys or values")
    return tuple(connection.post_json("/plan/validation", json=plan_json))


def run_project(plan_name, project_file_path, run_directory, project_file, ignore_out_of_bounds_input_variables):
    ensure_correct_args(("plan_name", "!string", plan_name),
                        ("project_file_path", "?string", project_file_path),
                        ("run_directory", "?string", run_directory),
                        ("project_file", "?string", project_file),
                        ("ignore_out_of_bounds_input_variables", "bool", ignore_out_of_bounds_input_variables))
    return connection.post_json("/run/{plan_name}", parameters={"plan_name": plan_name},
                                json={"project_file_path": project_file_path,
                                      "run_directory": run_directory,
                                      "project_file": project_file,
                                      "ignore_out_of_bounds_input_variables": ignore_out_of_bounds_input_variables})


def can_start_run():
    return connection.get_json("/run/", query_parameters={"param": "can_start_run"})


def kill_run(stop_level):
    ensure_correct_args(("stop_level", "!string", stop_level))
    connection.get("/run/kill/{stop_level}", parameters={"stop_level": stop_level})


def get_current_project_location():
    return connection.get_json("/run/current/project_location")


def has_run_ended(run_directory, project_name):
    return connection.get_json("/run/{run_directory}/{project_name}/has_ended",
                               parameters={"run_directory": run_directory,
                                           "project_name": project_name})


def get_session_table_name(run_directory, project_name):
    return connection.get("/run/{run_directory}/{project_name}/session_table_name",
                          parameters={"run_directory": run_directory,
                                      "project_name": project_name})


def get_engine_error(run_directory, project_name):
    return connection.get("/run/{run_directory}/{project_name}/engine_error",
                          parameters={"run_directory": run_directory,
                                      "project_name": project_name})
