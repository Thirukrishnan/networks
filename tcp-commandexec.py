					#Q1
import socket
import os
from functools import reduce

def route():
    os.system('route print >> abc.txt')
    file=open('abc.txt','r')
    text = bytes(reduce(lambda a,b : a +'\n'+b, list(file)[7:23]),'utf-8')
    return text
def arp():
    os.system('arp -a >> arp.txt')
    file=open('arp.txt','r')
    text = bytes(reduce(lambda a,b : a +'\n'+b, list(file)),'utf-8')
    return text
    
def net():
    os.system('netstat -s >> stat.txt')
    file=open('stat.txt','r')
    text = bytes(reduce(lambda a,b : a +'\n'+b, list(file)),'utf-8')
    return text

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(('0.0.0.0',8080))
sock.listen(5)
while True:
    exchng,addr=sock.accept()
    while exchng:
        data=""
        data=exchng.recv(1024)
        data=data.decode()
        if data == 'R':
            exchng.send(route())
        elif data == 'A':
            exchng.send(arp())
	elif data == 'N':
	    exchng.send(net())
    exchng.close()
