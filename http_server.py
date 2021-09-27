# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#import requests
#r = requests.get('http://10.1.67.30/')
#print(r.text)
import subprocess

def send_file(filename,conn):
    file=open(filename,'r')
    for line in file:
        conn.send(bytes(line,encoding='ascii'))
        
import socket

http_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

http_server.bind(('0.0.0.0',80))
http_server.listen(5)

error_code,response=subprocess.getstatusoutput("powershell.exe Get-ChildItem -File")

while True:
    conn,addr=http_server.accept()
    data=conn.recv(1024)
    data=data.decode()
    if 'GET' in data:
        index=data.find('GET')
        end=data.find('H')
        path=data[index+4:end-1]
        print(path)
        if path == '/':
            send_file('index.html',conn)
            continue
        else:
            if path[1::] in response:
                send_file(path[1::],conn)
                continue
            else:
                conn.send(b"404 Not Found")
                break
    
conn.close()
http_server.close()