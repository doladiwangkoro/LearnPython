# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 18:17:39 2017

@author: D M Dolaputra
"""

import socket

s = socket.socket()
s.bind(('',8000))
s.listen(5)

conn, address = s.accept()
