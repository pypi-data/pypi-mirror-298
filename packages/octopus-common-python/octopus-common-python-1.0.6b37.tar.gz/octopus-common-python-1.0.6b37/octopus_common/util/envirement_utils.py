import os

from requests.auth import HTTPBasicAuth

from octopus_common.config.octopus_config import LOCAL_AUTH_CONFIG


def get_client_code():
    client_code = os.environ.get('Auth.userid')
    if client_code is None:
        client_code = LOCAL_AUTH_CONFIG.get("userid", "")
    return client_code


def get_password():
    password = os.environ.get('Auth.password')
    if password is None:
        password = LOCAL_AUTH_CONFIG.get("password", "")
    return password


def get_auth():
    return HTTPBasicAuth(get_client_code(), get_password())
