#!/bin/sh

sudo docker exec -d swgp-go-server ip route del $(sudo docker exec swgp-go-server ip route | grep default)
sudo docker exec -d swgp-go-client ip route del $(sudo docker exec swgp-go-client ip route | grep default)
sudo docker exec -d clab-frr01-router1 ip route del $(sudo docker exec clab-frr01-router3 ip route | grep default)

sudo docker exec -d swgp-go-server ip link add dev wg0 type wireguard 
sudo docker exec -d clab-frr01-PC2 ip addr add dev wg0 192.168.2.1 peer 192.168.2.2
sudo docker exec -d clab-frr01-PC2 wg setconf wg0 myconfig.conf
sudo docker exec -d clab-frr01-PC2 ip link set up dev wg0

sudo docker exec -d clab-frr01-PC3 ip link set eth1 up
sudo docker exec -d clab-frr01-PC3 ip addr add 125.100.23.13/27 dev eth1
sudo docker exec -d clab-frr01-PC3 ip route del $(sudo docker exec clab-frr01-PC3 ip route | grep default)
sudo docker exec -d clab-frr01-PC3 ip route add default via 125.100.23.1 dev eth1

sudo docker exec -d clab-frr01-PC4 ip link set eth1 up
sudo docker exec -d clab-frr01-PC4 ip addr add 125.100.23.17/27 dev eth1
sudo docker exec -d clab-frr01-PC4 ip route del $(sudo docker exec clab-frr01-PC4 ip route | grep default)
sudo docker exec -d clab-frr01-PC4 ip route add default via 125.100.23.1 dev eth1

sudo docker exec -d clab-frr01-PC5 ip link set eth1 up
sudo docker exec -d clab-frr01-PC5 ip addr add 125.100.23.23/27 dev eth1
sudo docker exec -d clab-frr01-PC5 ip route del $(sudo docker exec clab-frr01-PC5 ip route | grep default)
sudo docker exec -d clab-frr01-PC5 ip route add default via 125.100.23.1 dev eth1

sudo docker exec -d clab-frr01-dns ip link set eth1 up
sudo docker exec -d clab-frr01-dns ip addr add 125.100.23.29/27 dev eth1
sudo docker exec -d clab-frr01-dns ip route del $(sudo docker exec clab-frr01-dns ip route | grep default)
sudo docker exec -d clab-frr01-dns ip route add default via 125.100.23.1 dev eth1

sudo docker exec -d clab-frr01-mail ip link set eth1 up
sudo docker exec -d clab-frr01-mail ip addr add 139.123.73.15/25 dev eth1
sudo docker exec -d clab-frr01-mail ip route del $(sudo docker exec clab-frr01-mail ip route | grep default)
sudo docker exec -d clab-frr01-mail ip route add default via 139.123.73.1 dev eth1

sudo docker exec -d clab-frr01-www ip link set eth1 up
sudo docker exec -d clab-frr01-www ip addr add 223.189.12.20/27 dev eth1
sudo docker exec -d clab-frr01-www ip route del $(sudo docker exec clab-frr01-www ip route | grep default)
sudo docker exec -d clab-frr01-www ip route add default via 223.189.12.1 dev eth1

sudo docker exec  clab-frr01-PC1 sh -c "echo 'nameserver 125.100.23.29' > /etc/resolv.conf"
sudo docker exec  clab-frr01-PC2 sh -c "echo 'nameserver 125.100.23.29' > /etc/resolv.conf"
sudo docker exec  clab-frr01-PC3 sh -c "echo 'nameserver 125.100.23.29' > /etc/resolv.conf"
sudo docker exec  clab-frr01-PC4 sh -c "echo 'nameserver 125.100.23.29' > /etc/resolv.conf"
sudo docker exec  clab-frr01-PC5 sh -c "echo 'nameserver 125.100.23.29' > /etc/resolv.conf"
sudo docker exec  clab-frr01-mail sh -c "echo 'nameserver 125.100.23.29' > /etc/resolv.conf"
sudo docker exec  clab-frr01-dns sh -c "echo 'nameserver 125.100.23.29' > /etc/resolv.conf"
sudo docker exec  clab-frr01-www sh -c "echo 'nameserver 125.100.23.29' > /etc/resolv.conf"
sudo docker exec  clab-frr01-router1 sh -c "echo 'nameserver 125.100.23.29' > /etc/resolv.conf"
sudo docker exec  clab-frr01-router2 sh -c "echo 'nameserver 125.100.23.29' > /etc/resolv.conf"
sudo docker exec  clab-frr01-router3 sh -c "echo 'nameserver 125.100.23.29' > /etc/resolv.conf"
sudo docker exec  clab-frr01-router4 sh -c "echo 'nameserver 125.100.23.29' > /etc/resolv.conf"
sudo docker exec  clab-frr01-router5 sh -c "echo 'nameserver 125.100.23.29' > /etc/resolv.conf"
sudo docker exec  clab-frr01-router6 sh -c "echo 'nameserver 125.100.23.29' > /etc/resolv.conf"
sudo docker exec  clab-frr01-router7 sh -c "echo 'nameserver 125.100.23.29' > /etc/resolv.conf"


