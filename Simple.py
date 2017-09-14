# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 11:31:43 2017

@author: D M Dolaputra
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 11:18:00 2017

@author: D M Dolaputra
"""

import socket
import threading
N = 2
from queue import Queue
queue = Queue()
N_job = [1,2]

    
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
                data = conn.recv(1024)
                data = data.decode('utf-8')
                print(data)
                print('Got connection from: ',addr)
                conn.send(str.encode('Thank you3'))
                conn.close()
            
        if x == 2:
            s = socket.socket()
            host = '127.0.0.1'
            port = 23456
            while True:
                try:
                    s.connect((host,port))
                    s.send(str.encode("say Thank you 1"))
                    data = s.recv(1024)
                    data = data.decode('utf-8')
                    print(data)
                    s.close()
                except:
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