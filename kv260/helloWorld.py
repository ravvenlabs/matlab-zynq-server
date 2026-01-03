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

npSocket = NumpySocket()
npSocket.startServer(9999)

print("entering main loop")

# feel free to modify this command structue as you wish.  It might match the 
# command structure that is setup in the Matlab side of things on the host PC.
while(1):
    cmd = npSocket.receiveCmd()
    print("received cmd from Matlab: " + str(cmd))
    npSocket.send(np.array(cmd))
    print("looping back data to Matlab")
    break
    
npSocket.close()