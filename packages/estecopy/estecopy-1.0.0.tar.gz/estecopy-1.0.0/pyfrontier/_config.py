import json
import os
import socket


class __PyFrontierConfig:
    __CONFIG_FILE_ENV_VARIABLE = "PYFRONTIER_CONFIG_FILE"
    __PORT_KEY = "port"
    __HOST_KEY = "host"
    __SELF_PROTOCOL_KEY = "protocol"
    __CONNECTION_PASSWORD_KEY = "connection_password"
    __CHECK_HOSTNAME_KEY = "check_hostname"
    __CA_BUNDLE_FILE_KEY = "ca_bundle_file"
    __CONFIG_FILE_VALID_KEYS = [__PORT_KEY, __HOST_KEY, __SELF_PROTOCOL_KEY, __CONNECTION_PASSWORD_KEY, __CHECK_HOSTNAME_KEY, __CA_BUNDLE_FILE_KEY]
    __MIN_PORT_VALUE = 1
    __MAX_PORT_VALUE = 65535
    __PROTOCOL_OPTIONS = ["http", "https", "https-no-checks", "auto"]

    def __init__(self):
        self.__host = None
        self.__port = None
        self.__protocol = "auto"
        self.__secure_connection = False
        self.__connection_password = None
        self.__check_certificate = False
        self.__check_hostname = True
        self.__ca_bundle_file = None
        self.__read_config_from_file()

    def __read_config_from_file(self):
        file_path = os.getenv(self.__CONFIG_FILE_ENV_VARIABLE)
        if file_path is not None:
            try:
                with open(file_path) as file_content:
                    self.__parse_config_file(file_content)
            except FileNotFoundError:
                raise FileNotFoundError(f"{self.__CONFIG_FILE_ENV_VARIABLE} not found, check environment variable definition") from None

    def __parse_config_file(self, file_content):
        try:
            config_dictionary = json.load(file_content)
        except json.decoder.JSONDecodeError as e:
            raise ValueError(f"{self.__CONFIG_FILE_ENV_VARIABLE} contains errors ({e})") from None
        try:
            self.__read_parsed_config(config_dictionary)
        except (TypeError, ValueError) as e:
            raise ValueError(f"{self.__CONFIG_FILE_ENV_VARIABLE} {e}") from None

    def __read_parsed_config(self, config_dictionary):
        for key, value in config_dictionary.items():
            if key == self.__PORT_KEY:
                self.set_port(value)
            elif key == self.__HOST_KEY:
                self.set_host(value)
            elif key == self.__SELF_PROTOCOL_KEY:
                self.set_protocol(value)
            elif key == self.__CONNECTION_PASSWORD_KEY:
                self.set_connection_password(value)
            elif key == self.__CHECK_HOSTNAME_KEY:
                self.set_check_hostname(value)
            elif key == self.__CA_BUNDLE_FILE_KEY:
                self.set_ca_bundle_file(value)
            else:
                raise ValueError(f"invalid key, valid keys are {self.__CONFIG_FILE_VALID_KEYS}")

    def set_host(self, host):
        if not isinstance(host, str):
            raise TypeError('host address must be a string')
        self.__check_host(host)
        self.__host = host

    def __check_host(self, host):
        try:
            socket.gethostbyname(host)
        except socket.gaierror:
            raise TypeError('host address must be a valid IPv4 string or a valid hostname') from None

    def get_host(self):
        return self.__host

    def set_port(self, port):
        if port:
            if not isinstance(port, int):
                raise TypeError('port must be an integer')
            if not self.__MIN_PORT_VALUE <= port <= self.__MAX_PORT_VALUE:
                raise ValueError(f'port must be an integer between {self.__MIN_PORT_VALUE} and {self.__MAX_PORT_VALUE}')
        self.__port = port

    def get_port(self):
        return self.__port

    def set_protocol(self, protocol):
        if not isinstance(protocol, str):
            raise TypeError('protocol must be a string')
        if protocol not in self.__PROTOCOL_OPTIONS:
            raise ValueError(f'protocol must be one of the following: {self.__PROTOCOL_OPTIONS}')
        self.__protocol = protocol
        if protocol == "http":
            self.__secure_connection = False
        elif protocol == "https":
            self.__secure_connection = True
            self.__check_certificate = True
        elif protocol == "https-no-checks":
            self.__secure_connection = True
            self.__check_certificate = False

    def get_protocol(self):
        return self.__protocol

    def is_secure_connection(self):
        return self.__secure_connection

    def set_connection_password(self, connection_password):
        if not isinstance(connection_password, str):
            raise TypeError('connection_password must be a string')
        self.__connection_password = connection_password

    def get_connection_password(self):
        return self.__connection_password

    def is_check_certificate(self):
        return self.__check_certificate

    def set_check_hostname(self, check_hostname):
        if not isinstance(check_hostname, bool):
            raise TypeError('check_hostname must be a boolean')
        self.__check_hostname = check_hostname

    def is_check_hostname(self):
        return self.__check_hostname

    def set_ca_bundle_file(self, ca_bundle_file):
        if not isinstance(ca_bundle_file, str):
            raise TypeError('ca_bundle_file must be a string')
        if not os.path.isfile(ca_bundle_file):
            raise ValueError('ca_bundle_file must be a valid file path')
        self.__ca_bundle_file = ca_bundle_file

    def get_ca_bundle_file(self):
        return self.__ca_bundle_file
