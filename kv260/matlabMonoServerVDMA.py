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