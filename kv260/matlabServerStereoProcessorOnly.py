# Dr. Kaputa
# Matlab Zynq Server Demo

from numpysocket import NumpySocket
import cv2
import numpy as np
import time
import mmap
import struct
import sys, random
import ctypes
import copy

#width = 752
#height = 480
#depth = 8

width = 1080
height = 720
depth = 8

npSocket = NumpySocket()
npSocket.startServer(9999)

print("entering main loop")

# feel free to modify this command structue as you wish.  It might match the 
# command structure that is setup in the Matlab side of things on the host PC.
while(1):
    cmd = npSocket.receiveCmd()
    if cmd == b'0':
        data = npSocket.receive(width,height,depth)
        #print("received frame from matlab")
        stereoImage = np.reshape(data,(height,width,depth))
        #print("converted image")
    elif cmd == b'2':
        #print("sending processed frames to matlab")
        leftGray = stereoImage[:,:,3]
        leftGray = np.ascontiguousarray(leftGray, dtype=np.uint8) 
        rightGray = stereoImage[:,:,7]
        rightGray = np.ascontiguousarray(rightGray, dtype=np.uint8) 
        
        # perform image processing to find edges
        leftEdge = cv2.Sobel(leftGray, cv2.CV_8U, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
        rightEdge = cv2.Sobel(rightGray, cv2.CV_8U, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
        
        # send back processed images
        npSocket.send(leftEdge)
        npSocket.send(rightEdge)
    else:
        break
        
npSocket.close()