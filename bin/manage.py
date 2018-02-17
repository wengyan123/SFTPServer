import argparse
import textwrap

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def main():

    usage = """\
    Usage: python manage.py [options]
        1. start server: manage.py startserver -C/--config [config file]
        2. manage account: manage.py account
            -C/--create: to create an account
            -D/--delete: to delete an account
            -V/--verify: to verify an account's password
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


def main():

    usage = """usage: python Account.py [options]
    -C/--create: to create an account
    -D/--delete: to delete an account
    -V/--verify: to verify an account's password\
    """
    if len(sys.argv) < 2:
        print(usage)

    parser = argparse.ArgumentParser(usage=textwrap.dedent(usage))
    parser.add_argument('-C', '--create', dest='create', action='store_true', default=False)
    parser.add_argument('-D', '--delete', dest='delete', action='store_true', default=False)
    parser.add_argument('-V', '--verify', dest='verify', action='store_true', default=False)
    args = parser.parse_args()

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