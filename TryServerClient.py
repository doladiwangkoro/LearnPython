# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 13:33:08 2017

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
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

""" Thread 1 """

def connect_client(s):
    while True:
        try:
            s.connect(('127.0.0.1',5567))
            print('connected to a server')
        except:
            time.sleep(10)
            print("the server is unavailable")
            continue
        else:
            break

""" Thread 2 """

def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 8000
        s = socket.socket()
        print("socket created")
    except socket.error as msg:
        print("socket creation error: "+str(msg))
        
def socket_bind():
    try:
        global host
        global port
        global s
        s.bind((host, port))
        s.listen(5)
        print("waiting for client")
        
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

""" Multithreading """            

def create_workers():
    for _ in range(N):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()
        
def work():
    while True:
        x = queue.get()
        if x == 2:
            socket_create()
            socket_bind()
            accept_connection()
            
        if x == 1:
            connect_client(s)
            

        queue.task_done()
        
def create_jobs():
    for x in N_job:
        queue.put(x)
    queue.join()
    

create_workers()
create_jobs()
for i in all_connection:
    i.close()
