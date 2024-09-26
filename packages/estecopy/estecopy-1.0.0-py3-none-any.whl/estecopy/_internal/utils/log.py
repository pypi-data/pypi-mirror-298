import os
import sys

__DEBUG_VARIABLE_NAME = "PYFRONTIER_DEBUG"

__debug_enabled = None


def info(msg):
    sys.stderr.write("pyFRONTIER[INFO]: " + msg + "\n")


def __is_debug_enabled():
    global __debug_enabled
    if __debug_enabled is None:
        debug_mode = os.getenv(__DEBUG_VARIABLE_NAME)
        __debug_enabled = debug_mode != None
    return __debug_enabled


def debug(msg):
    if __is_debug_enabled():
        sys.stderr.write("pyFRONTIER[DEBUG]: " + msg + "\n")
