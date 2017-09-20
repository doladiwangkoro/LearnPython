# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 16:50:26 2017

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
node = 'node2'

parameter = {
        'voltage':[10]
        }

parameterother = {}

addresses = [('127.0.0.1',12345), ('127.0.0.1',23456), ('127.0.0.1',34567)]
connectivity = [1, 0, 1] 

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
        i = 0
        while i < 2:
            conn, addr = s.accept()
            all_addresses.append(addr)
            all_connections.append(conn)
            print('Got connection from: ',addr)
            
    if x == 2:
        a = 0
        while a < 5:
            try:
                data1 = all_connections[0].recv(2048)
                print("data1 received",data1)
                data1 = data1.decode('utf-8')
                print("data1 decoded",data1)
                jason1 = json.loads(data1)
                print("data1loaded")
                print('received from client' + str(all_addresses[0]) + ': ', jason1)
                parameterother['node'+ str(othernode(node)[0])]['voltage'].insert(a,jason1['voltage'][a])
                print(parameterother)
                a = a+1
                #print(b)
            except Exception as msg:
                #lock.release()
                #time.sleep(2)
                #print(msg)
                continue
            
            
    if x == 3:
        b = 0
        while b < 5:
            try:
                data2 = all_connections[1].recv(2048)
                print("data2 received", data2)
                data2 = data2.decode('utf-8')
                print("data2 decoded")
                jason2 = json.loads(data2)
                print("data2 loaded")
                print('received from client' + str(all_addresses[1]) + ': ', jason2)
                parameterother['node'+ str(othernode(node)[1])]['voltage'].insert(b,jason2['voltage'][b])
                print(parameterother)
                b = b+1
                #print(b)
            except Exception as msg:
                #lock.release()
                #time.sleep(2)
                #print(msg)
                continue
            
    if x == 4:
        s1 = socket.socket()
        hostport = othernodeaddr(node)[0]
        while True:
            try:
                time.sleep(10)
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
        c = 0
        while c < 5:
            if len(parameter['voltage']) == c+2:
                jasonstr = json.dumps(parameter)
                s1.send(str.encode(jasonstr))
                print("sent to SERVER "+str(hostport),jasonstr)
                c = c+1
                #print(d)
            else:
                continue
                
            
    if x == 5:
        s2 = socket.socket()
        hostport = othernodeaddr(node)[1]
        while True:
            try:
                time.sleep(10)
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
        d = 0
        while d < 5:
            if len(parameter['voltage']) == d+2:
                jasonstr = json.dumps(parameter)
                s2.send(str.encode(jasonstr))
                print("sent to SERVER "+str(hostport),jasonstr)
                d = d+1
                #print(e)
            else:
                continue

                
    if x == 6:
        e = 0
        while e < 5:
            #print('e value is ',e)
            if e == 0:
                time.sleep(10)
            try:
                #lock.acquire()
                currentnode = parameter['voltage'][e]
                #print("the voltage now is: ",currentnode)
                connectednodes = parameterother['node'+ str(othernode(node)[0])]['voltage'][e] + parameterother['node'+ str(othernode(node)[1])]['voltage'][e] 
                #print("the sum of othe voltage is: ",connectednodes)
                newvalue = currentnode + 2*connectednodes
                #print("owyeah")
                parameter['voltage'].insert(e+1,newvalue)
                #print("go get it")
                e = e+1
                #print('e value is ',e)
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