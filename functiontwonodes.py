# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 10:25:10 2017

@author: ddolaputra
"""

import os
os.system("cls")

import threading
import time

def init1(x,y):
    p = {
    'voltage' : [x],
    'power' : [y]
    }
    return p

def init2(x,y):
    p = {
    'voltage' : [x],
    'power' : [y]
    }
    return p
    

def function1(list1):
    for i in range(5):
        time.sleep(0.5)
        voltagei = list1['voltage'][i]
        poweri = list1['power'][i]
    
        newvoltage = voltagei+2*b['voltage'][i]
        newpower = poweri+current*b['power'][i]
    
        list1['voltage'].insert(i+1,newvoltage)
        list1['power'].insert(i+1,newpower)
        #print(list1)
    return list1

def function2(list1):
    for i in range(5):
        time.sleep(0.5)

        voltagei = list1['voltage'][i]
        poweri = list1['power'][i]
    
        newvoltage = voltagei+2*a['voltage'][i]
        newpower = poweri+current*a['power'][i]
    
        list1['voltage'].insert(i+1,newvoltage)
        list1['power'].insert(i+1,newpower)
        #print(list1)
    return list1
    
current = 3
a = init1(1,2)
b = init2(10,3)

#i = 0
#while i < 5:
"""for i in range(4):
    function1(a)
    function2(b)"""
    #i = i+1

t1= threading.Thread(target = function1, args = (a,))
t2= threading.Thread(target = function2, args = (b,))

t1.start()
t2.start()

t1.join()
t2.join()

lastelementa = a['voltage'][len(a['voltage'])-1]
lastelementb = b['voltage'][len(b['voltage'])-1]
    
print('parameter node a',lastelementa)
print('parameter node b',lastelementb)