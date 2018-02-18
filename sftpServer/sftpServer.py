import socket
import sys
import time
import os

import paramiko

from sftpServer.settings import SERVER_BACKLOG, SERVER_KEYFILE
from sftpServer.StubServer import StubServer
from sftpServer.SubSFTPServer import SubSFTPServer
from sftpServer.helpers import createLogger

# global variables
logger = None


def startServer(host, port, log_level):
    # set paramiko logging level
    #paramiko_level = getattr(paramiko.common, level)
    #paramiko.common.logging.basicConfig(level=paramiko_level)
    global logger
    logger = createLogger(debug=log_level)

    logger.info(" Starting SFTP Server on " + str(host) + ":" + str(port))
    # start a socket listener
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # the SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state,
        # without waiting for its natural timeout to expire.
        # https://docs.python.org/2/library/socket.html
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        server_socket.bind((host, int(port)))
        server_socket.listen(SERVER_BACKLOG)
        logger.info(" Listen for connection...")
    except Exception as e:
        logger.error(" Listen failed. " + str(e))
        sys.exit(1)

    while True:
        conn, addr = server_socket.accept()
        logger.info(" Got a connection from " + str(addr[0]) + ':' + str(addr[1]))

        # When behaving as a server, the host key is used to sign certain packets during the SSH2 negotiation,
        # so that the client can trust that we are who we say we are.
        server_key = os.path.dirname(os.path.abspath(__file__)) + '/' + SERVER_KEYFILE
        host_key = paramiko.RSAKey.from_private_key_file(server_key)
        transport = paramiko.Transport(conn)
        transport.add_server_key(host_key)
        # Set the handler class for a subsystem in server mode.
        # If a request for this subsystem is made on an open ssh channel later,
        # this handler will be constructed and called
        transport.set_subsystem_handler('sftp', paramiko.SFTPServer, SubSFTPServer)

        server = StubServer()
        try:
            # Negotiate a new SSH2 session as a server.
            # This is the first step after creating a new Transport and setting up your server host key(s).
            # A separate thread is created for protocol negotiation.
            transport.start_server(server=server)
        except paramiko.SSHException as e:
            logger.error("SSH negotiation failed. " + str(e))

        channel = transport.accept()
        while transport.is_active():
            time.sleep(1)
