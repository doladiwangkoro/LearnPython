# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 11:18:00 2017

@author: D M Dolaputra
"""

import socket
import threading
import json
import time
from queue import Queue

N = 3
queue = Queue()
N_job = [1,2,3]
all_addresses = []
node = 'node1'

parameter = {
        'voltage':[5]
        }

parameterother = {}

addresses = [('127.0.0.1',12345), ('127.0.0.2',23456), ('127.0.0.3',34567)]
connectivity = [1, 1, 0] 

def thisnode(n):
    return addresses[int(n[4])-1]

def othernode(n):
    other = []
    for i in range(len(connectivity)):
        if connectivity[i] == 1:
            other.append(i+1)
    return other

for i in othernode(node):
    parameterother['node'+ str(i)] = {'voltage':[]}
        

def othernodeaddr(n):
    other = []
    for i in range(len(addresses)):
        if connectivity[i] == 1:
            other.append(addresses[i])
    return other

    
def create_workers():
    for _ in range(N):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()
        
def work():
    #while True:
    x = queue.get()
    if x == 1:
        s = socket.socket()
        s.bind(thisnode(node))

        s.listen(5)
        while len(all_addresses)<2:
            for i in range(2):
                conn, addr = s.accept()
                all_addresses.append(addr)
                print('Got connection from: ',addr)
                data = conn.recv(1024)
                data = data.decode('utf-8')
                jason = json.loads(data)
                print('received from client' + str(addr) + ': ', jason)
                
                parameterother['node'+ str(othernode(node)[i])]['voltage'].insert(i,jason['voltage'][0])
                #conn.close()
        
    if x == 2:
        s1 = socket.socket()
        hostport = othernodeaddr(node)[0]
        while True:
            try:
                s1.connect(hostport)
                jasonstr = json.dumps(parameter)
                s1.send(str.encode(jasonstr))
                print("sent to server "+str(hostport),jasonstr)
                #s.close()
            except:
                time.sleep(10)
                print("waiting for server")
                continue
            else:
                break
            
    if x == 3:
        s2 = socket.socket()
        hostport = othernodeaddr(node)[1]
        while True:
            try:
                s2.connect(hostport)
                jasonstr = json.dumps(parameter)
                s2.send(str.encode(jasonstr))
                print("sent to server "+str(hostport),jasonstr)
                #s.close()
            except:
                time.sleep(10)
                print("waiting for server")
                continue
            else:
                break

    queue.task_done()
        
def create_jobs():
    for x in N_job:
        queue.put(x)
    queue.join()
    

create_workers()
create_jobs()