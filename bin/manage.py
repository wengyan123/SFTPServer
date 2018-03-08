import argparse
import textwrap

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sftpServer import sftpServer, helpers
from sftpServer.Account import Account


def main():

    usage = """\
    Usage: python manage.py [action]
        1. start server: manage.py startserver
            -Con/--config: indicate server config file
            -debug: enable debug logs
        2. manage account: manage.py account
            -C/--create: to create an account
            -D/--delete: to delete an account
            -V/--verify: to verify an account's password
    """
    parser = argparse.ArgumentParser(usage=textwrap.dedent(usage))
    parser.add_argument('action', help='Processing some actions(startserver, account)')

    parser.add_argument('-Con', '--config', dest='config', default='settings.json', help='Config file used by SFTP server')
    parser.add_argument('-C', '--create', dest='create', action='store_true', default=False)
    parser.add_argument('-D', '--delete', dest='delete', action='store_true', default=False)
    parser.add_argument('-V', '--verify', dest='verify', action='store_true', default=False)
    parser.add_argument('-debug', dest='debug', action='store_true', default=False)

    args = parser.parse_args()

    # start server
    if args.action == 'startserver' and args.config:
        sftp_settings = helpers.loadConfig(args.config)
        host = sftp_settings['server']['host']
        port = sftp_settings['server']['port']
        root_dir = sftp_settings['server']['root_dir']
        helpers.setServerRootDir(root_dir)
        log_level = args.debug
        sftpServer.startServer(host, port, log_level)
    # manage account
    if args.action == 'account':
        if args.create:
            account = Account()
            account.createAccount()
            exit(0)
        if args.delete:
            account = Account()
            account.deleteAccount()
            exit(0)
        if args.verify:
            account = Account()
            account.verifyAccount()
            exit(0)


if __name__ == '__main__':
    main()
