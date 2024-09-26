import json as json_module
import pyfrontier
import re
import ssl
import urllib
import urllib.request
from estecopy._internal.utils import locks
from estecopy._internal.utils import log
from estecopy._internal.utils import server_validation
from http import HTTPStatus

__current_connection = None


class Connection:
    __HTTP = "http"
    __HTTPS = "https"
    __REALM = "pyFRONTIER_guest_realm"
    __USERNAME = "pyFRONTIER_guest"

    def __init__(self):
        self.pyfrontier_config = pyfrontier._get_config()
        handlers = []
        protocol, context = self.__setup_https(handlers)
        self.__setup_base_address(protocol, context)
        self.__setup_authentication(handlers)
        self.__setup_opener(handlers)
        self.__connection_closed = False

    def __setup_https(self, handlers):
        if self.pyfrontier_config.is_secure_connection():
            context = self.__create_context()
            handlers.append(urllib.request.HTTPSHandler(context=context))
            return self.__HTTPS, context
        else:
            return self.__HTTP, None

    def __create_context(self):
        if self.pyfrontier_config.is_check_certificate():
            context = ssl.create_default_context(cafile=pyfrontier.get_ca_bundle_file())
            context.check_hostname = pyfrontier.is_check_hostname()
            return context
        else:
            return ssl._create_unverified_context()

    def __setup_base_address(self, protocol, context):
        if pyfrontier.get_port():
            host = pyfrontier.get_host()
            address, port = host if host else server_validation.get_localhost_address(), pyfrontier.get_port()
        else:
            address, port = server_validation.get_server_address(locks.get_ports(), protocol, context)
        self.__base_address = "%s://%s:%d" % (protocol, address, port)

    def __setup_authentication(self, handlers):
        password = pyfrontier.get_connection_password()
        if password:
            password_mgr = urllib.request.HTTPPasswordMgr()
            password_mgr.add_password(self.__REALM, self.__base_address, self.__USERNAME, password)
            auth_handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
            handlers.append(auth_handler)

    def __setup_opener(self, handlers):
        opener = urllib.request.build_opener(*handlers)
        urllib.request.install_opener(opener)

    def __is_server_closed(self, url_error):
        return type(url_error.reason) == ConnectionRefusedError and url_error.reason.errno == 111

    def __get_encoded_parameters(self, query_parameters):
        encoded_query = urllib.parse.urlencode(query_parameters)
        return encoded_query and "?" + encoded_query

    def __get_urlencoded_address(self, path, query_parameters):
        return self.__base_address + path + self.__get_encoded_parameters(query_parameters)

    def __replace_parameters(self, template, parameters):
        current_path = template
        for name, value in parameters.items():
            quoted_value = urllib.parse.quote(str(value)).replace("/", "%2F")
            current_path = current_path.replace("{" + name + "}", quoted_value)
        if re.search("[{}]", current_path):
            raise ValueError("Insufficient parameters to complete the path")
        else:
            return current_path

    def __create_url(self, path_template, parameters, query_parameters):
        assert (path_template.startswith("/"))
        assert (path_template.count("/") >= 2)
        path = self.__replace_parameters(path_template, parameters)
        return self.__get_urlencoded_address(path, query_parameters)

    def __get_http_data(self, data, json):
        if data and json:
            raise ValueError("Only one of 'data' and 'json' should be specified")

        return data or (json and json_module.dumps(json).encode('utf-8'))

    def __get_connection_closed_exception(self):
        return RuntimeError("pyFRONTIER connection interrupted. Check connection configuration and try to reconnect")

    def __get_headers(self, content_type):
        if content_type:
            return {'content-type': content_type}
        else:
            return {}

    def __read_server_response(self, request, convert_f):
        try:
            result = urllib.request.urlopen(request)
            code = result.getcode()
            if code == HTTPStatus.NO_CONTENT:
                return None
            else:
                return convert_f(result.read().decode())
        except urllib.error.HTTPError as e:
            raise self.__convert_http_error(e) from None
        except urllib.error.URLError as e:
            if self.__is_server_closed(e):
                log.debug("'Connection closed' detected")
                self.__connection_closed = True
                raise self.__get_connection_closed_exception() from None
            else:
                raise RuntimeError(e.reason) from None
        except Exception as e:
            raise RuntimeError("Internal error", e)

    def __convert_http_error(self, e):
        message = e.fp.read().decode()
        if message.startswith("ValueError|"):
            return ValueError(message[len("ValueError|"):])
        elif message.startswith("TypeError|"):
            return TypeError(message[len("TypeError|"):])
        else:
            return RuntimeError(message)

    def __list_to_tuples(self, data):
        if isinstance(data, list):
            for i in range(len(data)):
                data[i] = self.__list_to_tuples(data[i])
            return tuple(data)
        elif isinstance(data, dict):
            for key in data.keys():
                data[key] = self.__list_to_tuples(data[key])
            return data
        elif isinstance(data, tuple):
            return self.__list_to_tuples(list(data))
        else:
            return data

    def __convert_json(self, data):
        return self.__list_to_tuples(json_module.loads(data))

    def __connect(self, path_template, parameters, query_parameters,
                  method="GET", content_type=None,
                  data=None, json=None,
                  convert_f=lambda x: x):
        if self.__connection_closed:
            raise self.__get_connection_closed_exception()

        url = self.__create_url(path_template, parameters, query_parameters)
        http_data = self.__get_http_data(data, json)
        headers = self.__get_headers(content_type)
        request = urllib.request.Request(url,
                                         headers=headers,
                                         method=method,
                                         data=http_data)
        return self.__read_server_response(request, convert_f)

    def get(self, path, parameters={}, query_parameters={}):
        return self.__connect(path, parameters, query_parameters)

    def get_json(self, path, parameters={}, query_parameters={}):
        return self.__connect(path, parameters, query_parameters,
                              convert_f=self.__convert_json)

    def __post(self, path, parameters, query_parameters, json, convert_f):
        return self.__connect(path, parameters, query_parameters,
                              method="POST",
                              content_type="application/json",
                              json=json,
                              convert_f=convert_f)

    def post(self, path, parameters={}, query_parameters={}, json=None):
        return self.__post(path, parameters, query_parameters, json, lambda x: x)

    def post_json(self, path, parameters={}, query_parameters={}, json=None):
        return self.__post(path, parameters, query_parameters, json, self.__convert_json)

    def post_data(self, path, parameters={}, query_parameters={}, data=None):
        if not data:
            raise ValueError("Missing data")
        else:
            return self.__connect(path, parameters, query_parameters,
                                  method="POST",
                                  data=data,
                                  content_type="text/plain",
                                  convert_f=self.__convert_json)

    def patch(self, path, parameters={}, query_parameters={}, json=None):
        return self.__connect(path, parameters, query_parameters,
                              method="PATCH",
                              content_type="application/json",
                              json=json)

    def patch_json(self, path, parameters={}, query_parameters={}, json=None):
        return self.__connect(path, parameters, query_parameters,
                              method="PATCH",
                              json=json,
                              content_type="application/json",
                              convert_f=self.__convert_json)

    def delete(self, path, parameters={}, query_parameters={}):
        return self.__connect(path, parameters, query_parameters,
                              method="DELETE")


def __get_connection():
    global __current_connection
    if not __current_connection:
        log.debug("Establishing a new connection (port = '%s')……" % pyfrontier.get_port())
        __current_connection = Connection()
    return __current_connection


def get(path, parameters={}, query_parameters={}):
    return __get_connection().get(path, parameters, query_parameters)


def get_json(path, parameters={}, query_parameters={}):
    return __get_connection().get_json(path, parameters, query_parameters)


def post(path, parameters={}, query_parameters={}, json=None):
    return __get_connection().post(path, parameters, query_parameters, json)


def delete(path, parameters={}, query_parameters={}):
    return __get_connection().delete(path, parameters, query_parameters)


def post_json(path, parameters={}, query_parameters={}, json=None):
    return __get_connection().post_json(path, parameters, query_parameters, json)


def post_data(path, parameters={}, query_parameters={}, data=None):
    return __get_connection().post_data(path, parameters, query_parameters, data)


def patch(path, parameters={}, query_parameters={}, json=None):
    return __get_connection().patch(path, parameters, query_parameters, json)


def patch_json(path, parameters={}, query_parameters={}, json=None):
    return __get_connection().patch_json(path, parameters, query_parameters, json)


def clear_connection():
    log.debug("Clearing connection…")
    global __current_connection
    __current_connection = None
