# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 18:47:24 2017

@author: D M Dolaputra
"""

import socket
import threading
import time

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket()
s3 = socket.socket()

port = [34567, 23456]

    
t1 = threading.Thread(target = s1.connect, args=(('127.0.0.1',34567),))
t2 = threading.Thread(target = s2.connect, args=(('127.0.0.1',23456),))
t3 = threading.Thread(target = s3.connect, args=(('127.0.0.1',12345),))

t1.start()
print("connected to 34567")
t2.start()
print("connected to 23456")
t3.start()
print("connected to 12345")

t1.join()
t2.join()
t3.join()