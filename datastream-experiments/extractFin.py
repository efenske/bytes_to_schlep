#!/usr/bin/env python3
import argparse
class Experiment:
    def __init__(self,logFileEntry):
        self.name = logFileEntry.split('||')[0]
        self.frames = []
        self.error = False
        self.startTime = int(logFileEntry.split('||')[1])
        self.nextStartTime = None
        self.serverRecvTimes = 0
        self.clientRecvTimes = 0
        self.serverRecv = 0
        self.clientRecv = 0
        self.serverSent = 0
        self.clientSent = 0
    def dataTransfer(self):
        ended = False
        for f in self.frames:
            if f[3] != '0' or f[2] != '0':
                ended = True
            if f[1] == '31004':
                self.serverRecv += int(f[4])
                if f[4] != '0' and not ended: self.serverRecvTimes += 1
            if f[0] == '31004':
                self.serverSent += int(f[4])
            if f[1] == '31000':
                self.clientSent += int(f[4])
            if f[0] == '31000':
                self.clientRecv += int(f[4])
                if f[4] != '0' and not ended: self.clientRecvTimes += 1
    def __str__(self):
        s = f"Name: {self.name}\n\tFrames: {len(self.frames)}\n"
        if self.error:
            s += '\tNo data for experiment'
            return s
        s += f'\tClient got: {self.clientRecv} over {self.clientRecvTimes} messages,  sent {self.clientSent}\n'
        s += f'\tServer got: {self.serverRecv}, over {self.serverRecvTimes} messages, sent {self.serverSent}\n'
        s += f'\tTerminated by {self.getFin()}\n'
        return s
    def fullPrint(self):
        s = str(self)
        for f in self.frames:
            if int(f[4]) == 0 and f[2] == '0' and f[3] == '0':
                continue
            elif f[2] == '1':
                s += '\t\tFIN ' + self.resolvePort(f[0],f[1]) + '\n'
            elif f[3] == '1':
                s += '\t\tRST ' + self.resolvePort(f[0],f[1]) + '\n' 
            else:
                s += '\t\t' + f[4] + ' ' + self.resolvePort(f[0],f[1]) + '\n' 
        print(s)
    def resolvePort(self,src,dst):
        if self.error:
            return 'ERR'
        if src in ('31000','31001','31002','10086','31003','31004') and dst in ('31000','31001','31002','10086','31003','31004'):
            return '???????????? ' + src + '->' + dst
        if dst == '31000':
            return 'CLIENT -> CLIENTPROXYMITM'
        if src == '31000':
            return 'CLIENTPROXYMITM -> CLIENT' 
        if dst == '31001':
            return 'CLIENTPROXYMITM -> CLIENTPROXY' 
        if src == '31001':
            return 'CLIENTPROXY -> CLIENTPROXYMITM'
        if dst == '31002':
            return 'CLIENTPROXY -> MITM'
        if src == '31002':
            return 'MITM -> CLIENTPROXY' 
        if dst == '10086':
            return 'MITM -> SERVERPROXY'
        if src == '10086':
            return 'SERVERPROXY -> MITM'
        if dst == '31003':
            return 'SERVERPROXY -> SERVERPROXYMITM'
        if src == '31003':
            return 'SERVERPROXYMITM -> SERVERPROXY'
        if dst == '31004':
            return 'SERVERPROXYMITM -> SERVER'
        if src == '31004':
            return 'SERVER -> SERVERPROXYMITM'

        return '???????????? ' + src + '->' + dst
        
    def setNextStartTime(self,t):
        self.nextStartTime = t
    def getFin(self):
        if self.error:
            return ''
        for f in self.frames:
            if f[2] == '1':
                return f"FIN: {self.resolvePort(f[0],f[1])}"
            if f[3] == '1':
                return f"RST: {self.resolvePort(f[0],f[1])}"

    def extractFrames(self,tsharkData):
        for frame in tsharkData:
            if not frame:
                continue
            frame = frame.split('\t')
            if float(frame[-1]) >= self.startTime:
                if self.nextStartTime == None or float(frame[-1]) <= self.nextStartTime:
                    self.frames.append(frame)
        if len(self.frames) == 0:
            self.error = True
        else:
            self.dataTransfer()
class DataSet:
    def __init__(self,tsharkFileName,logFileName):
        self.experiments = []
        L = self.experiments
        with open(tsharkFileName) as f:
            data = f.read().split('\n')
        with open(logFileName) as f:
            ll = f.read().split('\n')
            for i in range(len(ll)): 
                if not ll[i]:
                    continue
                L.append(Experiment(ll[i]))
                if len(L) > 1:
                    L[-2].setNextStartTime(L[-1].startTime)
        for i in L:
            i.extractFrames(data)
    def summary(self):
        for i in self.experiments:
            print(i)
    def full(self):
        for i in self.experiments:
            i.fullPrint()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--tshark-filename',dest='ts',action='store',type=str,default='tshark.txt')
    parser.add_argument('-l','--log-filename',dest='lf',action='store',type=str,default='mainLog.txt')
    parser.add_argument('-v','--verbose',dest='verb',action='store_true',default=False)
    parser.add_argument('-f','--final',dest='final',action='store_true',default=False)
    args,unknown = parser.parse_known_args()
        
    d = DataSet(args.ts,args.lf)
    if args.final:
        print(d.experiments[-1])
    elif not args.verb:
        d.summary() 
    else:
        d.full()
