# Dr. Kaputa
# Matlab Server
from numpysocket import NumpySocket
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

camProcessed = ImageProcessing()
camFeedthrough = ImageFeedthrough()
camWriter = ImageWriter()

npSocket = NumpySocket()
npSocket.startServer(9999)

# only set this flag to true if you have generated your bit file with a 
# Vivado reference design for Simulink
simulink = False
if simulink == True:
    f1 = open("/dev/mem", "r+b")
    simulinkMem = mmap.mmap(f1.fileno(), 1000, offset=0x43c60000)
    simulinkMem.seek(0) 
    simulinkMem.write(struct.pack('l', 1))       # reset IP core
    simulinkMem.seek(8)                         
    simulinkMem.write(struct.pack('l', 752))     # image width
    simulinkMem.seek(12)                        
    simulinkMem.write(struct.pack('l', 480))     # image height
    simulinkMem.seek(16)                        
    simulinkMem.write(struct.pack('l', 94))       #  horizontal porch
    simulinkMem.seek(20)                        
    simulinkMem.write(struct.pack('l', 1000))     #  vertical porch when reading from debug
    simulinkMem.seek(4) 
    simulinkMem.write(struct.pack('l', 1))       # enable IP core

print "entering main loop"

# feel free to modify this command structue as you wish.  It might match the 
# command structure that is setup in the Matlab side of things on the host PC.
while(1):
    cmd = npSocket.receiveCmd()
    #print(cmd)
    if cmd == '0':
        print "received frame from matlab"
        data = npSocket.receive()
        reshaped = np.reshape(data,(480, 752,8))
        print "writing frame to FPGA"
        camWriter.setFrame(reshaped)
    elif cmd == '1':
        print "sending feedthrough frame to matlab"
        frameLeft,frameRight = camFeedthrough.getStereoGray()
        tempImageLeft = np.ascontiguousarray(frameLeft, dtype=np.uint8) 
        tempImageRight = np.ascontiguousarray(frameRight, dtype=np.uint8) 
        npSocket.send(tempImageLeft)
    elif cmd == '2':
        print "sending processed frames to matlab"
        time.sleep(1)
        frameLeft,frameRight = camProcessed.getStereoGrayFrame()
        frameLeft,frameRight = camProcessed.getStereoGrayFrame()
        frameLeft,frameRight = camProcessed.getStereoGrayFrame()
        #frameLeft,frameRight = camProcessed.getStereoGray()
        tempImageLeft = np.ascontiguousarray(frameLeft, dtype=np.uint8) 
        tempImageRight = np.ascontiguousarray(frameRight, dtype=np.uint8) 
        npSocket.send(tempImageLeft)
        npSocket.send(tempImageRight) 
    elif cmd == '3':
        #print "sending raw frames to matlab"
        frameLeft,frameRight = camFeedthrough.getStereoGray()
        tempImageLeft = np.ascontiguousarray(frameLeft, dtype=np.uint8) 
        tempImageRight = np.ascontiguousarray(frameRight, dtype=np.uint8) 
        npSocket.send(tempImageLeft)
        npSocket.send(tempImageRight) 
    elif cmd == '4':
        print "sending processed frames to matlab from camera"
        camProcessed.setSource(0)
        time.sleep(.5)
        frameLeft,frameRight = camProcessed.getStereoGray()
        tempImageLeft = np.ascontiguousarray(frameLeft, dtype=np.uint8) 
        tempImageRight = np.ascontiguousarray(frameRight, dtype=np.uint8) 
        npSocket.send(tempImageLeft)
        npSocket.send(tempImageRight) 
    elif cmd == '5':  
        t_lower = float(npSocket.receiveParam())
        print(t_lower)
        t_upper = float(npSocket.receiveParam())
        print(t_upper)
        frameLeft,frameRight = camFeedthrough.getStereoGray()
        tempImageLeft = np.ascontiguousarray(frameLeft, dtype=np.uint8) 
        tempImageRight = np.ascontiguousarray(frameRight, dtype=np.uint8) 
        edge = cv2.Canny(tempImageLeft, t_lower, t_upper) 
        #print(edge.dtype)
        npSocket.send(edge)
        npSocket.send(tempImageRight) 
    elif cmd == '6':  
        print "reading image from camera"
        t_lower = float(npSocket.receiveParam())
        #print(t_lower)
        t_upper = float(npSocket.receiveParam())
        #print(t_upper)
        frameLeft,frameRight = camProcessed.getStereoGrayFrame()
        tempImageLeft = np.ascontiguousarray(frameLeft, dtype=np.uint8) 
        tempImageRight = np.ascontiguousarray(frameRight, dtype=np.uint8) 
        #edge = cv2.Canny(tempImageLeft, t_lower, t_upper) 
        #print(edge.dtype)
        npSocket.send(tempImageLeft)
        npSocket.send(tempImageRight) 
    else:
        break
npSocket.close()