# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 13:05:28 2017

@author: ddolaputra
"""

#Creating one flexible function for functiontwonodes.py

import os
os.system("cls")

import threading
import time


connection = {
'node1':[0,1,1],
'node2':[1,0,1],
'node3':[1,1,0]} #save for later

""""connection = {
'node1':[0,1],
'node2':[1,0]
}"""

def init(x,y):
    p = {
    'voltage' : [x],
    'power' : [y]
    }
    return p

def setup():
    a = init(5,0)
    b = init(10,0)
    c = init(2,0)
    full = [a,b,c]
    return full
    
# showing data for node n in the kth element
def callthisnode(n):
    this = int(n[4]) - 1 #getting index for allnode
    return allnode[this]
    
  

#sigma calculation for all nodes connected to node n and k is the kth element of the array
def callothernode(n,k):
    othernodesum = {
    'voltage sum':[],
    'power sum':[]}
    vsum = 0
    for i in range(len(connection[n])):
        con = connection[n][i] #check if node n is connected to the other node, con=0 (disconnected) or 1 (connected)
        vsum = vsum + con*allnode[i]['voltage'][k]  #summation of voltage value
    othernodesum['voltage sum'].insert(k+1,vsum)
    return othernodesum
        
        
#n is the node and k is number of iterations
#def function(n,k):

    
#Below is how this program should run chronologically

allnode = setup()

thisnode = callthisnode('node1')
othernode = callothernode('node1',0)
voltagei = thisnode['voltage'][0]
voltageiother = othernode['voltage sum'][0]
newvoltage = voltagei+2*voltageiother
thisnode['voltage'].insert(1,newvoltage)

thisnode2 = callthisnode('node2')
othernode2 = callothernode('node2',0)
voltagei = thisnode2['voltage'][0]
voltageiother = othernode2['voltage sum'][0]
newvoltage = voltagei+2*voltageiother
thisnode2['voltage'].insert(1,newvoltage)

thisnode3 = callthisnode('node3')
othernode3 = callothernode('node3',0)
voltagei = thisnode3['voltage'][0]
voltageiother = othernode3['voltage sum'][0]
newvoltage = voltagei+2*voltageiother
thisnode3['voltage'].insert(1,newvoltage)


thisnode = callthisnode('node1')
othernode = callothernode('node1',1)
voltagei = thisnode['voltage'][1]
voltageiother = othernode['voltage sum'][0]
newvoltage = voltagei+2*voltageiother
thisnode['voltage'].insert(2,newvoltage)

thisnode2 = callthisnode('node2')
othernode2 = callothernode('node2',1)
voltagei = thisnode2['voltage'][1]
voltageiother = othernode2['voltage sum'][0]
newvoltage = voltagei+2*voltageiother
thisnode2['voltage'].insert(2,newvoltage)

thisnode3 = callthisnode('node3')
othernode3 = callothernode('node3',1)
voltagei = thisnode3['voltage'][1]
voltageiother = othernode3['voltage sum'][0]
newvoltage = voltagei+2*voltageiother
thisnode3['voltage'].insert(2,newvoltage)

thisnode = callthisnode('node1')
othernode = callothernode('node1',2)
voltagei = thisnode['voltage'][2]
voltageiother = othernode['voltage sum'][0]
newvoltage = voltagei+2*voltageiother
thisnode['voltage'].insert(3,newvoltage)

thisnode2 = callthisnode('node2')
othernode2 = callothernode('node2',2)
voltagei = thisnode2['voltage'][2]
voltageiother = othernode2['voltage sum'][0]
newvoltage = voltagei+2*voltageiother
thisnode2['voltage'].insert(3,newvoltage)

thisnode3 = callthisnode('node3')
othernode3 = callothernode('node3',2)
voltagei = thisnode3['voltage'][2]
voltageiother = othernode3['voltage sum'][0]
newvoltage = voltagei+2*voltageiother
thisnode3['voltage'].insert(3,newvoltage)

    
"""
t1= threading.Thread(target = function, args = ('node1',5))
t2= threading.Thread(target = function, args = ('node2',5))

t1.start()
t2.start()

t1.join()
t2.join()
"""


#lastelementa = a['voltage'][len(a['voltage'])-1]
#lastelementb = b['voltage'][len(b['voltage'])-1]
    
#print('parameter node a',lastelementa)
#print('parameter node b',lastelementb)
    


