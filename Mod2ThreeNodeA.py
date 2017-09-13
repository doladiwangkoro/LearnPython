# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 11:38:27 2017

@author: D M Dolaputra
"""

import socket
import threading
import json
import time
from queue import Queue

N = 6
queue = Queue()
N_job = [1,2,3,4,5,6]
all_addresses = []
all_connections = []
node = 'node1'

parameter = {
        'voltage':[5]
        }

parameterother = {}

addresses = [('127.0.0.1',12345), ('127.0.0.1',23456), ('127.0.0.1',34567)]
connectivity = [0, 1, 1] 

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
        while True:
            conn, addr = s.accept()
            all_addresses.append(addr)
            all_connections.append(conn)
            print('Got connection from: ',addr)
            
    if x == 2:
        b = 0
        while b < 5:
            try:
                data1 = all_connections[0].recv(2048)
                print("data1 received")
                data1 = data1.decode('utf-8')
                print("data1 decoded")
                jason1 = json.loads(data1)
                print("data1loaded")
                print('received from client' + str(all_addresses[0]) + ': ', jason1)
                parameterother['node'+ str(othernode(node)[0])]['voltage'].insert(b,jason1['voltage'][b])
                print(parameterother)
                b = b+1
                #print(b)
            except Exception as msg:
                #lock.release()
                #time.sleep(2)
                #print(msg)
                continue
            
            
    if x == 3:
        c = 0
        while c < 5:
            try:
                data2 = all_connections[1].recv(2048)
                print("data received")
                data2 = data2.decode('utf-8')
                print("data decoded")
                jason2 = json.loads(data2)
                print("data loaded")
                print('received from client' + str(all_addresses[1]) + ': ', jason2)
                parameterother['node'+ str(othernode(node)[1])]['voltage'].insert(c,jason2['voltage'][c])
                print(parameterother)
                c = c+1
                #print(c)
            except Exception as msg:
                #time.sleep(2)
                #lock.release()
                #print(msg)
                continue
            
    if x == 6:
        s1 = socket.socket()
        hostport = othernodeaddr(node)[0]
        while True:
            try:
                s1.connect(hostport)
                jasonstr = json.dumps(parameter)
                s1.send(str.encode(jasonstr))
                print("sent to server "+str(hostport),jasonstr)
                #s.close()
            except Exception as msg:
                #time.sleep(2)
                #print(msg)
                continue
            else:
                break
        d = 0
        while d < 5:
            if len(parameter['voltage']) == d+2:
                jasonstr = json.dumps(parameter)
                s1.send(str.encode(jasonstr))
                print("sent to server "+str(hostport),jasonstr)
                d = d+1
                #print(d)
            else:
                continue
                
            
    if x == 5:
        s2 = socket.socket()
        hostport = othernodeaddr(node)[1]
        while True:
            try:
                s2.connect(hostport)
                jasonstr = json.dumps(parameter)
                s2.send(str.encode(jasonstr))
                print("sent to server "+str(hostport),jasonstr)
                #s.close()
            except Exception as msg:
                #time.sleep(2)
                #print(msg)
                continue
            else:
                break
        e = 0
        while e < 5:
            if len(parameter['voltage']) == e+2:
                jasonstr = json.dumps(parameter)
                s2.send(str.encode(jasonstr))
                print("sent to server "+str(hostport),jasonstr)
                e = e+1
                #print(e)
            else:
                continue

                
    if x == 4:
        f = 0
        while f < 5:
            #time.sleep(5)
            try:
                #lock.acquire()
                currentnode = parameter['voltage'][f]
                #print("the voltage now is: ",currentnode)
                connectednodes = parameterother['node'+ str(othernode(node)[0])]['voltage'][f] + parameterother['node'+ str(othernode(node)[1])]['voltage'][f] 
                #print("the sum of othe voltage is: ",connectednodes)
                newvalue = currentnode + 2*connectednodes
                #print("owyeah")
                parameter['voltage'].insert(f+1,newvalue)
                #print("go get it")
                f = f+1
                #print(f)
                #lock.release()
            except Exception as msg:
                #lock.release()
                #time.sleep(2)
                #print(msg)
                continue
            
    queue.task_done()
        
def create_jobs():
    for x in N_job:
        queue.put(x)
    queue.join()
    
create_workers()
create_jobs()