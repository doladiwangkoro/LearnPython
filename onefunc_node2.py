# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 15:32:34 2017

@author: D M Dolaputra

Node 2 as the client
"""

import socket
import json
import time

host = '127.0.0.1'
port = 5560

def setupserver():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket created")
    while True:
        try:
            s.connect((host,port))
        except:
            continue
        else:
            break
    print("Connected to node 1")
    return s

#connection = [1,0]

#setup for initial voltage and power (later to be initial parameters)
def init(x,y):
    p = {
    'voltage' : [x],
    'power' : [y]
    }
    return p


def function(s):
        
    data = s.recv(2048)
    data = data.decode('utf-8')
        
    neighbor = json.loads(data) #getting voltage and power value from the other node
    print("Recieved from node-1: ",neighbor) #printing data
        
    othernode = neighbor['voltage'][i]
    thisnode = initial['voltage'][i]
    newvoltage = thisnode + 2*othernode
    initial['voltage'].insert(i+1,newvoltage)
    print("Will be sent to node-1: ",initial)
        
    serialized_initial = json.dumps(initial)
    s.send(str.encode(serialized_initial))
        
    
initial = init(10,0)

s = setupserver()

serialized_init = json.dumps(initial)
s.send(str.encode(serialized_init))

i = 0    
while i < 4:
    try:
        function(s)
        i = i+1
    except:
        break
        print("fail")
    
s.close()
print("Disconnected")
