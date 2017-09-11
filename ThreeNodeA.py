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

N = 2
queue = Queue()
N_job = [1,2]

parameter = {
        'voltage':[5]
        }

fromnodeB = {
        'voltage':[]
        }

fromnodeC = {
        'voltage':[]
        }
    
def create_workers():
    for _ in range(N):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()
        
def work():
    while True:
        x = queue.get()
        if x == 1:
            s = socket.socket()
            host = ''
            port = 12345
            s.bind((host,port))

            s.listen(5)
            while True:
                conn, addr = s.accept()
                print('Got connection from: ',addr)
                data = conn.recv(1024)
                data = data.decode('utf-8')
                jason = json.loads(data)
                print('received from client' + str(addr) + ': ', jason)
                
                fromnodeB['voltage'].insert(0,jason['voltage'][0])
                
                jasonstr = json.dumps(parameter)
                conn.send(str.encode(jasonstr))
                print("sent to client ",jasonstr)
                conn.close()
            
        if x == 2:
            s = socket.socket()
            host = '127.0.0.1'
            port = 34567
            while True:
                try:
                    s.connect((host,port))
                    jasonstr = json.dumps(parameter)
                    s.send(str.encode(jasonstr))
                    print("sent to server ",jasonstr)
                    
                    data = s.recv(1024)
                    data = data.decode('utf-8')
                    jason = json.loads(data)
                    print('received from server: ', jason)
                    
                    fromnodeC['voltage'].insert(0,jason['voltage'][0])
                    
                    
                    s.close()
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