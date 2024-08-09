import socket,random,sys
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
dropPercentage = 0
s.bind(('',31000))
target_port = 4000
st = ''
clientPort = None
minSizeIn = 0
minSizeOut = 0
stats = {
        'packetsOut':0,
        'packetsIn':0,
        'bytesIn':0,
        'bytesOut':0,
        }
while True:
    send = True
    (m,addr) = s.recvfrom(66000)
    if clientPort == None:
        clientPort = addr[1]
        print('Relaying back to',addr)
    if addr[1] == clientPort:
        target = 4000
    else:
        print(clientPort)
        target = clientPort
    if random.randint(0,100) > 100-dropPercentage:
        #send = False
        m = b'\xff' + m[1:]
    print(len(m), '->',target)
    if target == 4000:
        stats['packetsOut'] += 1
        stats['bytesOut'] += len(m)
        if minSizeOut == 0:
            minSizeOut = len(m)
        if len(m) < minSizeOut:
            minSizeOut = len(m)
    else:
        if minSizeIn == 0:
            minSizeIn = len(m)
        if len(m) < minSizeIn:
            minSizeIn = len(m)
        stats['packetsIn'] += 1
        stats['bytesIn'] += len(m)
    stats['minSizeIn'] = minSizeIn
    stats['minSizeOut'] = minSizeOut
    with open('mitmlog.txt','w') as f:
        f.write(str(stats))
    if send:
        s.sendto(m,('127.0.0.1',target))
    
