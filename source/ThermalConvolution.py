#-*- coding: utf-8 -*-
"""
Created on Wed Nov 13 15:11:54 2019

@author: Duzi Huang
@email: amduzi@foxmail.com
Convolution Algorithm
"""
from ctypes import *
import numpy as np
import numpy.ctypeslib as npct
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
import time
import gc

class SimROM(object):
#{
#--------------------------------------------------------------------
    def __init__(self):
        pass
#--------------------------------------------------------------------
    def CONV(f1,f2,n1,n2):                                                      #{#f1:initial, f2:single impluse, n1: startT for f2, n2: endT for f2
        f1=100000*f1
        f2=100000*f2
        arrL=len(f1)
        arr1=np.array(f1,dtype=np.int)
        arr2=np.array(f2,dtype=np.int)
        CLIB=npct.load_library("dyncef",".")
        CLIB.CONV.argtypes=[npct.ndpointer(dtype = np.int, ndim = 1, flags="C_CONTIGUOUS"),\
                            npct.ndpointer(dtype = np.int, ndim = 1, flags="C_CONTIGUOUS"),\
                            c_int, c_int,c_int]
        CLIB.CONV(arr1,arr2,n1,n2,arrL)
        res=arr1/100000
        return res  #}

#--------------------------------------------------------------------
    def DRAWplt(f,xmin,xmax):                                                   #{#f: to be plotted, xmin: start x, xmax: end x.
       xx = np.arange(0,len(f))
       plt.plot(xx, f, color='r')
       if xmax != 0:
           plt.xlim(xmin,xmax)
       plt.grid(True)
       plt.show()  #}
#--------------------------------------------------------------------
    def OPENCSV(filepath,mcode,skipline): #{
        x0=np.loadtxt(open(filepath),delimiter=mcode,skiprows=skipline)
        return x0 #}
#--------------------------------------------------------------------
    def REGRCONV(f1,f2,n1,n2):                                                  #{ #regress sytle of SimROM.CONV()
        f1=100000*f1
        f2=100000*f2
        arrL=len(f2)
        arr1=np.array(f1,dtype=np.int)
        arr2=np.array(f2,dtype=np.int)
        CLIB=npct.load_library("dyncef",".")
        CLIB.RECURCONV.argtypes=[npct.ndpointer(dtype = np.int, ndim = 1, flags="C_CONTIGUOUS"),\
                            npct.ndpointer(dtype = np.int, ndim = 1, flags="C_CONTIGUOUS"),\
                            c_int, c_int,c_int]
        CLIB.RECURCONV(arr1,arr2,n1,n2,arrL)
        res=arr1/100000        
        return res      
#--------------------------------------------------------------------
#}

#--------------------------------------------------------------------        

#--------------------------------------------------------------------    
if __name__=="__main__": #{
    sys.setrecursionlimit(1000000)
    x1=SimROM.OPENCSV('1s10a_implus.csv',',',1)                                #10A implus
    x2=SimROM.OPENCSV('1s8a_implus.csv',',',1)                                 #8A implus
    t1=time.time()
#    y1=25+SimROM.CONV(SimROM.CONV(SimROM.OPENCSV('1s10a_implus.csv',',',1) ,\
#                                  SimROM.OPENCSV('1s10a_implus.csv',',',1) ,0,300),\
#                                   SimROM.OPENCSV('1s8a_implus.csv',',',1),300,1200)
    y2=25+SimROM.REGRCONV(SimROM.REGRCONV(SimROM.OPENCSV('1s10a_implus.csv',',',1),\
                          SimROM.OPENCSV('1s10a_implus.csv',',',1),0,300),\
                            SimROM.OPENCSV('1s8a_implus.csv',',',1),300,1200)
    t2=time.time()
#    SimROM.DRAWplt(y1,0,1200)
    SimROM.DRAWplt(y2,0,600)
    print('calculation time:',int(10*(t2-t1))/10,' sec')
#    print(y1[300],"~",y2[300])                                                 #debug point
#    print(y1[600],"~",y2[600])                                                 #debug point
#    print(y1[1200],"~",y2[1200])                                               #debug point
    del y2
    gc.collect()  #}
    

