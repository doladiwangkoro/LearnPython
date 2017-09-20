# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 19:34:12 2017

@author: D M Dolaputra
"""

import time

def main_node(thenode):

    import socket
    import threading
    import json
    import time
    from queue import Queue
    from ast import literal_eval as tup
    
    t = 0 #delay time to avoid conflicting data
    t1 = 0
    queue = Queue()
    all_addresses = [] #all addresses from the connected nodes
    all_connections = [] #all connection from the connected nodes (to perform server-client data transfer)
    all_client_sockets = [] #sockets prepared for a client to connect to multiple servers
    node = 'node'+str(thenode) #observed node
    num_iteration = 1000 #expected number of iterations
    
    #this node initial parameters (according to input)
    parameter = {
            'voltage':[0],
            'power':[0],
            'lambda':[0]
            }
    
    #conductivity for each connection. The 2nd element in 'node1' means conductivity between node 1 and 2
    all_conductivity = {
            'node1':[0,100,0,0],
            'node2':[100,0,0,0],
            'node3':[0,0,0,0],
            'node4':[0,0,0,0],
            }
    
    #constants
    alpha = 0.1485
    beta = 0.0056
    gamma = 0.005
    
    #Generators
    max_gen = [10000, 0, 0, 0]
    
    #Loads
    max_load = [0, 5000, 0, 0]
    
    #quadratic coefficient
    a_n = [0.45, 0.36, 0, 0]
    
    #linear coefficient
    b_n = [100, 10, 0, 0]
    
    #json for storing other connected nodes' parameters
    parameterother = {}
    
    # All nodes' addresses 
    addresses = [('127.0.0.1',12345), ('127.0.0.1',23456), ('127.0.0.1',34567), ('127.0.0.1',45678)]
    
    all_connectivity = {
            'node1':[0,1,0,0],
            'node2':[1,0,0,0],
            'node3':[0,0,0,0],
            'node4':[0,0,0,0],
            } 
    
    # How this node is connected to the other nodes
    connectivity = all_connectivity[node]
    
    #calling conductivity
    conductivity = all_conductivity[node]
    
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
    
    #if n = 'node1', return 0, etc
    def nodeindex(n):
        return int(n[4]) - 1
    
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
        parameterother['node'+ str(i)] = {
            'voltage':[],
            'power':[],
            'lambda':[]
            }
            
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
                        jasonstr = (json.dumps(parameter)+',')
                        time.sleep(t1)
                        all_client_sockets[j].send(str.encode(jasonstr))
                        #print("sent to server "+str(hostport),jasonstr)
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
        
    time.sleep(t)
    create_workers()
    create_jobs()
    
    
    i = 0
    while i < num_iteration:
        for z in range(len(all_connections)):
            #receiving data from the connections and store them in the json
            data1 = all_connections[z].recv(999999)
            #print("data1 received",data1)
            data1 = data1.decode('utf-8')
            #print("data1 decoded",data1)
            jason1 = tup(data1)
            #print("data1loaded")
            #print('received from client' + str(all_addresses[z]) + ': ', jason1)
            parameterother['node'+ str(othernode(node)[z])]['voltage'].insert(i,jason1[0]['voltage'][i])
            parameterother['node'+ str(othernode(node)[z])]['lambda'].insert(i,jason1[0]['lambda'][i])
            parameterother['node'+ str(othernode(node)[z])]['power'].insert(i,jason1[0]['power'][i])
            #print(parameterother)
        
        #Calculation part

        #oldvalue setup
        oldlambda = parameter['lambda'][i]
        oldvoltage = parameter['voltage'][i]
        oldpower = parameter['power'][i]
        
        #Lambda Calculation
        sum_cond = 0
        for y1 in conductivity:
            sum_cond = sum_cond + y1
            
        sum_lambda_times_cond = 0
        for y2 in othernode(node):
            sum_lambda_times_cond = sum_lambda_times_cond + parameterother['node'+str(y2)]['lambda'][i]*conductivity[y2-1]
        
        sum_volt_diff_times_cond = 0
        for y3 in othernode(node):
            sum_volt_diff_times_cond = sum_volt_diff_times_cond + conductivity[y3-1]*(oldvoltage-parameterother['node'+str(y3)]['voltage'][i])
            
        newlambda = oldlambda - beta*(oldlambda*sum_cond - sum_lambda_times_cond) - alpha*(oldpower - max_load[nodeindex(node)] - sum_volt_diff_times_cond)
        parameter['lambda'].insert(i+1,newlambda)
        
        
        #Power Calculation
        newpower = (oldlambda - b_n[nodeindex(node)])/a_n[nodeindex(node)]
        if newpower > max_gen[nodeindex(node)]:
            newpower = max_gen[nodeindex(node)]
        elif newpower < 0:
            newpower = 0
        else:
            newpower = newpower
        parameter['power'].insert(i+1,newpower)
        
        #Voltage Calculation
        newvoltage = oldvoltage - gamma*(-oldpower + max_load[nodeindex(node)] + sum_volt_diff_times_cond)
        parameter['voltage'].insert(i+1,newvoltage)
            
        
        #Transmitting updated parameters to the neighboring nodes
        for x in range(len((all_client_sockets))):
            jasonstr = (json.dumps(parameter)+',')
            all_client_sockets[x].send(str.encode(jasonstr))
            #print("sent to SERVER "+str(othernodeaddr(node)[x]),jasonstr)
        
        i = i+1
        
    print('voltage: ',parameter['voltage'][i])
    print('power: ',parameter['power'][i])
    print('lambda: ',parameter['lambda'][i])
    time.sleep(30)



