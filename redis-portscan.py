#!/usr/bin/python
# Thu Feb 13 16:55:32 UTC 2014 <aramosf @ unsec.net>
#
# Scan a host using redis server.
# Using MIGRATE response:
# MIGRATE 127.0.0.1 21 a 1 1
#-IOERR error or timeout writing to target instance
#MIGRATE 127.0.0.1 22 a 1 1
#-IOERR error or timeout reading from target node

import socket
import sys
import string

if len(sys.argv) < 4:
 print sys.argv[0] + " [redis IP] [redis PORT] [IP to scan]"
 sys.exit()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed'
    sys.exit()

host = sys.argv[1];
port = int(sys.argv[2]);
toscan = sys.argv[3];
readbuffer=""
s.connect((host, port))
message = "set a1 1\r\n"

try :
    s.sendall(message)
except socket.error:
    print 'Failed'
    sys.exit()
reply = s.recv(50)
for p in range(1, 82):
 message = "MIGRATE " + toscan + " " + str(p) + " a1 1 1\r\n"; 
 #print message
 try :
    s.sendall(message)
 except socket.error:
    print 'Failed'
    sys.exit()
 readbuffer=readbuffer+s.recv(1024)
 temp=string.split(readbuffer, "\n")
 readbuffer=temp.pop( )
 for line in temp:
     line=string.rstrip(line)
 #print line
 if not "writing" in line: 
   print str(p) + " open"
   if  "OK" in line: 
    message = "set a1 1\r\n"
    #print message
    s.sendall(message)
    reply=s.recv(10)
s.close()
