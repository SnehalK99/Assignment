import pytest
import pytest_html
import unittest
import socket
import paramiko
from paramiko import Channel
from socket import error as socket_error
import os
from test_data.input import *
from pytest import mark
import logging
import datetime

logging.basicConfig(filename="log.log",
                             filemode = "w+",
                             format = "%(asctime)s : %(levelname)s : %(message)s",
                             datefmt = "%Y-%d-%m %H:%M:%S",
                             level=logging.INFO)

mylogger = logging.getLogger()
fh = logging.FileHandler('log.log')
fh.setLevel(logging.DEBUG)
mylogger.addHandler(fh)


def ssh_connect():

        try:
            logging.info('Connecting to remote server:')
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, username=user, password=passwd, look_for_keys=False)
            mylogger.info("Connection to host successful")
            return client
        except paramiko.SSHException as e:
            print('SSH connection error: %s' % str(e))
            print("Please check the username and password")
        except socket.error:
            print("Please check server ip address", socket_error)

def capture_cpu():
    ssh_client = ssh_connect()
    # (stdin, stdout, stderr) = ssh_client.exec_command("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }'")
    (stdin, stdout, stderr) = ssh_client.exec_command(
        "grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }'")

    for line in stdout.readlines():
        file1 = open("MyFile.txt", "a+")
        file1.write(line+"")
        timestamp = capture_timestamp()
        file1.write(timestamp)
        file1.close()
        return line

def capture_timestamp():
    ssh_client = ssh_connect()
    (stdin, stdout, stderr) = ssh_client.exec_command("date")
    for line in stdout.readlines():


        return line

@pytest.mark.cli
def test_cpu_utilisation():
    mylogger.info("Test case started...")
    cpu_value = int(round(float(capture_cpu())))
    assert cpu_value < 80, "Test Pass"
    mylogger.debug('1 Critical Test Passed')

if __name__ == '__main__':

    pytest.main(args=['-sv', os.path.abspath(__file__)])