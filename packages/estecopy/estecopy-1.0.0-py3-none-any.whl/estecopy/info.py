from estecopy._internal import _info


def get_project_path():
    """Returns the path of the project currently open in modeFRONTIER."""
    return _info.get_project_path()


def get_proc_folder_path():
    """Returns the path of the 'proc' folder of the project currently open in modeFRONTIER.

'None' is returned if the working directory doesn't exist."""
    return _info.get_proc_folder_path()


__all__ = ["get_project_path", "get_proc_folder_path"]
