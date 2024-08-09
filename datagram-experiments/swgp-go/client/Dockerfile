FROM alpine:latest

RUN apk update && apk add wireguard-tools

# Add WireGuard configuration files
COPY client.conf /etc/wireguard/client.conf

#CMD ["wg-quick", "up", "client"]
