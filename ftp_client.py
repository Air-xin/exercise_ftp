# 客户端

from socket import *
from time import sleep

ADDR = ('127.0.0.1', 8800)


class Dispose:
    def __init__(self, tcp_sock):
        self.tcp_sock = tcp_sock

    def do_file(self):
        self.tcp_sock.send(b'L')
        data = self.tcp_sock.recv(20).decode()
        if data == "Y":
            data = self.tcp_sock.recv(5000)
            print(data.decode())
        else:
            print("获取文件列表失败")

    def get_file(self):
        self.tcp_sock.send(b'G')
        msg = input('请输入文件名:')
        self.tcp_sock.send(msg.encode())
        data = self.tcp_sock.recv(20).decode()
        if data == "Y":
            f = open('./' + msg, 'wb')
            while True:
                data = self.tcp_sock.recv(1024)
                if len(data) < 1024:
                    f.write(data)
                    f.close()
                    print('下载完成')
                    break
                else:
                    f.write(data)
        else:
            print("文件未找到")

    def put_file(self):
        self.tcp_sock.send(b'P')
        file = input('请输入文件路径:')
        try:
            f = open(file, 'rb')
        except:
            print('文件不存在')
            return
        self.tcp_sock.send(file.split('/')[-1].encode())
        data = self.tcp_sock.recv(20)
        if data == "N":
            msg = input('文件已经存在，是否继续上传(Y/N)')
            self.tcp_sock.send(msg.encode())
            sleep(0.1)
            if msg == 'N':
                print('上传失败')
                return
        while True:
            msg = f.read(1024)
            if len(msg) < 1024:
                self.tcp_sock.send(msg)
                f.close()
                print('上传成功')
                break
            else:
                self.tcp_sock.send(msg)


def main():
    tcp_sock = socket()
    tcp_sock.connect(ADDR)
    dis = Dispose(tcp_sock)
    while True:
        print("输入L查看文件：")
        print("输入G下载文件")
        print("输入P上传文件")
        print("输入Q退出")
        try:
            msg = input("请输入:")
        except:
            break
        if msg == "L":
            dis.do_file()
        elif msg == 'G':
            dis.get_file()
        elif msg == 'P':
            dis.put_file()
        elif msg == 'Q':
            tcp_sock.close()
            break


if __name__ == '__main__':
    main()
