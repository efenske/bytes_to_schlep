#!/bin/python3
import struct
import socket
from time import sleep

def create_ipv4_packet(src_ip, dst_ip):
    # IP header fields
    version = 4  # IPv4
    ihl = 5      # Internet Header Length
    tos = 0      # Type of Service
    total_length = 20 + 20  # IP header + TCP header
    identification = 54321  # Identification
    flags = 0     # Flags
    fragment_offset = 0  # Fragment Offset
    ttl = 255     # Time to Live
    protocol = socket.IPPROTO_TCP  # Protocol (TCP)
    checksum = 0  # Initial checksum value
    src_ip_packed = socket.inet_aton(src_ip)  # Source IP address
    dst_ip_packed = socket.inet_aton(dst_ip)  # Destination IP address

    # Construct IP header
    ip_header = struct.pack("!BBHHHBBH4s4s", (version << 4) + ihl, tos, total_length, identification,
                            (flags << 13) + fragment_offset, ttl, protocol, checksum, src_ip_packed, dst_ip_packed)

    # Calculate IP header checksum
    checksum = calculate_checksum(ip_header)

    # Update IP header with calculated checksum
    ip_header = struct.pack("!BBHHHBBH4s4s", (version << 4) + ihl, tos, total_length, identification,
                            (flags << 13) + fragment_offset, ttl, protocol, checksum, src_ip_packed, dst_ip_packed)

    return ip_header

def calculate_checksum(data):
    # Function to calculate checksum
    checksum = 0
    # If the length of the data is odd, pad it with a zero byte
    if len(data) % 2 != 0:
        data += b'\x00'
    for i in range(0, len(data), 2):
        w = (data[i] << 8) + (data[i+1])
        checksum += w
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = ~checksum & 0xffff
    return checksum

def send_ipv4_packet(packet):
    # Send the packet using a raw socket
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    s.sendto(packet, ("10.0.0.2", 0))  # Destination IP address and port (port 0)

def main():
    # Define source and destination IP addresses
    src_ip = "10.0.0.3"
    dst_ip = "10.0.0.2"

    # Create the IPv4 packet
    ipv4_packet = create_ipv4_packet(src_ip, dst_ip)

    # Print the packet in hexadecimal format
    print("IPv4 Packet in Hexadecimal:")
    print(ipv4_packet.hex())

    # Send the packet
    while True:
        send_ipv4_packet(ipv4_packet)
        print("Packet sent successfully.")
        sleep(5)

if __name__ == "__main__":
    main()

