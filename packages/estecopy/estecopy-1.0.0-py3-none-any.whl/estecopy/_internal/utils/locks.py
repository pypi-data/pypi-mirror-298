import os
import re
import subprocess
import traceback

from estecopy._internal.utils import config
from estecopy._internal.utils import log


def get_lock_port(path):
    try:
        with open(path) as f:
            return int(f.read())
    except:
        log.info("Unexpected lock content for '%s'" % path)
        return None


def __decode_tasklist_output(data):
    try:
        return data.decode()
    except:
        try:
            return data.decode("shift_jis")
        except:
            return None
    

def is_valid_pid_windows(pid):
    decoded = __decode_tasklist_output(subprocess.check_output(["tasklist.exe", "/fi", "PID eq %d" % (pid,), "/fo", "csv"]))
    if decoded is None:
        log.debug(f"tasklist.exe output not decoded: accepting PID {pid} as valid by default")
        return True

    lines = decoded.splitlines()
    if len(lines) == 1:
        if not lines[0].startswith("INFO"):
            log.info("Unexpected tasklist output for PID %d: assuming the process is alive" % pid)
            return True
        return False
    else:
        return True


def is_valid_pid_unix(pid):
    code = subprocess.call(["ps", str(pid)],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
    return code == 0


def is_pid_valid(pid):
    if os.name == 'nt':
        return is_valid_pid_windows(pid)
    else:
        return is_valid_pid_unix(pid)


def __print_exception(name):
    try:
        log.debug(f"Lock '{name}' accepted due to an unexpected exception")
        log.debug(traceback.format_exc())
    except:
        pass


def is_valid_lock(name):
    try:
        pid = int(name.split(".")[1])
        return is_pid_valid(pid)
    except:
        __print_exception(name)
        return True


def is_lock_file(filename):
    return re.fullmatch("pyFrontier[.][0-9]+", filename)


def get_locks(path):
    try:
        get_full_path = lambda name: os.path.join(path, name)
        return map(get_lock_port,
                   map(get_full_path,
                       filter(is_valid_lock,
                              filter(is_lock_file,
                                     os.listdir(path)))))
    except FileNotFoundError:
        raise RuntimeError("Could not find modeFRONTIER installation on this machine.")


def get_temp_dir_path():
    default_home = os.path.join(config.modeFRONTIER_config_dir,
                                str(config.modeFRONTIER_version))
    temp_path = os.path.join(os.getenv("FRONTIER_TMP_DIR", default_home), "tmp")
    return os.path.expanduser(temp_path)


def get_ports():
    ports = list(get_locks(get_temp_dir_path()))
    if not ports:
        raise RuntimeError("A valid pyFRONTIER was not found on this machine. Make sure pyFRONTIER is running")
    else:
        return ports
