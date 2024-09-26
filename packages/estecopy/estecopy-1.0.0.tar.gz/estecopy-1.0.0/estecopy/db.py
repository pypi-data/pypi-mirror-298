import math
import numbers
import re
import sys
from estecopy._internal import _db
from estecopy._utils import arg_parse

__ALL_TABLES = "all"
METADATA_KEY = "metadata"
INPUTS_KEY = "inputs"
OUTPUTS_KEY = "outputs"
CATEGORIES_KEY = "categories"
DATA_KEY = "data"
COLUMN_NAMES_KEY = "column_names"
MARKED_KEY = "marked"
LINKED_SESSION_TABLE_NAME_KEY = "linked_session_table_name"

NAME_KEY = "name"
ROWS_KEY = "rows"
ID_KEY = "id"
RID_KEY = "rid"
IDS_KEY = "ids"
VIRTUAL_KEY = "virtual"

ID_COLUMN_NAME = ID_KEY
MARKED_COLUMN_NAME = MARKED_KEY
VIRTUAL_COLUMN_NAME = VIRTUAL_KEY
CATEGORY_COLUMN_PREFIX = "cat:"
INPUT_COLUMN_PREFIX = "in:"
OUTPUT_COLUMN_PREFIX = "out:"


class Shapes:
    SQUARE = "SQUARE"
    DIAMOND = "DIAMOND"
    TRIANGLE = "TRIANGLE"
    TRIANGLE_DOWN = "TRIANGLE_DOWN"
    CIRCLE = "CIRCLE"
    CROSS = "CROSS"
    X = "X"
    H_LINE = "H_LINE"
    V_LINE = "V_LINE"
    STAR = "STAR"
    NONE = "NONE"

    __valid_shapes = None

    @staticmethod
    def get_valid_shapes():
        Shapes.__valid_shapes = Shapes.__valid_shapes or set([getattr(Shapes, i) for i in dir(Shapes) if i.upper() == i])
        return set(Shapes.__valid_shapes)

    @staticmethod
    def is_valid_shape(string):
        Shapes.__valid_shapes = Shapes.__valid_shapes or set([getattr(Shapes, i) for i in dir(Shapes) if i.upper() == i])
        return string in Shapes.__valid_shapes


def get_version():
    """Returns the version of this module as (major, minor, patch)."""
    return 1, 3, 0


def get_table_names():
    """Returns names of the available tables."""
    if __ALL_TABLES not in _db.get_table_types():
        return ()
    else:
        return _db.get_table_names(__ALL_TABLES)


class __TableDataChecker:

    def _check_columns(self, column_names):
        for index, column_name in enumerate(column_names, start=1):
            if not isinstance(column_name, str):
                raise TypeError("column %d is not a string" % (index,))
        names = set(column_names)
        if not len(names) == len(column_names):
            raise ValueError("column names should be unique")

    def _check_rows(self, column_names):
        columns = len(column_names)
        for index, row in enumerate(self.rows, start=1):
            if not len(row) == columns:
                raise ValueError("row %d has %d columns (%d expected)" % (index, len(row), columns))


class _EncodedHeaderTableBuilder(__TableDataChecker):
    __BOUNDS_KEY = "bounds"
    __TYPE_KEY = "type"
    __VALID_TYPES = set(("constant", "variable"))
    __DEFAULT_VALUE_KEY = "default_value"
    __BASE_KEY = "base"
    __FORMAT_KEY = "format"
    __DESCRIPTION_KEY = "description"
    __ALL_PARAMETER_KEYS = (__BOUNDS_KEY, __TYPE_KEY, __DEFAULT_VALUE_KEY, __BASE_KEY, __FORMAT_KEY, __DESCRIPTION_KEY)
    __CATEGORY_NAMES_KEY = "names"
    __CATEGORY_LABELS_KEY = "labels"
    __CATEGORY_SYMBOLS_KEY = "symbols"
    __CATEGORY_LABEL = "label"
    __CATEGORY_SHAPE = "shape"
    __DEFAULT_SHAPE = "CIRCLE"
    __CATEGORY_SIZE = "size"
    __DEFAULT_SIZE = 11
    __CATEGORY_COLOR = "color"
    __DEFAULT_COLOR = "#000000"
    __CATEGORY_BORDER = "border"
    __DEFAULT_BORDER = 1
    __CATEGORY_FILL_COLOR = "fill_color"
    __DEFAULT_FILL_COLOR = None
    __CATALOGUE_KEYS = {__CATEGORY_LABEL, __CATEGORY_SHAPE,
                        __CATEGORY_COLOR, __CATEGORY_SIZE,
                        __CATEGORY_BORDER, __CATEGORY_FILL_COLOR}
    __OBJECTIVES_KEY = "objectives"
    __OBJECTIVE_TYPE_KEY = "type"
    __OBJECTIVE_EXPRESSION_KEY = "expression"
    __OBJECTIVE_FORMAT_KEY = "format"
    __OBJECTIVE_DESCRIPTION_KEY = "description"
    __MANDATORY_OBJECTIVE_KEYS = (__OBJECTIVE_TYPE_KEY, __OBJECTIVE_EXPRESSION_KEY)
    __ALL_OBJECTIVE_KEYS = (*__MANDATORY_OBJECTIVE_KEYS, __OBJECTIVE_FORMAT_KEY, __OBJECTIVE_DESCRIPTION_KEY)
    __OBJECTIVE_TYPES = ("minimize", "maximize")
    __CONSTRAINTS_KEY = "constraints"
    __CONSTRAINT_TYPE_KEY = "type"
    __CONSTRAINT_TOLERANCE_KEY = "tolerance"
    __CONSTRAINT_LIMIT_KEY = "limit"
    __CONSTRAINT_EXPRESSION_KEY = "expression"
    __CONSTRAINT_FORMAT_KEY = "format"
    __CONSTRAINT_DESCRIPTION_KEY = "description"
    __MANDATORY_CONSTRAINT_KEYS = (__CONSTRAINT_TYPE_KEY, __CONSTRAINT_TOLERANCE_KEY, __CONSTRAINT_LIMIT_KEY, __CONSTRAINT_EXPRESSION_KEY)
    __ALL_CONSTRAINT_KEYS = (*__MANDATORY_CONSTRAINT_KEYS, __CONSTRAINT_FORMAT_KEY, __CONSTRAINT_DESCRIPTION_KEY)
    __CONSTRAINT_TYPES = ("greater than", "equal to", "less than")
    __EXPRESSIONS_KEY = "expressions"
    __EXPRESSION_EXPRESSION_KEY = "expression"
    __EXPRESSION_FORMAT_KEY = "format"
    __EXPRESSION_DESCRIPTION_KEY = "description"

    def __init__(self, table_name, encoded_column_names, rows, optional_properties=None,
                 objectives=None, constraints=None, expressions=None):
        self.table_name = table_name
        self.encoded_column_names = encoded_column_names
        self.rows = rows
        self.optional_properties = optional_properties
        self.objectives = objectives
        self.constraints = constraints
        self.expressions = expressions

    def check(self):
        self.__check_table_name()
        self._check_columns(self.encoded_column_names)
        for name in self.encoded_column_names:
            self.__check_column_name(name)
        variable_names = self.__check_variables()
        self._check_rows(self.encoded_column_names)
        self.__check_column_values()
        if self.optional_properties is not None:
            self.__parse_extra_properties(variable_names)
        if self.objectives is not None:
            self.__check_objectives()
        if self.constraints is not None:
            self.__check_constraints()
        if self.expressions is not None:
            self.__check_expressions()

    def __check_table_name(self):
        if not isinstance(self.table_name, str):
            raise TypeError("table_name must be a string")

    def __check_column_name(self, column_name):
        if column_name in {ID_COLUMN_NAME, MARKED_COLUMN_NAME, VIRTUAL_COLUMN_NAME}:
            return
        for prefix in (CATEGORY_COLUMN_PREFIX, INPUT_COLUMN_PREFIX, OUTPUT_COLUMN_PREFIX):
            prefix_length = len(prefix)
            if column_name[:prefix_length] == prefix and len(column_name[prefix_length:].strip()) > 0:
                return
        raise ValueError("invalid column name '%s'" % (column_name,))

    def __check_variables(self):
        variable_names = set()
        for name in self.encoded_column_names:
            for prefix in (CATEGORY_COLUMN_PREFIX, INPUT_COLUMN_PREFIX, OUTPUT_COLUMN_PREFIX):
                if name.startswith(prefix):
                    var_name = name[len(prefix):]
                    if var_name in variable_names:
                        raise ValueError("duplicate variable name '%s'" % (var_name,))
                    else:
                        variable_names.add(var_name)
        return variable_names

    def __check_column_values(self):
        checks = [[lambda name: name == ID_COLUMN_NAME, lambda value: isinstance(value, int) and not isinstance(value, bool), lambda value: value >= 0],
                  [lambda name: name == MARKED_COLUMN_NAME, lambda value: isinstance(value, bool), None],
                  [lambda name: name == VIRTUAL_COLUMN_NAME, lambda value: isinstance(value, bool), None],
                  [lambda name: name[:len(CATEGORY_COLUMN_PREFIX)] == CATEGORY_COLUMN_PREFIX, lambda value: isinstance(value, str), None],
                  [lambda name: name[:len(INPUT_COLUMN_PREFIX)] == INPUT_COLUMN_PREFIX, lambda value: isinstance(value, numbers.Number) and not isinstance(value, bool), None],
                  [lambda name: name[:len(OUTPUT_COLUMN_PREFIX)] == OUTPUT_COLUMN_PREFIX, lambda value: isinstance(value, numbers.Number) and not isinstance(value, bool), None]]

        for index, column_name in enumerate(self.encoded_column_names):
            for check in checks:
                name_predicate = check[0]
                if name_predicate(column_name):
                    type_predicate = check[1]
                    self.__ensure_valid_columns_types(index, type_predicate)
                    value_predicate = check[2]
                    if value_predicate:
                        self.__ensure_valid_columns_values(index, value_predicate)                                            

    def __ensure_valid_columns_types(self, column_index, type_predicate):
        column = [row[column_index] for row in self.rows]
        for row_index, value in enumerate(column):
            if not type_predicate(value):
                column_name = self.encoded_column_names[column_index]
                raise TypeError("Invalid type for value '%s' in column '%s' at row %d" % (value, column_name, row_index + 1))

    def __ensure_valid_columns_values(self, column_index, type_predicate):
        column = [row[column_index] for row in self.rows]
        for row_index, value in enumerate(column):
            if not type_predicate(value):
                column_name = self.encoded_column_names[column_index]
                raise ValueError("Invalid value '%s' for '%s' at row %d" % (value, column_name, row_index + 1))

    def __parse_extra_properties(self, variable_names):
        if not isinstance(self.optional_properties, dict):
            raise TypeError("This method requires a dictionary with properties as third parameter")

        for target_var, property_dict in self.optional_properties.items():
            if not isinstance(target_var, str):
                raise TypeError("Invalid type for value '%s'" % (target_var,))

            if target_var not in variable_names:
                raise ValueError("'%s' is not a valid variable or catalogue" % (target_var,))

            if not isinstance(property_dict, dict):
                raise TypeError("Invalid properties definition for '%s'" % (target_var,))

            encoded_catalogue = CATEGORY_COLUMN_PREFIX + target_var
            if encoded_catalogue not in self.encoded_column_names:
                self.__check_variables_options(property_dict.items(), target_var)
            else:
                self.__check_catalogues_options(target_var, encoded_catalogue, property_dict)
        self.__parse_optional_dictionary()

    def __check_catalogues_options(self, target_var, encoded_catalogue, property_dict):
        catalogue_properties_check = {
            self.__CATEGORY_LABEL: self.__check_string,
            self.__CATEGORY_SHAPE: self.__check_string,
            self.__CATEGORY_SIZE: self.__check_non_negative_number,
            self.__CATEGORY_BORDER: self.__check_non_negative_number,
            self.__CATEGORY_COLOR: self.__check_color,
            self.__CATEGORY_FILL_COLOR: self.__check_color
        }

        categories = self.__get_categories_for_catalogue(encoded_catalogue)
        for category, category_properties in property_dict.items():
            if not isinstance(category, str):
                raise TypeError("Invalid value '%s' for a category" % (category,))
            if category not in categories:
                raise ValueError("'%s' is not a category of '%s'" % (category, target_var))
            for property_name, property_value in category_properties.items():
                if not isinstance(property_name, str):
                    raise TypeError("'%s' is not a valid  category property" % (property_name,))

                if property_name not in self.__CATALOGUE_KEYS:
                    raise ValueError("'%s' is not a category of '%s'" % (property_name, encoded_catalogue[4:]))

                catalogue_properties_check[property_name](property_name, property_value)

    def __check_string(self, property_name, property_value):
        if not (property_value is None or isinstance(property_value, str)):
            raise TypeError("'%s' is not a valid %s" % (property_value, property_name))

    def __check_non_negative_number(self, property_name, property_value):
        self.__check_number(property_name, property_value)
        if property_value is not None and property_value < 0:
            raise ValueError("'%s' is not a valid %s" % (property_value, property_name))
        
    def __check_number(self, property_name, property_value):
        if not (property_value is None or self.__is_valid_number(property_value)):
            raise TypeError("'%s' is not a valid %s" % (property_value, property_name))

    def __check_color(self, property_name, property_value):
        if property_value is None:
            return
        if not self.__is_valid_color_type(property_value):
            raise TypeError("'%s' is not a valid %s (must be a string or a tuple)" % (property_value, property_name))
        if not self.__is_valid_color_value(property_value):
            raise ValueError("'%s' is not a valid %s" % (property_value, property_name))

    def __is_valid_color_type(self, value):
        return isinstance(value, str) or self.__is_tuple_like(value)

    def __is_tuple_like(self, value):
        try:
            tuple(value)
            return True
        except:
            return False

    def __is_valid_color_value(self, value):
        if isinstance(value, str):
            return re.match(r"#[\da-fA-F]{3,4}", value)
        else:
            n = len(value)
            return (n == 3 or n == 4) and all([self.__is_valid_number(i) for i in value])

    def __is_valid_number(self, value):
        return isinstance(value, numbers.Number)

    def __get_categories_for_catalogue(self, encoded_catalogue):
        return set(self.__get_column(self.encoded_column_names.index(encoded_catalogue)))

    def __check_variables_options(self, properties, target_var):
        for property_name, property_value in properties:
            if not isinstance(property_name, str):
                raise TypeError("'%s' is not a valid property" % (property_name,))
            if property_name not in self.__ALL_PARAMETER_KEYS:
                raise ValueError("'%s' is not a valid property" % (property_name,))
            input_properties = (self.__TYPE_KEY, self.__DEFAULT_VALUE_KEY, self.__BOUNDS_KEY, self.__BASE_KEY)
            if property_name in input_properties and not self.__is_input_var(target_var):
                raise ValueError("Invalid property '%s' for variable '%s'" % (property_name, target_var))
            self.__check_property_values(property_name, property_value)

    def __check_property_values(self, name, value):
        error_message = "Invalid value '%s' for property '%s'" % (value, name)

        if name in {self.__FORMAT_KEY, self.__DESCRIPTION_KEY, self.__TYPE_KEY} \
                and not isinstance(value, str):
            raise TypeError(error_message)

        if name == self.__TYPE_KEY and value not in self.__VALID_TYPES:
            raise ValueError(error_message)

        if name == self.__DEFAULT_VALUE_KEY and not self.__is_valid_number(value):
            raise TypeError(error_message)

        if name == self.__BOUNDS_KEY:
            self.__check_bounds(value)

        if name == self.__BASE_KEY:
            if not isinstance(value, int):
                raise TypeError(error_message)
            if value < 0:
                raise ValueError(error_message)

    def __check_bounds(self, value):
        try:
            bounds = tuple(value)
        except:
            raise TypeError("Invalid bounds '%s'" % (value,))
        if len(bounds) != 2:
            raise ValueError("Invalid length for bounds '%s'" % (value,))
        if not (self.__is_valid_number(bounds[0]) and self.__is_valid_number(bounds[1])):
            raise TypeError("Invalid bounds '%s'" % (value,))

        
    def __is_input_var(self, target_var):
        return INPUT_COLUMN_PREFIX + target_var in self.encoded_column_names

    def __parse_optional_dictionary(self):
        if self.optional_properties is not None:
            for variable_dict in self.optional_properties.values():
                if self.__BOUNDS_KEY in variable_dict.keys():
                    try:
                        variable_dict[self.__BOUNDS_KEY] = tuple(variable_dict[self.__BOUNDS_KEY])
                    except:
                        raise ValueError("Invalid bounds definition '%s'" % (variable_dict[self.__BOUNDS_KEY],))

    def __check_objectives(self):
        if not isinstance(self.objectives, dict):
            raise TypeError("Invalid objectives format")
        for obj_name, obj_dict in self.objectives.items():
            if not isinstance(obj_name, str):
                raise TypeError("Invalid type for objective name")
            if not isinstance(obj_dict, dict):
                raise TypeError("Invalid format for objective '%s' properties" % (obj_name,))
            self.__parse_objective_properties(obj_dict)

    def __parse_objective_properties(self, obj_dict):
        missing_obj_properties = [prop for prop in self.__MANDATORY_OBJECTIVE_KEYS if prop not in obj_dict]
        if missing_obj_properties:
            raise RuntimeError("Missing objective properties: '%s'" % ("', '".join(missing_obj_properties),))
        for property_name, property_value in obj_dict.items():
            if property_name not in self.__ALL_OBJECTIVE_KEYS:
                raise ValueError("'%s' is not a valid objective property" % (property_name,))
            if property_name == self.__OBJECTIVE_TYPE_KEY and property_value not in self.__OBJECTIVE_TYPES or \
                    not isinstance(property_value, str):
                raise ValueError("Invalid value '%s' for objective property '%s'" % (property_value, property_name))

    def __check_constraints(self):
        if not isinstance(self.constraints, dict):
            raise TypeError("Invalid constraints format")
        for constr_name, constr_dict in self.constraints.items():
            if not isinstance(constr_name, str):
                raise TypeError("Invalid type for constraint name")
            if not isinstance(constr_dict, dict):
                raise TypeError("Invalid format for constraint '%s' properties" % (constr_name,))
            self.__parse_constraints_properties(constr_dict)

    def __parse_constraints_properties(self, constr_dict):
        missing_constr_properties = [prop for prop in self.__MANDATORY_CONSTRAINT_KEYS if prop not in constr_dict]
        if missing_constr_properties:
            raise RuntimeError("Missing constraint properties: '%s'" % ("', '".join(missing_constr_properties),))
        string_properties = (self.__CONSTRAINT_EXPRESSION_KEY, self.__CONSTRAINT_FORMAT_KEY, self.__CONSTRAINT_DESCRIPTION_KEY)
        for property_name, property_value in constr_dict.items():
            if property_name not in self.__ALL_CONSTRAINT_KEYS:
                raise ValueError("'%s' is not a valid constraint property" % (property_name,))
            if property_name == self.__CONSTRAINT_TYPE_KEY and property_value not in self.__CONSTRAINT_TYPES or \
                    property_name == self.__CONSTRAINT_TOLERANCE_KEY and not self.__is_valid_number(property_value) or \
                    property_name == self.__CONSTRAINT_LIMIT_KEY and not self.__is_valid_number(property_value) or \
                    property_name in string_properties and not isinstance(property_value, str):
                raise ValueError("Invalid value '%s' for constraint property '%s'" % (property_value, property_name))

    def __check_expressions(self):
        if not isinstance(self.expressions, dict):
            raise TypeError("Invalid expressions format")
        for expr_name, expr_dict in self.expressions.items():
            if not isinstance(expr_name, str):
                raise TypeError("Invalid type for expression name")
            if not isinstance(expr_dict, dict):
                raise TypeError("Invalid format for expression '%s' properties" % (expr_name,))
            self.__parse_expression_properties(expr_dict)

    def __parse_expression_properties(self, expr_dict):
        if self.__EXPRESSION_EXPRESSION_KEY not in expr_dict:
            raise RuntimeError("Missing expression property: '%s'" % (self.__EXPRESSION_EXPRESSION_KEY,))
        for property_name, property_value in expr_dict.items():
            if property_name not in (self.__EXPRESSION_EXPRESSION_KEY, self.__EXPRESSION_FORMAT_KEY, self.__EXPRESSION_DESCRIPTION_KEY):
                raise ValueError("'%s' is not a valid expression property" % (property_name,))
            if not isinstance(property_value, str):
                raise ValueError("Invalid value '%s' for expression property '%s'" % (property_value, property_name))

    def build(self):
        spec = {INPUTS_KEY: {},
                OUTPUTS_KEY: {},
                CATEGORIES_KEY: {}}
        for index, name in enumerate(self.encoded_column_names):
            variable_added = self.__add_fixed_field_to_spec(spec, index, name) \
                             or self.__add_variable_to_spec(spec, index, name) \
                             or self.__add_category_to_spec(spec, index, name)
            if not variable_added:
                raise RuntimeError("unexpected row name")
        if self.optional_properties:
            self.__add_optional_properties_to_spec(spec)
        if self.objectives:
            spec[self.__OBJECTIVES_KEY] = self.objectives
        if self.constraints:
            spec[self.__CONSTRAINTS_KEY] = self.constraints
        if self.expressions:
            spec[self.__EXPRESSIONS_KEY] = self.expressions
        return _db.create_table(self.table_name, spec)

    def __add_fixed_field_to_spec(self, spec, index, name):
        """Return whether more processing is necessary for the column."""
        if name == ID_COLUMN_NAME:
            spec[ID_KEY] = self.__get_column(index)
            return True

        if name == MARKED_COLUMN_NAME:
            spec[MARKED_KEY] = self.__get_column(index)
            return True

        if name == VIRTUAL_COLUMN_NAME:
            spec[VIRTUAL_KEY] = self.__get_column(index)
            return True

        return False

    def __add_variable_to_spec(self, spec, index, name):
        input_name = self.__get_column_name(name, INPUT_COLUMN_PREFIX)
        if input_name:
            input = {DATA_KEY: self.__get_column(index)}
            spec[INPUTS_KEY][input_name] = input
            return True

        output_name = self.__get_column_name(name, OUTPUT_COLUMN_PREFIX)
        if output_name:
            output = {DATA_KEY: self.__get_column(index)}
            spec[OUTPUTS_KEY][output_name] = output
            return True

        return False

    def __add_category_to_spec(self, spec, index, name):
        catalogue_name = self.__get_column_name(name, CATEGORY_COLUMN_PREFIX)
        if catalogue_name:
            catalogue = {}
            names = self.__get_column(index)
            catalogue[self.__CATEGORY_NAMES_KEY] = names
            if self.optional_properties and catalogue_name in self.optional_properties:
                categories = self.__get_categories_for_catalogue(CATEGORY_COLUMN_PREFIX + catalogue_name)
                catalogue[self.__CATEGORY_LABELS_KEY] = self.__build_labels(self.optional_properties[catalogue_name], categories)
                catalogue[self.__CATEGORY_SYMBOLS_KEY] = self.__build_symbol_strings(self.optional_properties[catalogue_name], categories)
            else:
                catalogue[self.__CATEGORY_LABELS_KEY] = {}
                catalogue[self.__CATEGORY_SYMBOLS_KEY] = {}
            spec[CATEGORIES_KEY][catalogue_name] = catalogue
            return True

        return False

    def __build_labels(self, catalogue_properties, categories):
        results = {}
        for category in categories:
            label = catalogue_properties.get(category, {}).get(self.__CATEGORY_LABEL, None)
            if label:
                results[category] = label
        return results

    def __build_symbol_strings(self, catalogue_properties, categories):
        results = {}
        for category in categories:
            category_properties = catalogue_properties.get(category, {}).copy()
            if self.__CATEGORY_LABEL in category_properties:
                del (category_properties[self.__CATEGORY_LABEL])
            if len(category_properties) != 0:
                shape = self.__ensure_shape(category_properties.get(self.__CATEGORY_SHAPE, None) or self.__DEFAULT_SHAPE)
                size = self.__ensure_number("size", category_properties.get(self.__CATEGORY_SIZE, None) or self.__DEFAULT_SIZE)
                color = self.__convert_color(category_properties.get(self.__CATEGORY_COLOR, None) or self.__DEFAULT_COLOR)
                border = self.__ensure_number("border", category_properties.get(self.__CATEGORY_BORDER, None) or self.__DEFAULT_BORDER)
                raw_fill_color = category_properties.get(self.__CATEGORY_FILL_COLOR, None) or self.__DEFAULT_FILL_COLOR
                if raw_fill_color:
                    fill_color = self.__convert_color(raw_fill_color)
                    results[category] = "%s,NONE,%s,%s,%s,%s" % (shape, size, color, border, fill_color)
                else:
                    results[category] = "%s,NONE,%s,%s,%s" % (shape, size, color, border)
        return results

    def __ensure_shape(self, user_definition):
        if Shapes.is_valid_shape(user_definition):
            return user_definition
        else:
            message = "Invalid shape definition: '%s'" % (user_definition,)
            raise ValueError(message)

    def __ensure_number(self, field_name, user_definition):
        try:
            return max(0, int(user_definition))
        except:
            message = "Invalid %s definition: '%s'" % (field_name, user_definition)
            raise ValueError(message) from None

    def __convert_color(self, user_definition):
        if isinstance(user_definition, str):
            return self.__ensure_css_color(user_definition)
        else:
            try:
                return self.__color_to_CSS_color(user_definition)
            except:
                message = "Invalid color definition: '%s'" % (user_definition,)
                raise ValueError(message) from None

    def __ensure_css_color(self, user_definition):
        length = len(user_definition)
        if user_definition.startswith("#") and (length == 7 or length == 9):
            return user_definition
        else:
            raise ValueError("Invalid color definition: '%s'" % (user_definition,))

    def __color_to_CSS_color(self, rgb):
        clipped_components = [min(255, max(0, i)) for i in rgb]
        if len(clipped_components) == 3:
            format_string = "#{:02x}{:02x}{:02x}"
        else:
            format_string = "#{:02x}{:02x}{:02x}{:02x}"
        return format_string.format(*clipped_components)

    def __add_optional_properties_to_spec(self, spec):
        inputs = spec[INPUTS_KEY]
        outputs = spec[OUTPUTS_KEY]
        for variable_name, property_dict in self.optional_properties.items():
            if (CATEGORY_COLUMN_PREFIX + variable_name) not in self.encoded_column_names:
                if variable_name in inputs.keys():
                    self.__add_property_to_spec_dict(inputs[variable_name], property_dict)
                elif variable_name in outputs.keys():
                    self.__add_property_to_spec_dict(outputs[variable_name], property_dict)
                else:
                    raise ValueError("'%s' is not an input variable or an output variable" % (variable_name,))

    def __add_property_to_spec_dict(self, variable, property_dict):
        for property_name, property_value in property_dict.items():
            variable[property_name] = property_value

    def __get_column(self, index):
        return tuple([i[index] for i in self.rows])

    def __get_column_name(self, name, prefix):
        prefix_length = len(prefix)
        if name[:prefix_length] == prefix:
            return name[prefix_length:].strip()


def create_table(table_name, encoded_column_names, rows, optional_properties=None,
                 objectives=None, constraints=None, expressions=None):
    """Creates table in Design Space.

table_name
  name of the new table. Duplicated names are not allowed.
encoded_column_names
  variable type encoding followed by variable name (see example
  below). Columns require different value formats based on their type:


  Name        Description       Format
  ==================================================
  id          design ID         non-negative integer
  marked      "mark" status     boolean
  virtual     "virtual" status  boolean
  cat:<name>  a catalogue       string
  in:<name>   input variable    scalar
  out:<name>  output variable   scalar

rows
  list of values in the format required by the corresponding column
  type (see column encoding above). Each row is a design. Number of
  values in a row has to correspond to the number of columns.

optional_properties
  dictionary with optional properties to add to the table.

  There are two kind of properties: variable properties and catalogue
  properties.
    
  Valid variable properties are:

    Name             Description           Format
    ==========================================================
    bounds           variable bounds       list of two scalars
    default_value    default value         scalar
    type             variable type         string
      variable   (optional)
      constant   (requires 'default_value' key)
    base             variable base         integer
    format           variable format       string
    description      variable description  string

  Valid catalogue properties are:

    Name          Description          Format
    ===================================================
    label        category label        string
    size         symbol size           scalar
    border       symbol border width   scalar
    shape        symbol shape          any shape declared in db.Shapes
    color        symbol border color   RGB/RGBA or HEX string
    fill_color   symbol fill color     RGB/RGBA or HEX string

objectives
  dictionary with the objectives to add to the table.

  Valid objective properties are:

    Name          Description            Format
    ==================================================
    type          objective type         'maximize' or 'minimize'
    expression    objective expression   string
    format        objective format       string
    description   objective description  string

constraints
  dictionary with the constraints to add to the table.

  Valid constraint properties are:

    Name          Description             Format
    ==================================================
    type          constraint type         'less than', 'equal to'
                                            or 'greater than'
    tolerance     constraint tolerance    double
    limit         constraint limit        double
    expression    constraint expression   string
    format        constraint format       string
    description   constraint description  string

expressions
  dictionary with the expressions to add to the table.

  Valid expression properties are:

    Name          Description             Format
    ==================================================
    expression    expression expression   string
    format        expression format       string
    description   expression description  string

Example:

from estecopy import db
from estecopy.db import Shapes

objectives = {"obj1": {"type": "maximize", "expression": "input1", "format": "%2.5g", "description": "objective"},
              "obj2": {"type": "minimize", "expression": "input1 + output1"}}  
constraints = {"const1": {"type": "less than", "tolerance": 16.0, "limit": 7.0, "expression": "input1 + input2", "format": "%2g", "description": "constraint"},
               "const2": {"type": "greater than", "tolerance": 167.0, "limit": 78.0, "expression": "output1 + output2"},
               "const3": {"type": "equal to", "tolerance": 67.0, "limit": -12.0, "expression": "output1 - output2", "format": "%5g"}}
expressions = {"expr1": {"expression": "output1"},
               "expr2": {"expression": "input1 - output1", "format": "%2g", "description": "expression"}}

db.create_table('my_table',
        ['id', 'cat:color', 'in:input1', 'in:input2', 'out:output1', 'out:output2', 'marked'],
        [[3,   'red',        1.3,         1,           0.9,           -1.3,          True],
         [5,   'red',        2,           2,           1.5,           2.3,           False],
         [6,   'blue',       3.6,         3,           0.1,           -2,            False],
         [7,   'green',      4.1,         4,           3.2,           1,             True]],
         {"input1": {"type": "constant", "default_value": 12, "base": 1, "format": "%g", "description": "input"},
          "output1": {"format": "%g", "description": "output"},
          "color": {"red" : {
                             "shape" : Shapes.SQUARE,
                             "color" : "#FF0000",
                             "fill_color" : "#ff8888",
                             "size" : 15,
                             "border" : 2
                            },
                    "green" : {
                             "label" : "GR",
                             "fill_color" : "#88ff88",
                            }}},
          objectives=objectives, constraints=constraints, expressions=expressions)

creates a table called my_table with 1 catalogue, 2 input variables, 2 output variables,
2 objectives, 3 constraints, 2 expressions and 4 designs. The ID sequence is custom.
The first and the last designs are marked.

    """
    builder = _EncodedHeaderTableBuilder(table_name, encoded_column_names, rows, optional_properties,
                                         objectives, constraints, expressions)
    builder.check()
    return builder.build()


class __SimpleTableBuilder(__TableDataChecker):

    def __init__(self, table_name, column_names, rows, optional_properties=None):
        self.optional_properties = optional_properties
        self.table_name = table_name
        self.column_names = column_names
        self.rows = rows

    def check(self):
        self._check_columns(self.column_names)
        self._check_rows(self.column_names)

    def build_input_table(self):
        builder = _EncodedHeaderTableBuilder(self.table_name, [INPUT_COLUMN_PREFIX + i for i in self.column_names], self.rows, self.optional_properties)
        builder.check()
        return builder.build()

    def build_output_table(self):
        builder = _EncodedHeaderTableBuilder(self.table_name, [OUTPUT_COLUMN_PREFIX + i for i in self.column_names], self.rows, self.optional_properties)
        builder.check()
        return builder.build()


def create_input_table(table_name, column_names, rows, optional_properties=None):
    """Creates table with only input variables in Design Space.

table_name
  name of the new table. Duplicated names are not allowed.

column_names
  list of input names in string format

rows
  a row (design) consists of a list/tuple of values, where each value
  is the value of this design in a variable. Number of values in a row
  has to correspond to the number of columns.

optional_properties
  dictionary with optional properties to add to the table.
  See description for method create_table.

Returns the name of the new table.

Example:

from estecopy import db

db.create_input_table("input_table",
                       ["x1", "x2"],
                       [[1, 2], [2, 4], [3, 6], [4, 8]],
                       {"x2":{"bounds" : [-10,10], "default_value": 10},
                       "x1": {"type": "constant", "default_value": 12, "base": 1, "format": "%h", "description": "input"}})
    """
    builder = __SimpleTableBuilder(table_name, column_names, rows, optional_properties)
    builder.check()
    return builder.build_input_table()


def create_output_table(table_name, column_names, rows, optional_properties=None):
    """Creates table with only output variables in Design Space.

See description for method create_input_table.

Example:

from estecopy import db

db.create_output_table("output_table",
                        ["f1", "f2"],
                        [[1, 2], [2, 4], [3, 6], [4, 8]],
                        {"f2": {"format": "%h"},
                        "f1": {"format": "%f", "description": "output1"}})
"""
    builder = __SimpleTableBuilder(table_name, column_names, rows, optional_properties)
    builder.check()
    return builder.build_output_table()


class _ProgressLoader:
    __PERCENT_INTERVAL = 5

    def __init__(self, name):
        self.__name = name
        self.__tmp_data = []

    def load_table(self):
        self.__print("Loading '%s'" % (self.__name,))
        _db.supply_table_rows(self.__name, self.__append_row)
        data = {
            NAME_KEY: self.__name,
            METADATA_KEY: _db.get_table_metadata(self.__name),
            ROWS_KEY: self.__tmp_data
        }
        self.__print("\rLoading 100%%...")
        self.__print("Done.")
        return data

    def __print(self, string):
        print(string)

    def __append_row(self, count, row):
        interval = math.ceil(count * self.__PERCENT_INTERVAL / 100)
        self.__tmp_data.append(row)
        if interval > 0 and len(self.__tmp_data) % interval == 0:
            current_percent = 100 * len(self.__tmp_data) / count
            sys.stdout.write("\rLoading %d%%..." % current_percent)


class DesignTable:
    """This class represents a table loaded to pyCONSOLE from the Design Space.

To load a table use the method db.get_table(tableName).
"""

    __GOALS_KEY = "goals"
    __INPUTS_KEY = "input_variables"
    __INPUT_LOWER_BOUND_KEY = "lower_bound"
    __INPUT_UPPER_BOUND_KEY = "upper_bound"
    __OUTPUTS_KEY = "output_variables"
    __CONSTRAINTS_KEY = "constraints"
    __OBJECTIVES_KEY = "objectives"
    __EXPRESSIONS_KEY = "trans_variables"
    __ALL_VARIABLES_TYPES_KEYS = (__INPUTS_KEY, __OUTPUTS_KEY, __CONSTRAINTS_KEY, __OBJECTIVES_KEY, __EXPRESSIONS_KEY)
    __USER_TYPE_FOR_VARIABLE_TYPE_KEY = {__INPUTS_KEY: "input",
                                         __OUTPUTS_KEY: "output",
                                         __CONSTRAINTS_KEY: "constraint",
                                         __OBJECTIVES_KEY: "objective",
                                         __EXPRESSIONS_KEY: "expression"}

    __IS_VECTOR_COMPONENT_PROPERTY_KEY = "is_vector_component"
    __VECTOR_ID_PROPERTY_KEY = "vector_id"
    __DEFAULT_VALUE_KEY = "default_value"
    __INPUT_TYPE_KEY = "type"
    __INPUT_TYPES = ["variable", "constant", "expression"]
    __TOLERANCE_KEY = "tolerance"
    __EXPRESSION_KEY = "expression"
    __LIMIT_KEY = "limit"
    __CONSTRAINT_TYPE_KEY = "type"
    __CONSTRAINT_TYPES = ["greater than", "equal to", "less than"]
    __OBJECTIVE_TYPE_KEY = "type"
    __MINIMIZE_OBJECTIVE_TYPE = "minimize"
    __MAXIMIZE_OBJECTIVE_TYPE = "maximize"
    __FORMAT_KEY = "format"
    __DESCRIPTION_KEY = "description"
    __BASE_KEY = "base"
    __STEP_KEY = "step"

    __CATALOGUES_KEY = "catalogues"
    __CATALOGUE_NAME = "name"
    __CATEGORIES_KEY = "categories"
    __CATEGORY_NAME_KEY = "name"
    __CATEGORY_LABEL_KEY = "label"
    __CATEGORY_TITLE_KEY = "title"
    __CATEGORY_SYMBOL_KEY = "symbol"
    __CATEGORY_SYMBOL_SHAPE_KEY = "shape"
    __CATEGORY_SYMBOL_IGNORED_BORDER_KEY = "border"
    __CATEGORY_SYMBOL_SIZE_KEY = "size"
    __CATEGORY_SYMBOL_COLOR_KEY = "color"
    __CATEGORY_SYMBOL_BORDER_KEY = "border"
    __CATEGORY_SYMBOL_FILL_COLOR_KEY = "fill_color"

    __TYPE_PROPERTY = "type"
    __TYPE_PROPERTY_INPUT = "input"
    __TYPE_PROPERTY_OUTPUT = "output"
    __TYPE_PROPERTY_OBJECTIVE = "objective"
    __TYPE_PROPERTY_CATEGORY = "category"
    __TYPE_PROPERTY_EXPRESSION = "expression"
    __CATALOGUE_NAMES_PROPERTY = "names"
    __CATALOGUE_LABELS_PROPERTY = "labels"
    __CATALOGUE_TITLES_PROPERTY = "titles"
    __CATALOGUE_SYMBOLS_PROPERTY = "symbols"
    __BOUNDS_PROPERTY = "bounds"
    __VECTOR_INDEX_PROPERTY = "vector_index"
    __DEFAULT_VALUE_PROPERTY = "default_value"
    __INPUT_TYPE_PROPERTY = "input_type"
    __EXPRESSION_PROPERTY = "expression"
    __LIMIT_PROPERTY = "limit"
    __TOLERANCE_PROPERTY = "tolerance"
    __OBJECTIVE_TYPE_PROPERTY = "objective_type"
    __CONSTRAINT_TYPE_PROPERTY = "constraint_type"
    __FORMAT_PROPERTY = "format"
    __DESCRIPTION_PROPERTY = "description"
    __BASE_PROPERTY = "base"
    __STEP_PROPERTY = "step"

    def __init__(self, name, show_progress=True, preload_linked_table=True, show_robust_ids=False):
        self.__show_progress = show_progress
        self.__show_robust_ids = show_robust_ids
        self.__linked_table = None
        self.__name = name
        self.__load_table(name, preload_linked_table)

    def __dir__(self):
        return [i for i in DesignTable.__dict__.keys() if not i.startswith("_DesignTable__")]

    def __get_metadata_linked_table_name(self):
        return self.__raw_data[METADATA_KEY][LINKED_SESSION_TABLE_NAME_KEY]

    def __is_robust(self):
        return self.__get_metadata_linked_table_name() is not None

    def get_linked_table_name(self):
        """Returns the name of the work or session table that the robust table is linked to.

It will return 'None' for any other type of table."""
        # Use the actual linked table as the single reputable source
        # of information for the name.
        # Relevant for preload_linked_table = False followed by mF tables changes
        if self.__is_robust():
            return self.get_linked_table().get_name()

    def get_linked_table(self):
        """Returns the work or the session table that the robust table is linked to.

The argument show_robust_ids (explained in the context of the
get_table method) is True by default. It means that the designs in the
loaded table are loaded with their RIDs.

It will return 'None' for any other type of table.
"""
        if not self.__linked_table:
            linked_table_name = self.__get_metadata_linked_table_name()
            if linked_table_name:
                self.__linked_table = DesignTable(linked_table_name, self.__show_progress, preload_linked_table=False, show_robust_ids=True)
        return self.__linked_table

    def __load_table(self, name, preload_linked_table):
        if self.__show_progress:
            loader = _ProgressLoader(name)
            self.__raw_data = loader.load_table()
        else:
            self.__raw_data = _db.get_table_data(name)

        if preload_linked_table:
            self.get_linked_table()

    def get_name(self):
        """Returns table name."""
        return self.__name

    def __create_robust_header_row(self):
        header = [RID_KEY, MARKED_KEY, VIRTUAL_KEY]
        header.extend(self.__get_catalogue_names())
        header.extend(self.__raw_data[METADATA_KEY][COLUMN_NAMES_KEY])
        return tuple(header)

    def __create_robust_header_with_ids_row(self):
        header = [RID_KEY, IDS_KEY, MARKED_KEY, VIRTUAL_KEY]
        header.extend(self.__get_catalogue_names())
        header.extend(self.__raw_data[METADATA_KEY][COLUMN_NAMES_KEY])
        return tuple(header)

    def _create_plain_header_row(self):
        header = [ID_KEY, MARKED_KEY, VIRTUAL_KEY]
        header.extend(self.__get_catalogue_names())
        header.extend(self.__raw_data[METADATA_KEY][COLUMN_NAMES_KEY])
        return tuple(header)

    def __create_plain_meta_columns(self, meta):
        return [meta[ID_KEY], meta[MARKED_KEY], meta[VIRTUAL_KEY]]

    def __create_meta_columns_with_ids(self, meta):
        return [meta[ID_KEY], meta[IDS_KEY], meta[MARKED_KEY], meta[VIRTUAL_KEY]]

    def __create_linked_robust_header_row(self):
        header = [ID_KEY, RID_KEY, MARKED_KEY, VIRTUAL_KEY]
        header.extend(self.__get_catalogue_names())
        header.extend(self.__raw_data[METADATA_KEY][COLUMN_NAMES_KEY])
        return tuple(header)

    def __create_linked_robust_meta_columns(self, meta):
        try:
            rid = meta[IDS_KEY][0]
        except KeyError:
            rid = None
        return [meta[ID_KEY], rid, meta[MARKED_KEY], meta[VIRTUAL_KEY]]

    def __index_row(self):
        index = {}
        linked_rows = self.get_linked_table()._get_rows(False)
        assert (linked_rows[0][0] == "id")
        assert (linked_rows[0][1] != "rid")
        for row in linked_rows[1:]:
            index[row[0]] = row
        return index

    def __extract_robust_designs(self, set_header, linked_index, ids):
        subtable = [set_header]
        for id in ids:
            try:
                subtable.append(linked_index[id])
            except KeyError:
                subtable.append(None)
        return tuple(subtable)

    def __extract_row(self, raw_row, row_reader):
        meta = raw_row[1]
        row_metadata = row_reader(meta)
        categories = self.__decode_categories(meta[CATEGORIES_KEY])
        return tuple(row_metadata + categories + list(raw_row[0]))

    def get_robust_rows(self):
        """Returns table as a sequence of nominal design rows, each followed by its robust samples.

The first row contains column names.

All other rows are pairs of nominal designs and the associated robust samples subtables.

The subtables are analogous to those returned by the get_rows method.
"""
        if not self.__is_robust():
            raise RuntimeError("this method cannot be invoked on non-robust tables")
        else:
            linked_index = self.__index_row()
            set_linked_header = self.get_linked_table()._create_plain_header_row()
            new_rows = [self.__create_robust_header_row()]
            for raw_row in self.__raw_data[ROWS_KEY]:
                header_row = self.__extract_row(raw_row, self.__create_plain_meta_columns)
                ids_tuple = raw_row[1][IDS_KEY]
                sub_table = self.__extract_robust_designs(set_linked_header, linked_index, ids_tuple)
                new_rows.append((header_row, sub_table))
            return tuple(new_rows)

    def __has_extra_ids(self):
        try:
            return len(self.__raw_data[ROWS_KEY][0][1][IDS_KEY]) > 0
        except (IndexError, TypeError):
            return False

    def __create_rows_header(self, show_robust_ids):
        if self.__is_robust():
            if show_robust_ids:
                return self.__create_robust_header_with_ids_row()
            else:
                return self.__create_robust_header_row()
        else:
            if show_robust_ids and self.__has_extra_ids():
                return self.__create_linked_robust_header_row()
            else:
                return self._create_plain_header_row()

    def __create_row_reader(self, show_robust_ids):
        if self.__is_robust():
            if show_robust_ids:
                return self.__create_meta_columns_with_ids
            else:
                return self.__create_plain_meta_columns
        else:
            if show_robust_ids and self.__has_extra_ids():
                return self.__create_linked_robust_meta_columns
            else:
                return self.__create_plain_meta_columns

    def _get_rows(self, show_robust_ids):
        row_reader = self.__create_row_reader(show_robust_ids)
        data = []
        for raw_row in self.__raw_data[ROWS_KEY]:
            data.append(self.__extract_row(raw_row, row_reader))
        data.insert(0, self.__create_rows_header(show_robust_ids))
        return tuple(data)

    def __get_catalogues(self):
        return self.__raw_data[METADATA_KEY][self.__CATALOGUES_KEY]

    def get_rows(self):
        """Returns table as a sequence of rows.

The first row contains column names.

All other rows are designs.

Design ID, RID/robust samples (optionally, if the table was created with
show_robust_ids) whether a design is marked or not and whether a design is
virtual or real are indicated in columns "id", "rid"/"ids", "marked"
and "virtual" respectively.
"""
        return self._get_rows(self.__show_robust_ids)

    def __get_catalogue_names(self):
        return [i[NAME_KEY] for i in self.__get_catalogues()]

    def __decode_categories(self, categories):
        raw_catalogues = self.__get_catalogues()
        names = []
        for catalogue_index, category_index in enumerate(categories):
            if category_index != -1:
                catalogue = raw_catalogues[catalogue_index]
                category = catalogue[CATEGORIES_KEY][category_index]
                row_category = category[NAME_KEY]
            else:
                row_category = None
            names.append(row_category)
        return names

    def __get_goals(self):
        return self.__raw_data[METADATA_KEY][self.__GOALS_KEY]

    def __raise_not_a_variable_error(self, name):
        raise ValueError("'%s' is not a variable" % (name,))

    def __get_type_property(self, name):
        goals = self.__get_goals()
        for type_key in self.__ALL_VARIABLES_TYPES_KEYS:
            var_group = goals[type_key]
            if name in var_group:
                return self.__USER_TYPE_FOR_VARIABLE_TYPE_KEY[type_key]
        self.__raise_not_a_variable_error(name)

    def __get_bounds_property(self, name):
        input = self.__get_input_variable_or_throw(name)
        return input[self.__INPUT_LOWER_BOUND_KEY], input[self.__INPUT_UPPER_BOUND_KEY]

    def __get_all_variables(self):
        all_variables = dict()
        goals = self.__get_goals()
        for var_type_key in self.__ALL_VARIABLES_TYPES_KEYS:
            all_variables.update(goals[var_type_key])
        return all_variables

    def get_variables(self):
        """Returns the list of variables in the table."""
        return set(self.__get_all_variables())

    def get_catalogues(self):
        """Returns the list of catalogues in the table."""
        return set(self.__get_catalogue_names())

    def __get_variable(self, name):
        all_variables = self.__get_all_variables()
        if not name in all_variables:
            self.__raise_not_a_variable_error(name)
        return all_variables[name]

    def __get_vector_index_property(self, name):
        variable = self.__get_variable(name)
        if not variable[self.__IS_VECTOR_COMPONENT_PROPERTY_KEY]:
            return None
        else:
            return variable[self.__VECTOR_ID_PROPERTY_KEY]

    def __get_input_type_property(self, name):
        input = self.__get_input_variable_or_throw(name)
        try:
            return self.__INPUT_TYPES[input[self.__INPUT_TYPE_KEY]]
        except IndexError:
            raise ValueError("Unexpected type for input '%s'" % (name,))

    def __get_input_variable_or_throw(self, name):
        inputs = self.__get_goals()[self.__INPUTS_KEY]
        if not name in inputs:
            raise ValueError("'%s' is not an input variable" % (name,))
        return inputs[name]

    def get_variable_property(self, name, property):
        """Returns information about the specified variable, if available.

If the name is not associated to a variable, the function will raise a
ValueError.

Asking for a property unavailable for the specified variable will raise
a ValueError.

Valid properties are:

"type" - returns the type of the variable.

  It can be applied to all variables. It can return one of the following
  values: "input", "output", "objective", "constraint", "expression".

"bounds" - returns the lower and upper bound of a variable.

  It can be applied to input variables and returns a tuple with the
  lower and upper bounds of the variable.

"vector_index" - returns the index of a vector component, or None.

  It can be applied to all variables and returns the index of the specified
  vector component or 'None' for non-vector variables.

"default_value" - returns the default value.

  It can be applied to input variables and returns a float.

"input_type" - returns the type of the input variable.

  It can be applied to input variables and returns one of the following values:
  "variable", "constant", "expression" (the latter is only provided
  for compatibility reasons and will be deprecated).

"expression" - returns the expression of the variable.

  It can be applied to input variables, objectives, constraints and expressions and returns a string.

"limit" - returns the limit of a constraint.

  It can be applied to constraints and returns a float.

"tolerance" - returns the tolerance of a variable.

  It can be applied to input variables and constraints and returns a float.

"constraint_type" - returns the type of the constraint.

  It can be applied to constraints and returns one of the following values:
  "greater than", "equal to", "less than".

"objective_type" - returns the type of the objective.

  It can be applied to objectives and returns either "minimize" or "maximize".

"format" - returns the format of the variable.

  It can be applied to all types of variables and returns a string.

"description" - returns the description of the variable.

  It can be applied to all types of variables and returns a string.

"base" - returns the base of the input variable.

  It can be applied to input variables and returns an integer.

"step" - returns the step of the input variable.

  It can be applied to input variables and returns a float.

        """
        if not name in self.get_variables():
            raise ValueError("'%s' is not a variable" % (name,))
        if property == self.__TYPE_PROPERTY:
            return self.__get_type_property(name)
        elif property == self.__BOUNDS_PROPERTY:
            return self.__get_bounds_property(name)
        elif property == self.__VECTOR_INDEX_PROPERTY:
            return self.__get_vector_index_property(name)
        elif property == self.__DEFAULT_VALUE_PROPERTY:
            return self.__get_input_variable_or_throw(name)[self.__DEFAULT_VALUE_KEY]
        elif property == self.__INPUT_TYPE_PROPERTY:
            return self.__get_input_type_property(name)
        elif property == self.__EXPRESSION_PROPERTY:
            return self.__get_expression_property(name)
        elif property == self.__LIMIT_PROPERTY:
            return self.__get_limit_property(name)
        elif property == self.__TOLERANCE_PROPERTY:
            return self.__get_tolerance_property(name)
        elif property == self.__OBJECTIVE_TYPE_PROPERTY:
            return self.__get_objective_type_property(name)
        elif property == self.__CONSTRAINT_TYPE_PROPERTY:
            return self.__get_constraint_type_property(name)
        elif property == self.__FORMAT_PROPERTY:
            return self.__get_variable(name)[self.__FORMAT_KEY]
        elif property == self.__DESCRIPTION_PROPERTY:
            return self.__get_variable(name)[self.__DESCRIPTION_KEY]
        elif property == self.__BASE_PROPERTY:
            return self.__get_input_variable_or_throw(name)[self.__BASE_KEY]
        elif property == self.__STEP_PROPERTY:
            return self.__get_input_variable_or_throw(name)[self.__STEP_KEY]
        else:
            raise ValueError("'%s' is not a valid property" % (property,))

    def __get_expression_property(self, name):
        outputs = self.__get_goals()[self.__OUTPUTS_KEY]
        if name in outputs:
            raise ValueError("'%s' has to be an input variable, an objective or a constraint" % (name,))
        return self.__get_variable(name)[self.__EXPRESSION_KEY]

    def __get_limit_property(self, name):
        constraints = self.__get_goals()[self.__CONSTRAINTS_KEY]
        if not name in constraints:
            raise ValueError("'%s' is not a constraint" % (name,))
        return constraints[name][self.__LIMIT_KEY]

    def __get_tolerance_property(self, name):
        goals = self.__get_goals()
        vars = {**(goals[self.__CONSTRAINTS_KEY]), **(goals[self.__INPUTS_KEY])}
        if name not in vars:
            raise ValueError("'%s' is not an input variable or a constraint" % (name,))
        return vars[name][self.__TOLERANCE_KEY]

    def __get_constraint_type_property(self, name):
        constraints = self.__get_goals()[self.__CONSTRAINTS_KEY]
        if not name in constraints:
            raise ValueError("'%s' is not a constraint" % (name,))
        return self.__convert_constraint_type(constraints[name][self.__CONSTRAINT_TYPE_KEY], name)

    def __convert_constraint_type(self, type, name):
        try:
            return self.__CONSTRAINT_TYPES[type + 1]
        except IndexError:
            raise ValueError("Unexpected type for constraint '%s'" % (name,))

    def __get_objective_type_property(self, name):
        objectives = self.__get_goals()[self.__OBJECTIVES_KEY]
        if not name in objectives:
            raise ValueError("'%s' is not an objective" % (name,))
        return self.__convert_objective_type(objectives[name][self.__OBJECTIVE_TYPE_KEY], name)

    def __convert_objective_type(self, type, name):
        if type == 1:
            return self.__MAXIMIZE_OBJECTIVE_TYPE
        elif type == -1:
            return self.__MINIMIZE_OBJECTIVE_TYPE
        else:
            raise ValueError("Unexpected type for objective '%s'" % (name,))

    def get_catalogue_property(self, catalogue_name, property):
        """Returns information about the categories of the specified catalogue.

Specifying an invalid property or catalogue will raise an Exception.

Valid values for 'property' are:

"names" - returns a set with the names of all categories in the catalogue.

"labels" - returns a dictionary with the labels associated with each category.        

"titles" - returns a dictionary with the titles associated with each category.        

"symbols" - returns a dictionary with the symbols associated with each category.

  Each symbol is represented by a dictionary with the following keys: 'shape',
  'color', 'fill_color', 'size', and 'border'.

  'shape' can be any of the shapes returned by the 'get_valid_shapes' method
  in the db.Shapes class."""
        catalogues = dict([(i[self.__CATALOGUE_NAME], i) for i in self.__raw_data[METADATA_KEY][self.__CATALOGUES_KEY]])
        if catalogue_name not in catalogues:
            raise ValueError("'%s' is not a catalogue" % (catalogue_name,))
        categories = catalogues[catalogue_name][self.__CATEGORIES_KEY]
        if property == self.__CATALOGUE_LABELS_PROPERTY:
            return self.__get_catalogue_properties(categories, self.__CATEGORY_LABEL_KEY)
        elif property == self.__CATALOGUE_NAMES_PROPERTY:
            return set([i[self.__CATEGORY_NAME_KEY] for i in categories])
        elif property == self.__CATALOGUE_TITLES_PROPERTY:
            return self.__get_catalogue_properties(categories, self.__CATEGORY_TITLE_KEY)
        elif property == self.__CATALOGUE_SYMBOLS_PROPERTY:
            return self.__get_catalogue_symbols(categories)
        else:
            raise ValueError("'%s' is not a valid property" % (property,))

    def __get_catalogue_properties(self, categories, category_property_name, transform=lambda x: x):
        return dict([(category[self.__CATEGORY_NAME_KEY], transform(category[category_property_name]))
                     for category in categories])

    def __get_catalogue_symbols(self, categories):
        return self.__get_catalogue_properties(categories,
                                               self.__CATEGORY_SYMBOL_KEY,
                                               self.__encoded_symbol_to_dict)

    def __encoded_symbol_to_dict(self, symbol):
        fields = symbol.split(",")
        del (fields[1])  # don't expose the LINE field of the Symbol to the user
        fields[1] = int(fields[1])
        fields[3] = int(fields[3])
        result = dict(zip((self.__CATEGORY_SYMBOL_SHAPE_KEY,
                           self.__CATEGORY_SYMBOL_SIZE_KEY,
                           self.__CATEGORY_SYMBOL_COLOR_KEY,
                           self.__CATEGORY_SYMBOL_BORDER_KEY,
                           self.__CATEGORY_SYMBOL_FILL_COLOR_KEY),
                          fields))
        if self.__CATEGORY_SYMBOL_FILL_COLOR_KEY not in result:
            result[self.__CATEGORY_SYMBOL_FILL_COLOR_KEY] = None
        return result


def get_table(name, show_progress=True, show_robust_ids=False, preload_linked_table=True):
    """Returns a table of class 'DesignTable'

show_progress: print the progress of table loading
show_robust_ids: for robust and design tables, show the RIDs or the associated IDs of the designs, if present
preload_linked_table: for robust tables only, load the robust table and the associated design table

Lazy loading with 'preload_linked_table=False' should be used with
caution, as it may cause errors if the model is renamed in
modeFRONTIER.

    """
    arg_parse.ensure_correct_args(("name", "string", name), )
    return DesignTable(name, show_progress, preload_linked_table, show_robust_ids)


__all__ = ["get_version", "get_table_names", "create_table", "create_input_table", "create_output_table", "get_table", "DesignTable"]
