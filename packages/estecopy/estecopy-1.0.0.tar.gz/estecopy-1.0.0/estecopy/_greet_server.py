import atexit
import pyfrontier
import sys
import traceback
from estecopy._internal.utils import connection
from estecopy._internal.utils import log


def __log(message):
    connection.post_data("/server/log", query_parameters={"estecopy-version": pyfrontier.get_estecopy_version()}, data=bytes(message, "utf-8"))


def __get_version():
    raw_version = sys.version
    try:
        return raw_version.splitlines()[0]
    except:
        return raw_version


def __debug_exception(e):
    log.debug(str(e))
    log.debug(traceback.format_exc())


def __farewell_server():
    try:
        __log(f"Python {__get_version()} disconnected")
    except Exception as e:
        log.debug("Unable to farewell server")
        __debug_exception(e)


def __clear_modules():
    try:
        to_delete = [i for i in sys.modules.keys() if i.startswith("estecopy.")]
        for i in to_delete:
            del sys.modules[i]
    except Exception as e:
        log.debug("Unable to clear estecopy modules (ignored)")
        __debug_exception(e)


def __greet_server():
    if pyfrontier.get_protocol() == "auto":
        __try_all_protocols_in_order()
    else:
        __use_current_protocol()


def __try_all_protocols_in_order():
    if __try_protocol("https"):
        return
    elif __try_protocol("https-no-checks"):
        return
    else:
        pyfrontier._get_config().set_protocol("http")
        __use_current_protocol()


def __try_protocol(protocol):
    pyfrontier._get_config().set_protocol(protocol)
    try:
        __use_current_protocol()
        return True
    except:
        return False


def __use_current_protocol():
    try:
        __log(f"Python {__get_version()} connected")
        atexit.register(__farewell_server)
    except Exception as e:
        connection.clear_connection()
        __clear_modules()
        __debug_exception(e)
        raise ImportError(f"Connection with pyFRONTIER failed:\n"
                          f"{e}") from None
