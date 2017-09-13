# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 21:04:46 2017

@author: D M Dolaputra
"""

import socket
import threading
import json
import time
from queue import Queue

N = 2
queue = Queue()
N_job = [1,2]

parameter = {
        'voltage':[2]
        }

fromnodeA = {
        'voltage':[]
        }

fromnodeB = {
        'voltage':[]
        }
    
def create_workers():
    for _ in range(N):
        t = threading.Thread(target=work, args=(lock,))
        t.daemon = True
        t.start()
        
def work(lock):
    while True:
        x = queue.get()
        if x == 1:
            s = socket.socket()
            host = ''
            port = 34567
            s.bind((host,port))

            s.listen(5)
            conn, addr = s.accept()
            print('Got connection from: ',addr)
            j = 0
            while j<5:
                #conn, addr = s.accept()
                #print('Got connection from: ',addr)
                lock.acquire()
                
                data = conn.recv(1024)
                data = data.decode('utf-8')
                jason = json.loads(data)
                print('received from client' + str(addr) + ': ', jason)
            
                fromnodeA['voltage'].insert(j,jason['voltage'][j])
                
                jasonstr = json.dumps(parameter)
                conn.send(str.encode(jasonstr))
                print("sent to client ",jasonstr)
                lock.release()
                j = j+1
                #conn.close()
            
        if x == 2:
            s = socket.socket()
            host = '127.0.0.1'
            port = 23456
            while True:
                try:
                    s.connect((host,port))
                    k = 0
                    while k < 5:
                        lock.acquire()
                        jasonstr = json.dumps(parameter)
                        s.send(str.encode(jasonstr))
                        print("sent to server ",jasonstr)
                    
                        data = s.recv(1024)
                        data = data.decode('utf-8')
                        jason = json.loads(data)
                        print('received from server: ', jason)
                    
                        fromnodeB['voltage'].insert(k,jason['voltage'][k])
                        lock.release()
                        k = k+1 
                        #s.close()
                except socket.error as msg:
                    time.sleep(10)
                    print(msg)
                    continue
                else:
                    break
                
        if x == 3:
            for i in range(5):
                lock.acquire()
                sumothernode = fromnodeA['voltage'][i]+fromnodeB['voltage'][i]
                newvoltage = parameter['voltage'][i]+2*sumothernode
                parameter['voltage'].insert(i+1,newvoltage)
                lock.release()
            
            
            

        queue.task_done()
        
def create_jobs():
    for x in N_job:
        queue.put(x)
    queue.join()
    

lock = threading.Lock()
create_workers()
create_jobs()