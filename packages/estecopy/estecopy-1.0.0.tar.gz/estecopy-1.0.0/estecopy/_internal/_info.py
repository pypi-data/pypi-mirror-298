from estecopy._internal.utils import connection


def get_project_path():
    return connection.get("/info/frontier-project-path")


def get_proc_folder_path():
    return connection.get("/info/proc-folder-path")
