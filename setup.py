from setuptools import setup


with open("README", 'r') as f:
    long_description = f.read()


setup(
    name='SFTPServer',
    version='0.1.0',
    description='A Demo SFTP server',
    long_description=long_description,
    author='WENG Yan',
    author_email='yan.weng@outlook.com',
    url="https://github.com/wengyan123/SFTPServer",
    packages=['sftpServer'],
    license='MIT',
    install_requires=[
        'bcrypt>=3.1.3',
        'cryptography>=1.5',
        'pynacl>=1.0.1',
        'pyasn1>=0.1.7',
        'paramiko>=2.4.0',
    ],
)