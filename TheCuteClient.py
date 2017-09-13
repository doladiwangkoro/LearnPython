# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 15:28:15 2017

@author: D M Dolaputra
"""

import socket
import json

parameter = {
        'voltage':[3]}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1',5567))
print('connected to a server')

i = 0
while i < 10:
    print("will be sent to server: ",parameter)
    stringparameter = json.dumps(parameter)
    s.send(str.encode(stringparameter))
    
    data = s.recv(1024)
    data = data.decode('utf-8')
    parameter = json.loads(data)
    print("received from server: ",parameter)
    i = i+1

a = input("say bye to close: ")
if len(a) >= 0:
    s.close()