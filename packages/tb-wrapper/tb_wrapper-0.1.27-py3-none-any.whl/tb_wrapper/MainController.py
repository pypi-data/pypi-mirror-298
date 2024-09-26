from tb_rest_client.rest_client_ce import *
from tb_wrapper.Connection import Connection


class MainController:

    tb_client = None

    def __init__(self, tb_url=None, userfile=None, passwordfile=None, connection=None, token=None, refresh_token=None):
        self.tb_client = Connection(tb_url=tb_url, userfile=userfile, passwordfile=passwordfile,
                                    connection=connection, token=token, refresh_token=refresh_token).tb_client
