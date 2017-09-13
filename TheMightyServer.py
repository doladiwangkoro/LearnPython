# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 12:59:17 2017

@author: D M Dolaputra
"""

import socket
import json
import threading
import time
from queue import Queue

N = 3
N_job = [1, 2, 3]
queue = Queue()
all_connection = []
all_address = []


""" Thread 1 """

def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 5567
        s = socket.socket()
    except socket.error as msg:
        print("socket creation error: "+str(msg))
        
def socket_bind():
    try:
        global host
        global port
        global s
        s.bind((host, port))
        s.listen(5)
        print("waiting")
    except socket.error as msg:
        print("socket bind error: "+str(msg))
        time.sleep(5)
        socket_bind()
        
def accept_connection():
    for c in all_connection:
        c.close()
    del all_connection[:]
    del all_address[:]
    while len(all_connection) < 2:
        try:
            conn, address = s.accept()
            conn.setblocking(1)
            all_connection.append(conn)
            all_address.append(address)
            print("\nConnection is established: "+address[0])
            print(all_connection)
        except:
            print("Error")
            break

""" Thread 2 Given """
"""
def start_turtle():
    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command is not recognized")

def list_connections():
    results = ''
    for i, conn in enumerate(all_connection):
        
        try:
            conn.send(str.encode(''))
            conn.recv(1024)
        except:
            del all_connection[i]
            del all_address[i]
            continue #uncomment this part will stuck the program
        results += str(i) + ' ' + str(all_address[i][0]) + ' ' + str(all_address[i][1]) + '\n'
    print('-----clients-----' + '\n' + results)
    
def get_target(cmd):
    try:
        target = cmd.replace('select', '')
        target = int(target)
        conn = all_connection[target]
        print("You are now connected to " + str(all_address[target][0]))
        print(str(all_address[target][0]) + '> ', end="")
        return conn
    except:
        print("Not a valid connection")
        return None

def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(1024), "utf-8")
                print(client_response, end="")
            if cmd == 'quit':
                break
        except:
            print("connection was lost")
            break
"""    

""" Thread 2 """

def calculation(conn):
    i = 0
    while i < 10:
        dat = conn.recv(1024)
        data = dat.decode('utf-8')
        json_calculate = json.loads(data)
        print("Recieved from client: ",json_calculate)
        newvalue = json_calculate['voltage'][i] + 10
        json_calculate['voltage'].insert(i+1,newvalue)
        data = json.dumps(json_calculate)
        conn.send(str.encode(data))
        print("Sent to client: ",data)
        i = i+1
        
    conn.close()


    
""" Multithreading """            

def create_workers():
    for _ in range(N):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()
        
def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            accept_connection()
            
        if x == 2:
            while len(all_connection) < 1:
                time.sleep(30)
                print("please connect a client"+"\n")
            calculation(all_connection[0])
            
        if x == 3:
            while len(all_connection) < 2:
                time.sleep(30)
                print("please connect another client"+"\n")
            calculation(all_connection[1])
            

        queue.task_done()
        
def create_jobs():
    for x in N_job:
        queue.put(x)
    queue.join()
    

create_workers()
create_jobs()
for i in all_connection:
    i.close()


