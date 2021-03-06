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
        myu['myu'+n[4]+str(i+1)] = [(2+i)*3]
    return myu

#getting a set of dictionary for all myus
def setupconnection():
    allmyu = []
    for i in range(len(connection['node1'])):
        allmyu.insert(i,defineconnection('node'+str(i+1)))
    return allmyu

allconnection = setupconnection()

#getting array of the connection from n (as a node) to node i+1
def callthisconnection(n,i):
    thisconnection = defineconnection(n)
    print (thisconnection['myu'+n[4]+str(i+1)])
    
#geting the sum of all myu n-others
def sumthisconnection(n):
    thisconnection = defineconnection(n)
    summyu = 0
    for i in range(len(connection[n])):
        con = connection[n][i]
        summyu = summyu + con*thisconnection['myu'+n[4]+str(i+1)][0]
    print (summyu)

#getting array of the connection from node i+1 to n
def callotherconnection(n):
    for i in range(len(connection[n])):
        if i != int(n[4])-1:
            othermyu = defineconnection(n[:4]+str(i+1))
            print (othermyu)
    return othermyu
    
    
#getting the sum of all myu others-n

    
    