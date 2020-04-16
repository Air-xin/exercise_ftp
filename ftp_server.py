"""
ftp 文件服务器
【1】	分为服务端和客户端，要求可以有多个客户端同时操作。
【2】	客户端可以查看服务器文件库中有什么文件。
【3】	客户端可以从文件库中下载文件到本地。
【4】	客户端可以上传一个本地文件到文件库。
【5】    使用print在客户端打印命令输入提示，引导操作
"""
# 服务端
from socket import *
from threading import Thread
import sys, os
import time

ADDR = ("0.0.0.0", 8800)
DIR = "./file_dir/"


class MyThread(Thread):
    def __init__(self, tcp_connect):
        super().__init__()
        self.tcp_connect = tcp_connect
        self.file_list = os.listdir(DIR)

    def do_list(self):
        if not self.file_list:
            self.tcp_connect.send(b"N")
        else:
            self.tcp_connect.send(b"Y")
            time.sleep(0.1)
            data = "\n".join(self.file_list)
            self.tcp_connect.send(data.encode())

    def put_file(self):
        data = self.tcp_connect.recv(20).decode()
        if data not in self.file_list:
            self.tcp_connect.send(b"N")
        else:
            f = open(DIR + data, 'rb')
            self.tcp_connect.send(b"Y")
            time.sleep(0.1)
            while True:
                data = f.read(1024)
                if len(data) < 1024:
                    self.tcp_connect.send(data)
                    f.close()
                    break
                else:
                    self.tcp_connect.send(data)

    def get_file(self):
        data = self.tcp_connect.recv(20).decode()
        if data in self.file_list:
            self.tcp_connect.send(b"Y")
            msg = self.tcp_connect.recv(20).decode()
            if msg == 'N':
                return
        else:
            self.tcp_connect.send(b"N")
        f = open(DIR + data, 'wb')
        while True:
            file = self.tcp_connect.recv(1024)
            if len(data) < 1024:
                f.write(file)
                f.close()
                break
            f.write(file)

    def run(self):
        while True:
            data = self.tcp_connect.recv(20).decode()
            if not data:
                break
            if data == "L":
                self.do_list()
            elif data == 'G':
                self.put_file()
            elif data == 'P':
                self.get_file()
            elif data == 'Q':
                break


def main():
    tcp_sock = socket()
    tcp_sock.bind(ADDR)
    tcp_sock.listen(2)
    while True:
        try:
            tcp_connect, addr = tcp_sock.accept()
            print("客户端地址:", addr)
        except:
            sys.exit("服务退出")
        t = MyThread(tcp_connect)
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    main()
