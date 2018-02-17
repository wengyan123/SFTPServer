import argparse
import socket
import sys
import textwrap
import time

import paramiko

from sftpServer.settings import SERVER_HOST, SERVER_PORT, SERVER_BACKLOG, SERVER_KEYFILE
from sftpServer.StubServer import StubServer
from sftpServer.SubSFTPServer import SubSFTPServer
from sftpServer.helpers import createLogger

# global variables
logger = None


def startServer(host, port, keyfile, level):
    # set paramiko logging level
    #paramiko_level = getattr(paramiko.common, level)
    #paramiko.common.logging.basicConfig(level=paramiko_level)
    global logger
    logger = createLogger(debug=True)

    logger.info(" Starting SFTP Server on " + str(host) + ":" + str(port))
    # start a socket listener
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # the SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state,
        # without waiting for its natural timeout to expire.
        # https://docs.python.org/2/library/socket.html
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        server_socket.bind((host, port))
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
        host_key = paramiko.RSAKey.from_private_key_file(keyfile)
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


def main():

    usage = """\
    usage: sftpserver [options]
    -k/--keyfile should be specified
    """
    parser = argparse.ArgumentParser(usage=textwrap.dedent(usage))
    parser.add_argument(
        '--host', dest='host', default=SERVER_HOST,
        help='listen on HOST [default: %(default)s]'
    )
    parser.add_argument(
        '-p', '--port', dest='port', type=int, default=SERVER_PORT,
        help='listen on PORT [default: %(default)d]'
    )
    parser.add_argument(
        '-l', '--level', dest='level', default='DEBUG',
        help='Debug level: WARNING, INFO, DEBUG [default: %(default)s]'
    )
    parser.add_argument(
        '-k', '--keyfile', dest='keyfile', metavar='FILE', default=SERVER_KEYFILE,
        help='Path to private key, for example /tmp/test_rsa.key'
    )

    args = parser.parse_args()

    if args.keyfile is None:
        parser.print_help()
        sys.exit(-1)

    startServer(args.host, args.port, args.keyfile, args.level)


if __name__ == '__main__':
    main()
