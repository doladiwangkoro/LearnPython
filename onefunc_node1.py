# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 14:50:14 2017

@author: D M Dolaputra

Node 1 as the server
"""
import socket
import json

host = ''
port = 5560

def setupserver():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket created")
    try:
        s.bind((host,port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete")
    return s

def setupconnection():
    s.listen(1)
    conn, address = s.accept()
    print('connected to', address)
    return conn

#connection = [0,1]

#setup for initial voltage and power (later to be initial parameters)
def init(x,y):
    p = {
    'voltage' : [x],
    'power' : [y]
    }
    return p


def function(conn):
    
    data = conn.recv(2048)
    data = data.decode('utf-8')
    
    neighbor = json.loads(data) #getting voltage and power value from the other node
    print("Recieved from node-2: ",neighbor) #printing data
        
    othernode = neighbor['voltage'][i]
    thisnode = initial['voltage'][i]
    newvoltage = thisnode + 2*othernode
    initial['voltage'].insert(i+1,newvoltage)
    print("Will be sent to node-2: ",initial)
        
    serialized_initial = json.dumps(initial)
    conn.send(str.encode(serialized_initial))
        
    

initial = init(5,0)

s = setupserver()
conn = setupconnection()

i = 0    
while i < 4:
    try:
        function(conn)
        i = i+1
    except:
        break
        print("fail")

    
conn.close()
print("Disconected")
        
        



