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


#setup for initial voltage and power (later to be initial parameters)
def init(x,y):
    p = {
    'voltage' : [x],
    'power' : [y]
    }
    return p

#setup for the three nodes
#This are variables that we can set, however, usually this value are all zeros for our optimization case
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
  

#sigma calculation for all nodes connected to node n and k is the (k+1)th update since k starts from zero
def callothernode(n,k):
    othernodesum = {
    'voltage sum':[],
    'power sum':[]} #dictionary preparation
    vsum = 0 #initial value for the voltage
    for i in range(len(connection[n])):
        con = connection[n][i] #check if node n is connected to the other node, con=0 (disconnected) or 1 (connected)
        vsum = vsum + con*allnode[i]['voltage'][k]  #summation of voltage value
    othernodesum['voltage sum'].insert(k+1,vsum) #the value will be stored in the dictionary
    return othernodesum
        
        
#n is the node and k is number of iterations
def function(n,k):
    for i in range(k):
        time.sleep(0.1) #delay so the function can run simultaneously without any conflicting updates
        thisnode = callthisnode(n) #the nodes that we want to examine
        #print(thisnode) #prove of value (will be commented next time) 
        othernode = callothernode(n,i) #calling other node for summation calculation
        #print(othernode) #prove of value (will be commented next time) 
        voltagei = thisnode['voltage'][i] #value setting of the node n
        #print(voltagei) 
        voltageiother = othernode['voltage sum'][0] #summation of other's node voltage connected to the node n
        #print(voltageiother)
        newvoltage = voltagei+2*voltageiother #voltage calculation
        #print(newvoltage)
        thisnode['voltage'].insert(i+1,newvoltage) #updating voltage value 
        #print(thisnode)
    
    
#Below is how this program should run chronologically

def main(n,k):

    t1= threading.Thread(target = function, args = ('node1',k))
    t2= threading.Thread(target = function, args = ('node2',k))
    t3= threading.Thread(target = function, args = ('node3',k))
    
    t1.start()
    t2.start()
    t3.start()
    
    t1.join()
    t2.join()
    t3.join()
    
    print (allnode[int(n[4]) - 1]['voltage'])
    
#adjacency matrix or how the nodes are connected
connection = {
'node1':[0,1,1],
'node2':[1,0,1],
'node3':[1,1,0]} 

allnode = setup()
main('node2',3)








"""

Running Draft

_______________ooooo__________________

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


