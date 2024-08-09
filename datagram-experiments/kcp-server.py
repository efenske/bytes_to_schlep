import socketserver,threading,datetime,socket,select,time,os,argparse,string
defRecvs = 0
outAddr = '157.166.226.25'
printables = bytes(string.printable,'ascii')

definPort = 31001
defoutPort = 443
defAction = '1stbyte'
defDelta = 10
defExtend = False
trickleDelta = 100
dt = .5
defFrag = -1 #-1 for any fragment
parser = argparse.ArgumentParser()
parser.add_argument('-n','--num-recvs',dest='n',action='store',type=int,default=defRecvs)
parser.add_argument('-i','--input-port',dest='ip',action='store',type=int,default=definPort)
parser.add_argument('-o','--output-port',dest='op',action='store',type=int,default=defoutPort)
parser.add_argument('-a','--action',dest='ac',action='store',type=str,default=defAction) 
parser.add_argument('-d','--delta',dest='delta',action='store',type=int,default=defDelta)
parser.add_argument('-e','--extend',dest='extend',action='store_true',default=defExtend)
parser.add_argument('-dir','--direction',dest='direction',action='store',type=str,default=defExtend)
parser.add_argument('-b','--byte',dest='b',action='store',type=int,default=defExtend)
parser.add_argument('-f','--fragment',dest='frag',action='store',type=int,default=defFrag)
args = parser.parse_args()
outPort,bindPort,n,delta,extend,direction,b,frag = args.op,args.ip,args.n,args.delta,args.extend,args.direction,args.b,args.frag
class handler(socketserver.BaseRequestHandler):
    def handle(self):
        print('connection')
        bytesIn = 0
        bytesOut = 0
        handshook = 0
        global delta
        #counter for how many recv calls have happened from the local obfsproxy #anecdotally takes two before we can ensure handshake has occured
        while True:
            s = self.request
            dat = self.request.recv(10000)
            with open('recvLog.txt','a+') as f:
                f.write(str(dat) + '\n')
            if dat == b'':
                print('Connection terminated by remote host')
                print('In:',bytesIn, 'Out:',bytesOut)
                self.request.close()
                return


if __name__ == '__main__':
    host,port = '127.0.0.1',bindPort
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer((host,port),handler) as server:
        print('In port:',bindPort)
        print('Out port:',outPort)

        server.serve_forever()
