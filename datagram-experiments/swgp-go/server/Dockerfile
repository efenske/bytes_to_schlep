FROM alpine:latest

RUN apk update && apk add wireguard-tools

# Add WireGuard configuration files
COPY server.conf /etc/wireguard/server.conf

#CMD ["wg-quick", "up", "server"]
