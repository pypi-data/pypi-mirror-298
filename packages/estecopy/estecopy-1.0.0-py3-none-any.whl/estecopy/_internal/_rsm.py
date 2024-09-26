import atexit
import base64

from estecopy._internal.utils import connection
from estecopy._internal.utils import log
from estecopy._utils.arg_parse import ensure_correct_args, is_sequence

__session = None


def __get_session():
    global __session
    if __session is None:
        log.debug("Creating session…")
        __session = connection.post("/rsm/sessions")
        log.debug("Got session: %s" % __session)
    return __session


def __delete_current_session():
    global __session
    if __session:
        log.debug("About to delete %s" % (__session,))
        try:
            connection.delete("/rsm/sessions/{session}", {"session": __session})
        except:
            pass
        finally:
            __session = None
    else:
        log.debug("Deleting session not required")


def list():
    return connection.get_json("/rsm/list")


def load(output_variable, rsm_name):
    ensure_correct_args(("output_variable", "!string", output_variable),
                        ("rsm_name", "!string", rsm_name))
    return connection.get_json("/rsm/sessions/{session}/functions/load/{variable}/{rsm name}",
                               parameters={"session": __get_session(),
                                           "variable": output_variable,
                                           "rsm name": rsm_name})


def eval(rsm_id, *values):
    ensure_correct_args(("rsm_id", "int", rsm_id),
                        ("*values", "[num]", values))
    return connection.post_json("/rsm/sessions/{session}/functions/{rsm id}/eval",
                                parameters={"session": __get_session(),
                                            "rsm id": rsm_id},
                                json=values)


def eval_array(rsm_id, values):
    check_array(rsm_id, values)
    return connection.post_json("/rsm/sessions/{session}/functions/{rsm id}/eval-array",
                                parameters={"session": __get_session(),
                                            "rsm id": rsm_id},
                                json=values)


def eval_with_std(rsm_id, *values):
    ensure_correct_args(("rsm_id", "int", rsm_id),
                        ("*values", "[num]", values))
    return connection.post_json("/rsm/sessions/{session}/functions/{rsm id}/eval-with-std",
                                parameters={"session": __get_session(),
                                            "rsm id": rsm_id},
                                json=values)


def eval_array_with_std(rsm_id, values):
    check_array(rsm_id, values)
    return connection.post_json("/rsm/sessions/{session}/functions/{rsm id}/eval-array-with-std",
                                parameters={"session": __get_session(),
                                            "rsm id": rsm_id},
                                json=values)


def check_array(rsm_id, values):
    if not is_sequence(values):
        raise ValueError("Argument is not a sequence")
    ensure_correct_args(("rsm_id", "int", rsm_id))
    for value in values:
        ensure_correct_args(("value", "[num]", value))


def get_properties(rsm_id):
    ensure_correct_args(("rsm_id", "int", rsm_id))
    return connection.get_json("/rsm/sessions/{session}/functions/{rsm id}",
                               parameters={"session": __get_session(),
                                           "rsm id": rsm_id},
                               query_parameters={"property": "properties"})


def can_estimate_std(rsm_id):
    ensure_correct_args(("rsm_id", "int", rsm_id))
    return connection.get_json("/rsm/sessions/{session}/functions/{rsm id}",
                               parameters={"session": __get_session(),
                                           "rsm id": rsm_id},
                               query_parameters={"property": "can_estimate_std"})


def get_python_code(rsm_id, class_name):
    ensure_correct_args(("rsm_id", "int", rsm_id),
                        ("class_name", "?!string", class_name))
    if class_name:
        query_parameters = {"property": "python_code",
                            "class_name": class_name}
    else:
        query_parameters = {"property": "python_code"}

    return connection.get_json("/rsm/sessions/{session}/functions/{rsm id}",
                               parameters={"session": __get_session(),
                                           "rsm id": rsm_id},
                               query_parameters=query_parameters)


def remove(rsm_id):
    ensure_correct_args(("rsm_id", "int", rsm_id))
    global __session
    # Ensure that the underlying session has not been deleted already by the atexit callback
    if __session:
        log.debug("Removing '%d'" % rsm_id)
        connection.delete("/rsm/sessions/{session}/functions/{rsm id}",
                          parameters={"session": __session,
                                      "rsm id": rsm_id})


def set_output_name(rsm_id, output_variable_name):
    ensure_correct_args(("rsm_id", "int", rsm_id),
                        ("output_variable_name", "!string", output_variable_name))
    connection.patch("/rsm/sessions/{session}/functions/{rsm id}",
                     parameters={"session": __get_session(),
                                 "rsm id": rsm_id},
                     query_parameters={"property": "output_variable_name"},
                     json=output_variable_name)


def set_name(rsm_id, rsm_name):
    ensure_correct_args(("rsm_id", "int", rsm_id),
                        ("rsmname", "!string", rsm_name))
    connection.patch("/rsm/sessions/{session}/functions/{rsm id}",
                     parameters={"session": __get_session(),
                                 "rsm id": rsm_id},
                     query_parameters={"property": "name"},
                     json=rsm_name)

def from_file(path_to_rsm_file):
    ensure_correct_args(("path_to_rsm_file", "!string", path_to_rsm_file))
    with open(path_to_rsm_file, "rb") as f:
        base64Data = base64.standard_b64encode(f.read())
        return connection.post_data("/rsm/sessions/{session}/functions",
                                    parameters={"session": __get_session()},
                                    data=base64Data)

def to_file(rsm_id, path_to_rsm_file):
    ensure_correct_args(("rsm_id", "int", rsm_id),
                        ("path_to_rsm_file", "!string", path_to_rsm_file))
    base64Data = connection.get("/rsm/sessions/{session}/functions/{rsm id}/data",
                                parameters={"session": __get_session(),
                                            "rsm id": rsm_id})
    rsm_bytes = base64.decodebytes(bytes(base64Data, "ASCII"))
    with open(path_to_rsm_file, "wb") as f:
        f.write(rsm_bytes)

def save(rsm_id, exported_name, destination):
    ensure_correct_args(("rsm_id", "int", rsm_id),
                        ("exported_name", "!string", exported_name))
    if destination == "output node":
        raise RuntimeError("Save to output node not supported in pyFRONTIER")
    return connection.post_json("/rsm/sessions/{session}/functions/{rsm id}/save/{name}",
                                parameters={"session": __get_session(),
                                            "rsm id": rsm_id,
                                            "name": exported_name})


atexit.register(__delete_current_session)
