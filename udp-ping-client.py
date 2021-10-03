import socket

client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
addr=(('127.0.0.1',8080))
while True:
	data=input('Enter ip or url to ping: ')
	if data.isalpha():
		ip=socket.gethostbyname(data)
	else:
		ip=bytes(data,encoding='utf-8')
	client.sendto(ip,addr)
	data=client.recvfrom(1024)
	response=data[0].decode()
	print(response)
	break

client.close()