import base64
import pyfrontier
import socket
import urllib.request
from estecopy._internal.utils import log

STANDARD_LOCALHOST_ADDRESS = "127.0.0.1"
CHECK_TIMEOUT_S = 10


def get_localhost_address():
    try:
        log.debug("Checking if localhost is valid…")
        return socket.gethostbyname("localhost")
    except:
        log.debug("Defaulting to '%s'…" % STANDARD_LOCALHOST_ADDRESS)
        return STANDARD_LOCALHOST_ADDRESS


def is_server_valid(url_template, port, context, errors):
    try:
        request = urllib.request.Request(url_template % port)
        __add_header_if_auth_enabled(request)
        urllib.request.urlopen(request, timeout=CHECK_TIMEOUT_S, context=context)
        return True
    except urllib.error.HTTPError as e:
        errors.append(RuntimeError(e.fp.read().decode()))
    except urllib.error.URLError as e:
        errors.append(RuntimeError(e.reason))
    except Exception as e:
        errors.append(RuntimeError("Internal error", e))
    log.debug(f"Could not connect to pyFRONTIER on local machine on port {port}.\n")
    return False


def __add_header_if_auth_enabled(request):
    password = pyfrontier.get_connection_password()
    if password:
        credentials = '%s:%s' % ("pyFRONTIER_guest", password)
        encoded_credentials = base64.b64encode(credentials.encode('ascii'))
        request.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))


def get_server_address(ports, protocol, context):
    assert (len(ports) >= 1)
    address = get_localhost_address()
    errors = []
    url_template = "%s://%s" % (protocol, address) + ":%d/server/ping"
    valid_server_f = lambda port: (is_server_valid(url_template, port, context, errors))
    valid_ports = list(filter(valid_server_f, ports))
    if not valid_ports:
        raise errors[-1]
    else:
        return address, valid_ports[0]
