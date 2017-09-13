# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 18:53:33 2017

@author: ddolaputra
"""

import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',5650))
print("Listening ...") #waiting for a connection

s.listen(10)

connection, address = s.accept() #accepting connection from a client 
print("Connected to the client", address)

### The client is taking information and sending it here ###

while True:
    dat = connection.recv(1024) #receiving bytes from client as data
    data = dat.decode('utf-8') #decoding received data from bytes to string
    
    parameter = json.loads(data) #converting received strings (after being converted from bytes) into dictionary
    
    print("Recieved from client:",parameter) #printing data
    
    #calculation part : adding 10 for each voltage
    for i in range(len(parameter['voltage'])):
        parameter['voltage'][i] = parameter['voltage'][i] + 10 
    
    
    
    if not data:
        break #break the loop when there's no data sent

    print("Will be sent to client:",parameter) #printing data
    
    
    serialized_parameter = json.dumps(parameter) #converting dictionary into strings for being transmitted to the client
    
    #transmittal
    connection.send(str.encode(serialized_parameter)) #encoding data from string to bytes
    
connection.close()

