import socket,random
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('',31000))
target_port = 8388
init_port = 0
while True:
    (m,addr) = s.recvfrom(66000)
    if addr[1] == target_port:
        t = init_port
    else:
        if not init_port:
            init_port = addr[1]
        t = target_port

    print('MITMPROXY:->',len(m),t)
    s.sendto(m,('127.0.0.1',t))

