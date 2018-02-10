import sys
import hashlib
import uuid
import getpass
import argparse
import textwrap
import paramiko
import base64

from Settings import PASSWD


class Account:

    def hashPasswd(self, user_password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha512(salt.encode() + user_password.encode()).hexdigest(), salt


    def checkPasswd(self, hashed_password, salt, user_password):
        if hashed_password == hashlib.sha512(salt.encode() + user_password.encode()).hexdigest():
            return True
        return False


    def checkUserExsistence(self, username):
        with open(PASSWD, 'r') as fr:
            for line in fr:
                _username = line.split(':')[0]
                if _username == username:
                    return True
            return False


    def createAccount(self):
        username = input("Please Enter a Username: ")
        if username == "":
            print("Username can not be Null!")
            sys.exit(1)
        if self.checkUserExsistence(username):
            print("Username already exist!")
            sys.exit(1)
        user_password = getpass.getpass("Please Enter a Password: ")
        hashed_password, salt = self.hashPasswd(user_password)

        with open(PASSWD, 'a') as fw:
            fw.write(username + ":" + hashed_password + ":" + salt + "\n")
        print("Account: " + username + " created successfully.")


    def deleteAccount(self):
        username_to_del = input("Please Enter a Username to Delete:")
        if self.checkUserExsistence(username_to_del) is False:
            print("Username does not exist!")
            exit(1)

        output = []
        with open(PASSWD, 'r') as fr:
            for line in fr:
                _username = line.strip('\n').split(':')[0]
                if _username != username_to_del:
                    output.append(line)
        with open(PASSWD, 'w') as fw:
            fw.writelines(output)
        print("Account: " + username_to_del + "deleted successfully.")


    def verifyAccountPwd(self, username, user_password):
        with open(PASSWD, 'r') as fr:
            for line in fr:
                _username, _hashed_password, _salt = line.strip('\n').split(':')
                if _username == username and self.checkPasswd(_hashed_password, _salt, user_password):
                    return True
            return False


    def verifyAccountPubKey(self, username, pubkey):
        pubkey_file = 'secret/clientKeys/' + username + '_rsa.pub'
        try:
            with open(pubkey_file, 'r') as fp:
                for rawline in fp:
                    line = rawline.strip()
                    if not line or line.startswith('#'):
                        continue
                    if line.startswith("ssh-rsa "):
                        # Get the key field
                        d = " ".join(line.split(" ")[1:]).lstrip().split(" ")[0]
                        k = paramiko.RSAKey(data=base64.b64decode(d))
                    # compare pub key
                    if pubkey == k:
                        return True
        except Exception as e:
            return False


    def verifyAccount(self):
        username = input("Please Enter a Username: ")
        if username == "":
            print("Username can not be Null!")
            sys.exit(1)
        if self.checkUserExsistence(username) is False:
            print("Username does not exist!")
            sys.exit(1)
        user_password = getpass.getpass("Please Enter a Password: ")
        if self.verifyAccountPwd(username, user_password):
            print("Verify Account password successfully.")
        else:
            print("Verify Account password failed.")


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
