import paramiko
import os


# open a transport
transport = paramiko.Transport(('localhost', 3373))

# password auth
#transport.connect(username='wengyan', password='123456')

# public key auth
key = paramiko.RSAKey.from_private_key_file('client_dir/clientKeys/wengyan_rsa')
transport.connect(username='wengyan', pkey=key)

# fork stfp client
sftp = paramiko.SFTPClient.from_transport(transport)

# list remote server dir
out=sftp.listdir('.')
print(out)

# download
server_path = "server_test1.txt"
client_path = "client_dir/from_server_test1.txt"
sftp.get(server_path, client_path)

# upload
#server_path = "/from_client_test1.txt"
#client_path = "/Users/wengyan/Dev/gto/github/gto/python/sftp/client_dir/client_test1.txt"
#sftp.put(client_path, server_path)


# Close
sftp.close()
transport.close()