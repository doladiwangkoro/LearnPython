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

t = 5 #delay time to avoid conflicting data
t1 = 0
queue = Queue()
all_addresses = [] #all addresses from the connected nodes
all_connections = [] #all connection from the connected nodes (to perform server-client data transfer)
all_client_sockets = [] #sockets prepared for a client to connect to multiple servers
node = 'node2' #observed node (vary for each file)
num_iteration = 5 #expected number of iterations

#this node initial parameters (vary for each file)
parameter = {
        'voltage':[10]
        }

#json for storing other connected nodes' parameters
parameterother = {}

# All nodes' addresses 
addresses = [('127.0.0.1',12345), ('127.0.0.1',23456), ('127.0.0.1',34567), ('127.0.0.1',45678)]
# How this node is connected to the other nodes (vary for each file)
connectivity = [1, 0, 1, 0] 

#counting how many connections
def count_one():
    one = 0
    for i in connectivity:
        if i == 1:
            one = one + 1
    return one

#counting how many threads should be made
def count_workers():
    N = count_one() + 1
    return N

N = count_workers()

#producing a list of numbers from 0 to N
def array_jobs():
    N_job = []
    for i in range((count_workers())):
        N_job.append(i+1)
    return N_job

N_job = array_jobs()

#calling this node's address
def thisnode(n):
    return addresses[int(n[4])-1]

#producing list of other connected nodes index
def othernode(n):
    other = []
    for i in range(len(connectivity)):
        if connectivity[i] == 1:
            other.append(i+1)
    return other

#preparing storage for other connected nodes' parameter
for i in othernode(node):
    parameterother['node'+ str(i)] = {'voltage':[]}
        
#producing list of other connected nodes' address
def othernodeaddr(n):
    other = []
    for i in range(len(addresses)):
        if connectivity[i] == 1:
            other.append(addresses[i])
    return other

#starting the multithreading
def create_workers():
    for _ in range(N):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

#multithreading part which consists of establishing connections to other connected nodes
#One thread serves as a server and accept connections until all the connection in the connectivity matrix is connected
#The other thread serves as clients to deliver initial value          
def work():
    x = queue.get()
    
    #server part, running until all connection is connected
    if x == 1:
        s = socket.socket()
        s.bind(thisnode(node))

        s.listen(5)
        while len(all_addresses) < count_one():
            conn, addr = s.accept()
            all_addresses.append(addr)
            all_connections.append(conn)
            print('Got connection from: ',addr)
            
    #clients part
    for j in range(count_one()):         
        if x == j+2:
            s1 = socket.socket()
            all_client_sockets.append(s1)
            hostport = othernodeaddr(node)[j]
            while True:
                try:
                    all_client_sockets[j].connect(hostport)
                    jasonstr = json.dumps(parameter)
                    time.sleep(t1)
                    all_client_sockets[j].send(str.encode(jasonstr))
                    print("sent to server "+str(hostport),jasonstr)
                except Exception as msg:
                    continue
                else:
                    break
            
    queue.task_done()

#multithreading        
def create_jobs():
    for x in N_job:
        queue.put(x)
    queue.join()
    
create_workers()
create_jobs()


i = 0
while i < num_iteration:
    for z in range(len(all_connections)):
        #receiving data from the connections and store them in the json
        data1 = all_connections[z].recv(1024)
        print("data1 received",data1)
        data1 = data1.decode('utf-8')
        print("data1 decoded",data1)
        jason1 = json.loads(data1)
        print("data1loaded")
        print('received from client' + str(all_addresses[z]) + ': ', jason1)
        parameterother['node'+ str(othernode(node)[z])]['voltage'].insert(i,jason1['voltage'][i])
        print(parameterother)
    
    #Calculation part
    time.sleep(t)
    currentnode = parameter['voltage'][i]
    connectednodes = 0 
    for y in othernode(node):
        connectednodes = connectednodes + parameterother['node'+ str(y)]['voltage'][i] 
    newvalue = currentnode + 2*connectednodes
    parameter['voltage'].insert(i+1,newvalue)
    
    #Transmitting updated parameters to the neighboring nodes
    for x in range(len((all_client_sockets))):
        jasonstr = json.dumps(parameter)
        all_client_sockets[x].send(str.encode(jasonstr))
        print("sent to SERVER "+str(othernodeaddr(node)[x]),jasonstr)
    
    i = i+1