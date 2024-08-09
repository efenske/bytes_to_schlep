import socket,time

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
header =b''
header += b'\x00\x00'
header += b'\x00'
#header += b'\x03\x00'
header += b'\x01\x7f\x00\x00\x01'
header += b'\x79\x19'
for m in ('','one','two','three','four','five','six','seven'):
    bb = header + bytes(m,'utf-8')
    print('CLIENT',bb)
    s.sendto(bb,('127.0.0.1',1080))
    time.sleep(1)
