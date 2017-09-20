# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 11:52:03 2017

@author: D M Dolaputra
"""

import os
os.system("cls")

import threading
import time

""" Initialization """

#adjacency matrix or how the nodes are connected
connection = {
'node1':[0,1,1],
'node2':[1,0,1],
'node3':[1,1,0]}

def init(x,y,z):
    p = {
    'lambda' : [x],
    'power' : [y],
    'voltage': [z]
    }
    return p

def setupnode():
    a = init(0,0,0)
    b = init(0,0,0)
    c = init(0,0,0)
    full = [a,b,c]
    return full

allnode = setupnode()

#getting a dictionary of connection from n (as a node) to all the nodes available
def defineconnection(n):
    myu = {}
    for i in range(len(connection[n])):
        con = connection[n][i] #check if node n is connected to the other node, con=0 (disconnected) or 1 (connected)
        myu['myu'+n[4]+str(i+1)] = [0]
    return myu

#getting a set of dictionary for all myus
def setupconnection():
    allmyu = []
    for i in range(len(connection['node1'])):
        allmyu.insert(i,defineconnection('node'+str(i+1)))
    return allmyu

allconnection = setupconnection()

""" Functions Preparation """

# showing data for node n in the kth element
def callthisnode(n):
    thisnode = int(n[4]) - 1 #getting index for allnode
    return allnode[thisnode]

#getting array of the connection from n (as a node) to node i+1
def callthisconnection(n,i):
    return allconnection[int(n[4])-1]['myu'+n[4]+str(i+1)]

def callothernode(n):
    




""" Updating each parameter """

