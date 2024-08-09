import socket,time
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("127.0.0.1",1080))
#hello
b = b'\x05'
b += b'\x01'
b += b'\x00'
s.send(b)
time.sleep(1)
b = b'\x05'
b += b'\x03'
b += b'\x00'
b += b'\x01'
b += b'\x7f\x00\x00\x01'
b += b'\x18\x79'
s.send(b)
time.sleep(1)
print(int.from_bytes(s.recv(10000)[-2:],'big'))
while True:
    pass
