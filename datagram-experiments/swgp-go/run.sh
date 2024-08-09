#!/bin/sh

# Update the docker images
sudo docker build ./swgp-go -t swgp-go

# Start the docker compose
echo "Starting Docker Compose"
sudo docker compose up -d

# Remove the default route from the client and server
sudo docker exec -d swgp-go-server-1 ip -6 route del $(sudo docker exec swgp-go-server-1 ip -6 route | grep default)
sudo docker exec -d swgp-go-client-1 ip -6 route del $(sudo docker exec swgp-go-client-1 ip -6 route | grep default)

# Add a default route to the client and server
sudo docker exec -d swgp-go-server-1 ip -6 route add default via 2001:1111::3 dev eth0
sudo docker exec -d swgp-go-client-1 ip -6 route add default via 2001:2222::3 dev eth0

# Start up the swgp-go proxy
echo "Intializing swgp-go proxy..."
sudo docker exec -d swgp-go-server-1 ./swgp-go -confPath /etc/wireguard/config.json
sudo docker exec -d swgp-go-client-1 ./swgp-go -confPath /etc/wireguard/config.json

# Start up the wireguard
echo "Starting wireguard..."
sudo docker exec -d swgp-go-server-1 wg-quick up server
sudo docker exec -d swgp-go-client-1 wg-quick up client
sleep 5
# Open up wireshark sessions
echo "Starting capture..."
sudo docker run -d --rm --net container:swgp-go-client-1 nicolaka/netshoot tshark -i lo
sudo docker run -d --rm --net container:swgp-go-router-1 nicolaka/netshoot tshark

# Get the container id's for the wireshark instances
CAPTURES=$(sudo docker ps | grep nicolaka | cut -d ' ' -f 1)
echo "$CAPTURES"

# We're going to wait for about 30 seconds to allow for keepalives, etc.
sleep 30

echo "Generating Traffic..."
# Execute a python script to generate some traffic (this will send every 5 seconds)
sudo docker exec -d swgp-go-client-1 /etc/wireguard/send_traffic.py

# Let the captures run for ~ 5 min.
sleep 300

echo "Copying back pcaps and cleaning up..."
# Copy all the pcaps back over to the host
for CAPTURE in $CAPTURES; do
    PCAP=$(sudo docker exec -it $CAPTURE ls --color=never /tmp |  sed 's/\r$//')
    sudo docker cp "$CAPTURE":"/tmp/${PCAP}" .
    sudo chmod +r ${PCAP}
    sudo docker kill $CAPTURE
done

# kill off the docker compose
sudo docker compose down --rmi all


