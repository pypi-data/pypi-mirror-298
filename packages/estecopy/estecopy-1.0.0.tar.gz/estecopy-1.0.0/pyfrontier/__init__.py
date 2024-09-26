import sys
from pyfrontier._config import __PyFrontierConfig


def set_host(host):
    """Set the IP address or hostname where pyFRONTIER is running."""
    __throw_if_already_connected()
    __CONFIG.set_host(host)


def get_host():
    """Returns the IP address or host set with the 'set_host' method."""
    return __CONFIG.get_host()


def set_port(port):
    """Set the port on which pyFRONTIER is accepting connections."""
    __throw_if_already_connected()
    __CONFIG.set_port(port)


def get_port():
    """Returns the port set with the 'set_port' method."""
    return __CONFIG.get_port()


def set_connection_password(connection_password):
    """Set the password required for the authentication on the remote pyFRONTIER."""
    __throw_if_already_connected()
    __CONFIG.set_connection_password(connection_password)


def get_connection_password():
    """Returns the password set with the 'set_connection_password' method."""
    return __CONFIG.get_connection_password()


def set_protocol(protocol):
    """
    Specify the protocol for the connection with the remote pyFRONTIER. The available options are:
     "http", "https", "https-no-checks", "auto". The default is "auto".
    """
    __throw_if_already_connected()
    __CONFIG.set_protocol(protocol)


def get_protocol():
    """Returns the protocol for the connection with the remote pyFRONTIER."""
    return __CONFIG.get_protocol()


def set_check_hostname(check_hostname):
    """Set whether to check the hostname of the remote pyFRONTIER."""
    __throw_if_already_connected()
    __CONFIG.set_check_hostname(check_hostname)


def is_check_hostname():
    """Returns whether to check the hostname of the remote pyFRONTIER."""
    return __CONFIG.is_check_hostname()


def set_ca_bundle_file(ca_bundle_file):
    """Set the path of the CA bundle file that will be used to verify the server certificate."""
    __throw_if_already_connected()
    __CONFIG.set_ca_bundle_file(ca_bundle_file)


def get_ca_bundle_file():
    """Returns the path of the CA bundle file that will be used to verify the server certificate."""
    return __CONFIG.get_ca_bundle_file()


def get_estecopy_version():
    """Returns the estecopy version installed on your machine."""
    return "1.0.0"


def __throw_if_already_connected():
    if 'estecopy' in sys.modules:
        raise RuntimeError("Can't change configuration after connecting to pyFRONTIER.")


def _get_config():
    return __CONFIG


__CONFIG = __PyFrontierConfig()
