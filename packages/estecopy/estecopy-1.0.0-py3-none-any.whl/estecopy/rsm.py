import numbers
import os
import tempfile
import webbrowser
from estecopy._internal import _rsm
from estecopy._utils import arg_parse
from estecopy._utils import python_rsm

DEST_DESIGN_SPACE = "design space"
DEST_OUTPUT_NODE = "output node"
DEST_DEFAULT = "default"

__use_java_rsm = True

def use_python_rsm(use_python_rsm):
    """Sets whether to use Python-based RSMs when available.

    By default, the Java implementation is used

    use_python_rsm:
      True to use Python-based RSMs when available, False otherwise."""
    global __use_java_rsm
    if not isinstance(use_python_rsm, bool):
        raise TypeError("'use_python_rsm' must be a boolean")
    __use_java_rsm = not use_python_rsm


def __convert_rsm(rsm):
    if __use_java_rsm:
        return rsm
    else:
        python_rsm = rsm.get_python_rsm()
        return python_rsm if python_rsm else rsm

class RSM:
    """This class represents an RSM function created with modeFRONTIER.

    You can evaluate the RSM with the 'eval' method:

        >>> kr0 = rsm.load('f1', 'f1_KR_0')
        >>> kr0.eval(1, 2)
        12.5

    or by directly calling the object:

        >>> kr0(1, 2)
        12.5

    The arguments of the function are the input variable values.
    Use the 'get_input_names' method to retrieve the input variables used to train the RSM:

        >>> len(rsm.get_input_names())
        2"""

    def __init__(self, index, __callbacks=_rsm):
        self.__callbacks = __callbacks
        self.__index = index
        self.__cache_properties()
        self.__log_files = []

    def __cache_properties(self):
        self.__raw_properties = self.__callbacks.get_properties(self.__index).copy()
        self.__input_count = len(self.__raw_properties["input_variables_names"])

    def get_name(self):
        """Returns the RSM name."""
        return self.__raw_properties["name"]

    def get_input_names(self):
        """Returns a tuple with the names of the input variables used to train the RSM."""
        return self.__raw_properties["input_variables_names"]

    def get_output_name(self):
        """Returns the name of the output approximated by the RSM."""
        return self.__raw_properties["output_variable_name"]

    def get_created(self):
        """Returns the timestamp of the RSM training (in seconds)."""
        return self.__raw_properties["created_ms"] / 1000.0

    def show_training_logs(self, auto_remove_log_file=True, create_only=False):
        """Opens the RSM training logs in a browser.

        Returns the name of the temporary log file that by default is deleted when the RSM goes out of scope.

        auto_remove_log_file:
           delete the temporary log file when the RSM goes out of scope.
        create_only:
            create the temporary log file without opening it in the browser."""
        # Turning the "delete" option on would create a file with an unwanted FILE_SHARE_DELETE flag on Windows
        temp_file = tempfile.NamedTemporaryFile(prefix="modeFRONTIER_%s_training_log_" % self.get_name(), suffix=".html", delete=False)
        temp_file.write(bytes(self.__raw_properties["log"], "utf8"))
        temp_file.close()
        if auto_remove_log_file:
            self.__log_files.append(temp_file)
        log_path = os.path.realpath(temp_file.name)
        if not create_only:
            webbrowser.open("file://" + log_path)
        return log_path

    def __call__(self, *args):
        return self.eval(*args)

    def eval(self, *args):
        """Evaluates a single point with the RSM."""
        self.__ensure_valid_arguments(args)
        return self.__callbacks.eval(self.__index, *args)

    def eval_array(self, array):
        """Evaluates an array of points with the RSM."""
        for args in array:
            self.__ensure_valid_arguments(args)
        return self.__callbacks.eval_array(self.__index, array)

    def can_estimate_std(self):
        """Returns whether the RSM can estimate the standard deviation."""
        return self.__callbacks.can_estimate_std(self.__index)

    def eval_with_std(self, *args):
        """Evaluates a single point with the RSM and computes the standard deviation.

        Returns a tuple (evaluation, std), where std is None if the RSM does not support standard deviation estimation."""
        self.__ensure_valid_arguments(args)        
        return self.__callbacks.eval_with_std(self.__index, *args)

    def eval_array_with_std(self, array):
        """Evaluates an array of points with the RSM and computes the standard deviation.

        Returns a tuple of tuples (evaluation, std), where std is None if the RSM does not support standard deviation estimation."""
        for args in array:
            self.__ensure_valid_arguments(args)        
        return self.__callbacks.eval_array_with_std(self.__index, array)

    def __ensure_valid_arguments(self, args):
        if len(args) != self.__input_count:
            raise TypeError("Invalid number of arguments")
        for value in args:
            if not isinstance(value, numbers.Number):
                raise TypeError("Invalid type for input value")           

    def __del__(self):
        self.__callbacks.remove(self.__index)
        self.__delete_log_files()

    def __delete_log_files(self):
        for path in self.__log_files:
            try:
                os.unlink(path.name)
            except:
                pass

    def is_python_rsm(self):
        """Returns whether the RSM is based on pure Python code.

        Returns True for Python-based RSM, False otherwise."""
        return isinstance(self.__callbacks, python_rsm.PythonRsm)

    def to_file(self, rsm_file_path):
        """Export the RSM to an *.rsm file.

        This operation is not supported for pure Python RSMs.

        Returns the path to the file."""
        path_to_rsm_file = os.path.abspath(rsm_file_path)
        self.__try_save(path_to_rsm_file)
        self.__callbacks.to_file(self.__index, path_to_rsm_file)
        return path_to_rsm_file

    def __try_save(self, path):
        with open(path, "wb") as f:
            f.write(b"0")

    def save(self, rsm_name=None, destination=DEST_DEFAULT):
        """Export the RSM to modeFRONTIER.

        This operation is not supported for pure Python RSMs.

        rsm_name
           the name of the RSM to be exported (if unspecified, the name of the current RSM will be used)
        destination
            can be one of the following strings:

            DEST_DESIGN_SPACE
                save the RSM in the Design Space (pyCONSOLE or CPython node with process fork run policy)
            DEST_OUTPUT_NODE
                send the RSM to the specified RSM output parameter node (CPython node only)
            DEST_DEFAULT
                same as DEST_DESIGN_SPACE in pyCONSOLE and DEST_OUTPUT_NODE in the CPython node

        Returns the name with which the RSM was exported."""
        if not arg_parse.is_string(destination):
            raise TypeError("Third argument has to be a string")
        if not destination in [DEST_DESIGN_SPACE, DEST_OUTPUT_NODE, DEST_DEFAULT]:
            raise ValueError("'%s' is not a valid RSM destination" % destination)
        exported_name = self.get_name() if rsm_name is None else rsm_name        
        self.__callbacks.save(self.__index, exported_name, destination)
        return exported_name

    def set_output_name(self, output_variable_name):
        """Change the output variable name of the RSM."""
        self.__callbacks.set_output_name(self.__index, output_variable_name)
        self.__raw_properties["output_variable_name"] = output_variable_name

    def set_name(self, rsm_name):
        """Change the name of the RSM."""
        self.__callbacks.set_name(self.__index, rsm_name)
        self.__raw_properties["name"] = rsm_name

    def get_python_code(self, class_name=None):
        """Return the Python code for the RSM, if available.

class_name
  the name of the Python class to be generated (defaults to 'RSM' if not specified).

Returns the Python representation of the RSM or None if unavailable."""
        if class_name and not isinstance(class_name, str):
            raise TypeError("'%s' is not a string" % (class_name,))
        elif class_name and not class_name.isidentifier():
            raise ValueError("'%s' is not a valid Python identifier" % (class_name,))
        return self.__callbacks.get_python_code(self.__index, class_name)

    def get_python_rsm(self):
        """Returns a Python-based copy of the RSM.

        While based on the same algorithm, Python-based RSMs are implemented with 
        pure Python code: they may show small differences in the evaluation results
        and will perform differently than their Java counterparts.

        The RSM is based on the algorithm returned by the 'get_python_code' method.

        Python-based RSM can't be exported.

        Returns a new Python-based RSM or None if unavailable."""
        template_token = "__TEMPLATE_TOKEN_FOR_THE_CLASS_NAME__"
        template = self.get_python_code(template_token)
        if template:
            return RSM(-1, python_rsm.PythonRsm(template, self.__raw_properties, template_token))
        else:
            return None

    def get_leave_one_out_errors(self):
        """Returns the leave-one-out errors of the RSM.

        Returns a tuple with the errors, or None if unavailable."""
        return self.__raw_properties.get("loo_errors")

    def serialize(self):
        """Serializes the RSM to binary format suitable for use with the "pickle" module."""
        tmp = tempfile.NamedTemporaryFile(delete=False)
        try:
            self.__callbacks.to_file(self.__index, tmp.name)
            return tmp.read()
        finally:
            tmp.close()
            os.unlink(tmp.name)


def deserialize(serialized_rsm):
    """Deserializes the RSM based on the binary object."""
    tmp = tempfile.NamedTemporaryFile(delete=False)
    try:
        tmp.write(serialized_rsm)
        tmp.flush()
        return from_file(tmp.name)
    finally:
        tmp.close()
        os.unlink(tmp.name)

def from_file(rsm_path):
    """Imports an *.rsm file and returns an RSM object."""
    path = os.path.abspath(rsm_path)
    __try_load(path)
    return __convert_rsm(RSM(_rsm.from_file(path)))


def __try_load(path):
    with open(path, "rb") as f:
        f.read(1)

def list():
    """List the RSMs in Design Space.

    Returns a dictionary of RSMs, grouped by output.

    Example:

        >>> rsm.list()
        {'f1' : ['f1_KR_0', 'f1_SVD_0'], 'f2' : ['f2_H2O_DRF_0']}"""

    result = {}
    for output_variable, rsm_name in _rsm.list():
        if not output_variable in result:
            result[output_variable] = []
        result[output_variable].append(rsm_name)
    return result


def load(output_variable, rsm_name):
    """RSM is loaded from Design Space and returned it as RSM object.

    output_variable:
      name of output approximated by RSM.
    rsm_name:
      name of RSM.

    Example:

        # first obtain the dictionary of available RSMs
        >>> rsm.list()
        {'f1' : ['f1_KR_0', 'f1_SVD_0'], 'f2' : ['f2_H2O_DRF_0']}
        # use key and value to load a specific RSM
        >>> kr0 = rsm.load('f1', 'f1_KR_0')
        >>> kr0.get_name()
        f1_KR_0"""
    return __convert_rsm(RSM(_rsm.load(output_variable, rsm_name)))


__all__ = ["from_file", "load", "list", "deserialize", "RSM"]
