# Dr. Kaputa
# Matlab Server
from numpysocket import NumpySocket
import os
import cv2
import numpy as np
import time
import mmap
import struct
import sys, random
import ctypes
import copy
from frameGrabber import ImageProcessing
from frameGrabber import ImageFeedthrough
from frameGrabber import ImageWriter

width = 752
height = 480
depth = 1

camProcessed = ImageProcessing(width,height,depth)
camFeedthrough = ImageFeedthrough(width,height,depth)
camWriter = ImageWriter(width,height,depth)

npSocket = NumpySocket()
npSocket.startServer(9999)

# only set this flag to true if you have generated your bit file with a 
# Vivado reference design for Simulink
simulink = True    
if simulink == True:
    f1 = open("/dev/mem", "r+b")
    simulinkMem = mmap.mmap(f1.fileno(), 1000, offset=0xa0060000)
    mv = memoryview(simulinkMem).cast('Q') 
    mv[0] = 0x0000000000000001
    mv[1] = 0x000001e0000002f0
    mv[0] = 0x0000000100000000
    
    # simulinkMem.seek(0) 
    # simulinkMem.write(struct.pack('l', 1))       # reset IP core
    # simulinkMem.seek(8)                         
    # simulinkMem.write(struct.pack('l', 752))     # image width
    # simulinkMem.seek(12)                        
    # simulinkMem.write(struct.pack('l', 480))     # image height
    # simulinkMem.seek(16)                        
    # simulinkMem.write(struct.pack('l', 94))       #  horizontal porch
    # simulinkMem.seek(20)                        
    # simulinkMem.write(struct.pack('l', 1000))     #  vertical porch when reading from debug
    # simulinkMem.seek(4) 
    # simulinkMem.write(struct.pack('l', 1))       # enable IP core

print("entering main loop")

# feel free to modify this command structue as you wish.  It might match the 
# command structure that is setup in the Matlab side of things on the host PC.
while(1):
    cmd = npSocket.receiveCmd()
    if cmd == b'0':
        data = npSocket.receive(width,height,depth)
        camWriter.setFrame(data)
        npSocket.send(np.array(2))
    elif cmd == b'1':
        frame = camFeedthrough.getMonoGray()
        npSocket.send(frame)
    elif cmd == b'2':
        frame = camProcessed.getMonoGray()
        npSocket.send(frame) 
    else:
        break
npSocket.close()