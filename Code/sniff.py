from scapy.all import *

def show(packet):
	print(packet.summary())
	if IP in packet:
        	print("Source IP: ", packet[IP].src)
        	print("Destination IP: " ,packet[IP].dst)
        	print("====================================================")
	
print("Dang nghe len thong tin ...")
sniff(iface="ens33", prn=show, filter="ip and (icmp or udp or tcp)", store=0)
