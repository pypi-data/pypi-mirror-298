import json
import math
import time
from estecopy import db
from estecopy._internal import _plan
from estecopy._utils import arg_parse

ALL_NOTIFICATIONS = "all"
ONLY_ERRORS = "only_errors"
PROCESS_MODE = "process"
SCHEDULING_MODE = "scheduling"
SOFT_STOP = "soft_stop"
TERMINATE_RUN = "terminate_run"
KILL_ALL_PROCESSES = "kill_processes"


def get_current_mode():
    """Returns the current project mode, either PROCESS_MODE or SCHEDULING_MODE."""
    return _plan.get_current_mode()


def list():
    """Returns the plans available in the project."""
    return _plan.list()


def get_plan_as_json(plan_name, as_string=False):
    """Import a plan from modeFRONTIER and returns the plan json as a Python object.

    as_string
      Optional parameter which, if specified, returns the plan json as a string.
    """
    arg_parse.ensure_correct_args(("plan_name", "string", plan_name),
                                  ("as_string", "bool", as_string))
    json_string = _plan.get_as_json(plan_name)
    return json_string if as_string else json.loads(json_string)


def validate_json(plan_object):
    """Check if the plan json is valid.

    Returns a tuple with the JSON errors, or an empty tuple if no errors are present.
    """
    return _plan.validate(json.dumps(plan_object))


def export_plan(plan_object):
    """Export a plan json to modeFRONTIER.

    Returns the name of the exported plan.
    """
    plan_string = json.dumps(plan_object)
    plan_errors = _plan.validate(plan_string)
    if len(plan_errors) == 0:
        return _plan.export(plan_string)
    else:
        raise ValueError("The plan you're trying to export is invalid")


def get_plan_notifications(plan_name, notification_type=ALL_NOTIFICATIONS):
    """Returns a tuple with the plan notifications as in modeFRONTIER.

    notification_type
      Optional parameter which specifies the severity of the issues returned,
      either ALL_NOTIFICATIONS or ONLY_ERRORS. Default is ALL_NOTIFICATIONS.
    """
    arg_parse.ensure_correct_args(("plan_name", "string", plan_name),
                                  ("notification_type", "string", notification_type), )
    return _plan.get_plan_notifications(plan_name, notification_type)


def get_workflow_notifications(notification_type=ALL_NOTIFICATIONS):
    """Returns a tuple with the workflow notifications as in modeFRONTIER.

    notification_type
      Optional parameter which specifies the severity of the issues returned,
      either ALL_NOTIFICATIONS or ONLY_ERRORS. Default is ALL_NOTIFICATIONS.
    """
    arg_parse.ensure_correct_args(("notification_type", "string", notification_type), )
    return _plan.get_workflow_notifications(notification_type)


def can_start_run(plan_name):
    """Checks if a new run can be started.

    Returns True if there are no errors in the plan and in the workflow and if there is no ongoing run.
    """
    arg_parse.ensure_correct_args(("plan_name", "string", plan_name), )
    return (len(get_plan_notifications(plan_name, ONLY_ERRORS)) == 0
            and len(get_workflow_notifications(ONLY_ERRORS)) == 0
            and _plan.can_start_run())


def run_project(plan_name, run_directory=None, project_name=None, project_file_path=None, ignore_out_of_bounds_input_variables=True):
    """Run the current project with the plan specified by plan_name.
    Specify either project_file_path only, or both run_directory and project_name.

    run_directory
      Optional parameter which specifies the run directory
    project_name
      Optional parameter which specifies the project name
    project_file_path
      Optional parameter which specifies the project file path, including the project name with the extension
    ignore_out_of_bounds_input_variables
      Optional parameter which specifies whether the out of bound input values should be recomputed to fit the bounds.
      If False the run won't start.

    Returns a Run object.
    """
    arg_parse.ensure_correct_args(("plan_name", "string", plan_name),
                                  ("run_directory", "?string", run_directory),
                                  ("project_name", "?string", project_name),
                                  ("project_file_path", "?string", project_file_path),
                                  ("ignore_out_of_bounds_input_variables", "bool", ignore_out_of_bounds_input_variables))
    if project_file_path is not None:
        if run_directory is None and project_name is None:
            return __run_indexed_project(project_file_path, plan_name, ignore_out_of_bounds_input_variables)
        else:
            raise ValueError("Wrong arguments: define either project_file_path only or both run_directory and project_name")
    else:
        if run_directory is not None and project_name is not None:
            return __run_project(run_directory, project_name, plan_name, ignore_out_of_bounds_input_variables)
        else:
            raise ValueError("Wrong arguments: define either project_file_path only or both run_directory and project_name")


def __run_indexed_project(project_file_path, plan_name, ignore_out_of_bounds_input_variables):
    run_directory, project_name = _plan.run_project(plan_name, project_file_path, None, None, ignore_out_of_bounds_input_variables)
    return Run(run_directory, project_name)


def __run_project(run_directory, project_name, plan_name, ignore_out_of_bounds_input_variables):
    run_dir, prj_name = _plan.run_project(plan_name, None, run_directory, project_name + ".prj", ignore_out_of_bounds_input_variables)
    return Run(run_dir, prj_name)


def get_current_run():
    """Returns the current run when the run has been started from Python, or None
    if there is no ongoing run or if the run has been started from modeFRONTIER."""
    project_location = _plan.get_current_project_location()
    if project_location is not None:
        return Run(*project_location)


class Run:
    """Class that holds information on a modeFRONTIER run."""

    def __init__(self, run_directory, project_name):
        self.__run_directory = run_directory
        self.__project_name = project_name
        self.__session_name = None

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__run_directory == other.__run_directory and self.__project_name == other.__project_name
        return False

    def stop_run(self, stop_level=SOFT_STOP):
        """Stops the run associated with this class.

        stop_level
          Parameter which specifies the stop level: either SOFT_STOP (which waits for the running designs to be completed),
          TERMINATE_RUN (which terminates the run, including any running designs) and KILL_ALL_PROCESSES (which terminates all run processes).
        """
        arg_parse.ensure_correct_args(("stop_level", "string", stop_level), )
        if not self.has_run_ended():
            _plan.kill_run(stop_level)

    def has_run_ended(self):
        """Returns whether the run has ended."""
        return _plan.has_run_ended(self.__run_directory, self.__project_name)

    def get_session_table_name(self, timeout=None):
        """Returns the name of the session table of this run.

        timeout_s
          Optional parameter which, if specified, limits the waiting time (in seconds) of this method.
        """
        arg_parse.ensure_correct_args(("timeout", "?num", timeout), )
        if timeout is None:
            timeout = math.inf
        if self.__session_name is None:
            self.__session_name = self.__wait_for_file_and_table_creation(timeout)
        return self.__session_name

    def __wait_for_file_and_table_creation(self, timeout):
        session_name = None
        start = time.time()
        while session_name not in db.get_table_names():
            if session_name is None:
                session_name = _plan.get_session_table_name(self.__run_directory, self.__project_name)
            else:
                if time.time() - start > timeout:
                    return None
                time.sleep(0.1)
        return session_name

    def get_run_directory(self):
        """Returns the run directory."""
        return self.__run_directory

    def get_project_name(self):
        """Returns the name of the project associated with the run."""
        return self.__project_name

    def get_engine_error(self):
        """Returns the error occurred on the engine at runtime, or None."""
        return _plan.get_engine_error(self.__run_directory, self.__project_name)


__all__ = ["list", "get_current_mode", "get_plan_as_json", "export_plan", "get_plan_notifications", "validate_json",
           "get_workflow_notifications", "can_start_run", "run_project", "get_current_run", "Run"]
