# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 19:00:56 2017

@author: ddolaputra
"""

import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1',5567))
print('connected to a server')


hello = input("Say hello: ") #client input as strings

#initialized value
parameter = {
        'voltage':[3,4,5],
        'power':[5,6,7]
        }


#the back and forth information transmittal will go on as long as the voltages do not reach 100 
while parameter['voltage'][0] < 100:

    

    serialized_parameter = json.dumps(parameter) #converting dictionary into strings


    #sending part
    s.send(str.encode(serialized_parameter)) #encoding string into bytes and send it to the server
    
    ####The server will do its task in this part###
    
    #receiving data after being processed in the server
    data = s.recv(1024) #receiving data from server
    serialized_parameter = data.decode('utf-8') #decoding received data from bytes to string
    
    
    parameter = json.loads(serialized_parameter) #converting strings into dictionary
    
    print("Receive",parameter) #printing parameter
    
    #calculation part : adding 6 for each voltage
    for i in range(len(parameter['voltage'])):
        parameter['voltage'][i] = parameter['voltage'][i] + 6
    
    print("New",parameter) #printing parameter
    

s.close()
print("client has disconnected")