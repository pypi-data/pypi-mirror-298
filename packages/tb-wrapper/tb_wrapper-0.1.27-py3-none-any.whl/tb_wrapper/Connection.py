from tb_wrapper.handle_exception import handle_tb_wrapper_exception
from tb_rest_client.rest_client_ce import *
from typing import Dict


class Connection:
    tb_client = None

    def __init__(self, tb_url=None, userfile=None, passwordfile=None, connection=None, token=None, refresh_token=None):
        if token is not None:
            self.tb_client = RestClientCE(base_url=tb_url)
            if refresh_token is not None:
                self.tb_client.token_login(
                    token=token, refresh_token=refresh_token)
            else:
                self.tb_client.token_login(
                    token=token)
                self.__is_token_valid()

        elif connection is not None:
            self.tb_client = connection
            self.__is_connection_valid()
        else:
            self.__check_valid_parameters(tb_url, userfile, passwordfile)
            self.tb_client = RestClientCE(base_url=tb_url)
            with open(userfile) as f:
                USERNAME = f.readline().strip()
            with open(passwordfile) as f:
                PASSWORD = f.readline().strip()
            self.tb_client.login(
                username=USERNAME, password=PASSWORD)

    def destroyConnection(self):
        return self.tb_client.logout()

    @handle_tb_wrapper_exception
    def __check_valid_parameters(self, tb_url, userfile, passwordfile):
        if tb_url is None or tb_url == "":
            raise ValueError(
                "Invalid Url while trying to get connection to Thingsboard ")
        if userfile is None or userfile == "":
            raise ValueError(
                "Invalid username while trying to get connection to Thingsboard ")
        if passwordfile is None or passwordfile == "":
            raise ValueError(
                "Invalid password while trying to get connection to Thingsboard ")

    def __is_token_valid(self):
        try:
            self.tb_client.get_user()
        except Exception:
            raise ValueError(
                "Invalid Token received while trying to get connection to Thingsboard")

    def __is_connection_valid(self):
        try:
            self.tb_client.get_user()
        except Exception:
            raise ValueError(
                "Invalid Connection received while trying to get connection to Thingsboard")
