#!/bin/bash
#path-to-kcptun binary redacted
KCPPATH="REDACTED"
./kill.sh
#setup client, ->2080 client -> 31000 (udp)
echo Spinning up CLIENT
$KCPPATH/client_linux_amd64 -r "127.0.0.1:31000" -l ":2080" -mode fast3 -nocomp -autoexpire 900 -sockbuf 16777217 -dscp 46 >clientLog.txt &
#setup server, >4000 server -> 31001
echo Spinning up SERVER
$KCPPATH/server_linux_amd64 -t "127.0.0.1:31001" -l ":4000" -mode fast3 -nocomp -sockbuf 16777217 -dscp 46 >serverLog.txt &
sleep 2
#server should be listening on 31001
echo Spinning up LISTENER
python3 kcp-server.py -i 31001 &
sleep 2
#udp mitm should be listening to 31000, and relay messages to 4000
python3 kcp-mitm.py $1 &
#client should connect to lh:2080 (curl)
python3 kcp-client.py
sleep 120
./kill.sh
mv mitmlog.txt mitmlog-$1.txt
mv recvLog.txt recvLog-$1.txt

