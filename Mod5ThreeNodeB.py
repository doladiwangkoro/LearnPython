# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 19:34:13 2017

@author: D M Dolaputra
"""

import socket
import threading
import json
import time
from queue import Queue

t = 5
queue = Queue()
all_addresses = []
all_connections = []
all_client_sockets = []
node = 'node2'

parameter = {
        'voltage':[10]
        }

parameterother = {}

addresses = [('127.0.0.1',12345), ('127.0.0.1',23456), ('127.0.0.1',34567)]
connectivity = [1, 0, 1] 

def count_one():
    one = 0
    for i in connectivity:
        if i == 1:
            one = one + 1
    return one

def count_workers():
    N = count_one() + 1
    return N

N = count_workers()


def array_jobs():
    N_job = []
    for i in range((count_workers())):
        N_job.append(i+1)
    return N_job

N_job = array_jobs()


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
    x = queue.get()
    
    if x == 1:
        s = socket.socket()
        s.bind(thisnode(node))

        s.listen(5)
        while len(all_addresses) < count_one():
            conn, addr = s.accept()
            all_addresses.append(addr)
            all_connections.append(conn)
            print('Got connection from: ',addr)
            
    
    for j in range(count_one()):         
        if x == j+2:
            s1 = socket.socket()
            all_client_sockets.append(s1)
            hostport = othernodeaddr(node)[j]
            while True:
                try:
                    all_client_sockets[j].connect(hostport)
                    jasonstr = json.dumps(parameter)
                    all_client_sockets[j].send(str.encode(jasonstr))
                    print("sent to server "+str(hostport),jasonstr)
                except Exception as msg:
                    continue
                else:
                    break
        
                
            
#    if x == 3:
#        s2 = socket.socket()
#        all_client_sockets.append(s2)
#        hostport = othernodeaddr(node)[1]
#        while True:
#            try:
#                all_client_sockets[1].connect(hostport)
#                jasonstr = json.dumps(parameter)
#                all_client_sockets[1].send(str.encode(jasonstr))
#                print("sent to server "+str(hostport),jasonstr)
#            except Exception as msg:
#                continue
#            else:
#                break
            
    queue.task_done()
        
def create_jobs():
    for x in N_job:
        queue.put(x)
    queue.join()
    
create_workers()
create_jobs()

i = 0
while i < 5:
    for z in range(len(all_connections)):
        data1 = all_connections[z].recv(2048)
        print("data1 received",data1)
        data1 = data1.decode('utf-8')
        print("data1 decoded",data1)
        jason1 = json.loads(data1)
        print("data1loaded")
        print('received from client' + str(all_addresses[z]) + ': ', jason1)
        parameterother['node'+ str(othernode(node)[z])]['voltage'].insert(i,jason1['voltage'][i])
        print(parameterother)
    
    time.sleep(t)
    currentnode = parameter['voltage'][i]
    connectednodes = 3#parameterother['node'+ str(othernode(node)[0])]['voltage'][i] + parameterother['node'+ str(othernode(node)[1])]['voltage'][i] 
    newvalue = currentnode + 2*connectednodes
    parameter['voltage'].insert(i+1,newvalue)
    
    for x in range(len((all_client_sockets))):
        jasonstr = json.dumps(parameter)
        all_client_sockets[x].send(str.encode(jasonstr))
        print("sent to SERVER "+str(othernodeaddr(node)[x]),jasonstr)
#    
    i = i+1