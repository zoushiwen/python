# -*- coding:utf-8 -*-
# Author: zoujiangtao

import socket
import sys
import re
from paramiko import Transport,SSHException,ssh_exception ,SSHClient,AutoAddPolicy
import paramiko
import threading
import queue
import time

def Print(content,hostname=None,colour=None,type=False):

    if hostname is None:
        hostname = socket.gethostname()

    if colour is not None:
        if colour == "red":
            if type:
                print("[{}] \033[1;33mplease view  error log \033[0m".format(hostname))
            print("[{}] \033[1;31mError: {} \nExit installation.\033[0m".format(hostname,content))
            sys.exit(1)
        elif colour == "green":
            print("[{}] \033[1;32m{} \033[0m ".format(hostname,content))
        elif colour == "yellow":
            print("[{}] \033[1;33m{} \033[0m".format(hostname,content))
        else:
            print(content)
    else:
        print(content)

def getIndex(host):
    regx = re.compile(r'(.+)?\[(.*)\](.*)?')
    re_host = regx.match(host)
    start_domain, host_range, end_domain = re_host.group(1), re_host.group(2), re_host.group(3)
    separator = re.search('\W+', host_range).group()
    realHost = list()
    try:
        first, end = int(host_range.split(separator)[0]),int(host_range.split(separator)[1])
    except ValueError as e:
        print(e)
        sys.exit(1)

    if end < first:
        print("The index value must {} greater than {}.".format(end,first))
        sys.exit(1)

    for i in range(first, end):
        resHost = ''.join([start_domain,'{:02d}'.format(i),end_domain])
        realHost.append(resHost)
    return realHost

def write_file(content):
    file = 'host'
    with open(file,'a+') as f:
            f.writelines(content)

class LinuxSSHAuth:
    """
        Verify that Linux machines are SSH connected
    """
    def __init__(self,port=None,username=None,password=None,private_key=None,timeout=None):

        self.username = 'root' if username is None else username
        self.port = 22 if port is None else port
        self.timeout = 3 if timeout is None else timeout

        if password is not None:
            self.password = password
            self.private = None
        else:
            if private_key is not None:
                self.private = private_key
            else:
                self.private = '/root/.ssh/id_rsa'

    def auth(self,hostname):

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((hostname,self.port))
            self.ssh_check(hostname,sock=sock)
        except socket.error as error:
            Print ("{} {} {}".format(hostname,self.username,error),colour="yellow")

    def ssh_check(self,hostname,sock):

        transport= Transport(sock=sock)
        try:
            transport.start_client()
        except SSHException as error:
            Print("{} {}".format(self.username,error),colour="red")
        try:
            if self.password is None:
                private_key = paramiko.RSAKey.from_private_key_file(self.private)
                transport.auth_publickey(self.username,private_key)
            else:
                transport.auth_password(self.username, self.password)
            if transport.is_authenticated():
                Print("{} {} connection Successfully.".format(hostname,self.username),colour="green")
        except ssh_exception.SSHException as e:
            Print("{} {} Error in username or password.".format(hostname, self.username), colour="yellow")
            write_file(''.join([hostname,'\n']))
            raise Exception("{} {}".format(hostname,e))

def product(q):
    for ip in ip_list:
        q.put(ip)

def consumer(j,q):
    sshAuth = LinuxSSHAuth(username=username, password=password)
    try:
        sshAuth.auth(q.get())
    except Exception as error:
        print(error)

def multiThreading(num,args,q):

    for i in range(num):
        t = threading.Thread(target=product,args=args)
        t.start()

    for j in range(num):
        v = threading.Thread(target=consumer,args=(j,q))
        v.start()



if __name__ == '__main__':
    username = 'you_usernmae'
    password = 'you_password'
    q = queue.Queue()
    try:
        host = sys.argv[1]
        host_list = list()
        ip_list = getIndex(host)
        list_length = len(ip_list)
        multiThreading(list_length,args=(host,q),q=q)
    except IndexError as error:
        print(error)
