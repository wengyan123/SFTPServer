import logging
import threading

from paramiko import ServerInterface, AUTH_SUCCESSFUL, OPEN_SUCCEEDED, AUTH_FAILED, OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

from sftpServer.Account import Account


class StubServer(ServerInterface):

    def __init__(self):
        # an event to trigger when negotiation is complete
        self.event = threading.Event()
        self.logger = logging.getLogger(__name__)

    def check_auth_password(self, username, password):
        account = Account()
        if account.verifyAccountPwd(username, password):
            self.logger.info("User: [" + username + "] auth successful thru password.")
            return AUTH_SUCCESSFUL
        self.logger.info("User: [" + username + "] auth failed thru password!")
        return AUTH_FAILED


    # https://github.com/dlitz/pysftpd
    def check_auth_publickey(self, username, key):
        account = Account()
        if account.verifyAccountPubKey(username, key):
            self.logger.info("User: [" + username + "] auth successful thru public key.")
            return AUTH_SUCCESSFUL
        self.logger.info("User: [" + username + "] auth failed thru public key.")
        return AUTH_FAILED


    def check_channel_request(self, kind, chanid):
        #return OPEN_SUCCEEDED
        if kind == 'session':
            return OPEN_SUCCEEDED
        return OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


    def get_allowed_auths(self, username):
        """List availble auth mechanisms."""
        return "password,publickey"


