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


logging.basicConfig(filename="Allure_Reports.Allure_Reports",
                             filemode = "w+",
                             format = "%(asctime)s : %(levelname)s : %(message)s",
                             datefmt = "%Y-%d-%m %H:%M:%S",
                             level=logging.INFO)

mylogger = logging.getLogger()
fh = logging.FileHandler('Allure_Reports.Allure_Reports')
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

def capture_memory():
    ssh_client = ssh_connect()
    (stdin, stdout, stderr) = ssh_client.exec_command( "cat /proc/meminfo | grep 'MemTotal'")
    for line in stdout.readlines():

        Mem = int(line.split(":")[1].lstrip(" ").split(" ")[0])
        file1 = open("MyFile.txt", "a+")
        fo = str(Mem)
        file1.write(fo)
        timestamp = capture_timestamp()
        file1.write(timestamp)
        file1.close()
        return Mem

def capture_disk():
    ssh_client = ssh_connect()
    (stdin, stdout, stderr) = ssh_client.exec_command( "df -h /")
    output = stdout.readlines()
    for line in output[1:]:
        result = line.split()
        used = (result[2].rstrip("G"))
        free = (result[3].rstrip("G"))
        totaldisk = float(used) + float(free)
        file1 = open("MyFile.txt", "a+")
        fo = str(totaldisk)
        file1.write(fo)
        timestamp = capture_timestamp()
        file1.write(timestamp)
        file1.close()
        return totaldisk

def capture_timestamp():
    ssh_client = ssh_connect()
    (stdin, stdout, stderr) = ssh_client.exec_command("date")
    for line in stdout.readlines():
        return line

### Test Cases :

@pytest.mark.cli
def test_cpu_utilisation():
    mylogger.info("Test case started...")
    cpu_value = int(round(float(capture_cpu())))
    assert cpu_value < 80, "Test Pass"
    mylogger.debug('1 Critical Test Passed')

@pytest.mark.cli
def test_memory_utilisation():
    mylogger.info("Memory Utilisation test case started...")
    Memory = capture_memory()
    assert Memory < 2000000, "Test Pass"

@pytest.mark.cli
def test_disk_utilisation():
    mylogger.info("Disk Utilisation test case started...")
    disk_usage = capture_disk()
    assert disk_usage < 90, "Test Pass"


