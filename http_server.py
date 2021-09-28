
import subprocess
import os

def PUT(filename,data):
    file=open(filename,'w')
    file.write(data)
    file.close()
    
def POST(filename,data):
    file=open(filename,'a')
    data='\n'+data
    file.write(data)
    file.close()
    
    
def DELETE(filename):
    os.system('powershell Remove-Item '+filename)
    
def send_file(filename,conn):
    file=open(filename,'r')
    for line in file:
        conn.send(bytes(line,encoding='ascii'))
        
import socket

http_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

http_server.bind(('0.0.0.0',80))
http_server.listen(5)

error_code,response=subprocess.getstatusoutput("powershell.exe Get-ChildItem -File")        #prints out files in the directory

while True:
    conn,addr=http_server.accept()
    data=conn.recv(1024)
    data=data.decode()
    index=data.find('GET')
    end=data.find('H')
    path=data[index+4:end-1]      #GET / 3 chars for Request method and 1 for space so after 4 we get the path
    
    if 'GET' in data:
        if path == '/':
            send_file('index.html',conn)
            continue
        else:
            filename=path[1::]
            if filename in response:
                send_file(filename,conn)
                continue
            else:
                conn.send(b"404 Not Found")
                break
            
    elif 'PUT' in data:      
                                        #Creates a resource on the server 
        index=data.find('urlencoded')
        filedata=data[index+14::]               #Finds the body of the htttp request method
        PUT(path,filedata)
        break
    
    elif 'POST' in data:                        #Modifies existing resource on the server
        filename=path[3::]                       #since request method is of 4 chars
        if filename in response:
            index=data.find('urlencoded')
            filedata=data[index+14::]
            POST(filename,filedata)
            conn.send(b'200 OK')
            break
        else:
            conn.send(b'404 Not Found')
            break
        
    elif 'DELETE' in data:                      #Deletes a file mentioned in the path
        filename=path[5::]                      #Separate filename from actual path mentioned
        if filename in response:
            DELETE(filename)
            conn.send(b'200 OK')
            break
        else:
            conn.send(b'404 Not Found')
            break
        break
    else:
        conn.send(b'Invalid Request Method')
        break
        
conn.close()
http_server.close()
