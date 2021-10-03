import socket
import os

def ip_reach_check(ip):
	if os.system('ping -c 1 '+ip) == 0:
 		host_state=True
	else:
 		host_state=False
	return host_state

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(('0.0.0.0',8080))

while(True):

    bytesAddressPair = sock.recvfrom(1024)

    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    print(message)
    print(address)
    if ip_reach_check(message.decode()):
    	sock.sendto(b"Host is reachable",address)
    	break
    else:
    	sock.sendto(b"Host can't be reached",address)
    	break

