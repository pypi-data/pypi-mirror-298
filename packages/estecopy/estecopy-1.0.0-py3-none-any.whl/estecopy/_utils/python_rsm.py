import copy


class PythonRsm:
    __DEFAULT_EXPORTED_PYTHON_CLASS_NAME = "RSM"

    def __init__(self, code_template, raw_properties, template_token):
        self.__code_template = code_template
        self.__raw_properties = copy.deepcopy(raw_properties)
        self.__template_token = template_token
        self.__compile_code()

    def __compile_code(self):
        try:
            class_name = self.__DEFAULT_EXPORTED_PYTHON_CLASS_NAME
            sandbox = {}
            exec(self.get_python_code(-1, class_name), sandbox, sandbox)
            self.__bare_rsm = sandbox[class_name]()
        except Exception as e:
            raise RuntimeError("Algorithm compilation error") from e

    def get_properties(self, _):
        return copy.deepcopy(self.__raw_properties)

    def eval(self, _, *args):
        return self.__bare_rsm.evaluate(args)

    def eval_array(self, _, array):
        return tuple(self.__bare_rsm.evaluate(point) for point in array)

    def eval_array_with_std(self, _, array):
        return tuple((self.__bare_rsm.evaluate(point), None) for point in array)

    def can_estimate_std(self, _):
        return False

    def eval_with_std(self, _, *args):
        return self.__bare_rsm.evaluate(args), None

    def remove(self, _, *args):
        pass

    def to_file(self, _, path_to_rsm_file):
        raise RuntimeError("this operation is not supported for pure Python RSM")

    def save(self, _, exported_name, destination):
        raise RuntimeError("this operation is not supported for pure Python RSM")

    def set_output_name(self, _, output_variable_name):
        self.__raw_properties["output_variable_name"] = output_variable_name

    def set_name(self, _, rsm_name):
        self.__raw_properties["name"] = rsm_name

    def get_python_code(self, _, class_name):
        return self.__code_template.replace(self.__template_token,
                                            class_name or self.__DEFAULT_EXPORTED_PYTHON_CLASS_NAME)
