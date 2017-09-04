# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 16:57:05 2017

@author: D M Dolaputra
"""

#adjacency matrix or how the nodes are connected
connection = {
'node1':[0,1,1],
'node2':[1,0,1],
'node3':[1,1,0]} 

#getting a dictionary of connection from n (as a node) to all the nodes available
def defineconnection(n):
    myu = {}
    for i in range(len(connection[n])):
        con = connection[n][i] #check if node n is connected to the other node, con=0 (disconnected) or 1 (connected)
        myu['myu'+n[4]+str(i+1)] = [0]
    return myu

#getting array of the connection from n (as a node) to node i+1
def callthisconnection(n,i):
    thisconnection = defineconnection(n)
    print (thisconnection['myu'+n[4]+str(i+1)])
    
    