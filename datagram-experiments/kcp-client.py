import socket,time

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('127.0.0.1',2080))
for k in range(10):
    s.send(b'A')

    time.sleep(2)
