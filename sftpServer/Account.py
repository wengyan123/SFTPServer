import base64
import getpass
import hashlib
import sys
import os
import uuid
import paramiko
import logging

from sftpServer.settings import PASSWD


class Account:
    passwd = os.path.dirname(os.path.abspath(__file__)) + '/' + PASSWD
    client_pubkey_dir = os.path.dirname(os.path.abspath(__file__)) + '/secret/clientKeys'


    def __init__(self):
        self.logger = logging.getLogger(__name__)


    def hashPasswd(self, user_password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha512(salt.encode() + user_password.encode()).hexdigest(), salt


    def checkPasswd(self, hashed_password, salt, user_password):
        if hashed_password == hashlib.sha512(salt.encode() + user_password.encode()).hexdigest():
            return True
        return False


    def checkUserExsistence(self, username):
        with open(self.passwd, 'r') as fr:
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

        with open(self.passwd, 'a') as fw:
            fw.write(username + ":" + hashed_password + ":" + salt + "\n")
        print("Account: " + username + " created successfully.")


    def deleteAccount(self):
        username_to_del = input("Please Enter a Username to Delete:")
        if self.checkUserExsistence(username_to_del) is False:
            print("Username does not exist!")
            exit(1)
        output = []
        with open(self.passwd, 'r') as fr:
            for line in fr:
                _username = line.strip('\n').split(':')[0]
                if _username != username_to_del:
                    output.append(line)
        with open(self.passwd, 'w') as fw:
            fw.writelines(output)
        print("Account: " + username_to_del + " deleted successfully.")


    def verifyAccountPwd(self, username, user_password):
        with open(self.passwd, 'r') as fr:
            for line in fr:
                _username, _hashed_password, _salt = line.strip('\n').split(':')
                if _username == username and self.checkPasswd(_hashed_password, _salt, user_password):
                    return True
            return False


    def verifyAccountPubKey(self, username, pubkey):
        pubkey_file = self.client_pubkey_dir.rstrip('/') + '/' + username + '_rsa.pub'
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
            self.logger.error(e)
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
            print("Verify Account " + username + " password successfully.")
        else:
            print("Verify Account " + username + " password failed.")
