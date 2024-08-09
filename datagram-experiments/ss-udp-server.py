import socket

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('',31001))
print('SERVER: listening on port 31001')
while True:
    m, addr = s.recvfrom(66000)
    print('SERVER:',m,addr)
    s.sendto(b'',addr)

