#-*- coding: utf-8 -*-
"""
Created on Wed Nov 13 15:11:54 2019

@author: Duzi Huang
@email: amduzi@foxmail.com
多策略脉冲累加
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import gc

class SimROM(object):
#--------------------------------------------------------------------
    def CONV(f1,f2,n1,n2): #f1:initial, f2:single impluse, n1: startT for f2, n2: endT for f2
        res=f1
        #m1=len(f1)
        m2=len(f2)
        z=[0]
        f2=np.insert(f2,0,values=n1*z,axis=0) #insert 1 row
        for i in range(0,n2-n1):
            f2=np.insert(f2,0,values=z,axis=0)#d = np.insert(a, 0, values=b, axis=1) #insert 1 col
            for j in range(0,m2):
                res[j]=res[j]+f2[j]  
        return res

#--------------------------------------------------------------------
    def DRAWplt(f,xmin,xmax): #f: to be plotted, xmin: start x, xmax: end x.
       xx = np.arange(0,len(f))
       plt.plot(xx, f, color='r')
       if xmax != 0:
           plt.xlim(xmin,xmax)
       plt.grid(True)
       plt.show()  
#--------------------------------------------------------------------

if __name__=="__main__":
    org =np.loadtxt(open("1s10a_implus.csv"),delimiter=",",skiprows=1)
    org2 =np.loadtxt(open("1s8a_implus.csv"),delimiter=",",skiprows=1)
    
    x1=org #10A implus
    x2=org2 #8A implus

        
    y1=25+SimROM.CONV(SimROM.CONV(x1,x1,0,300),x2,300,660)

    SimROM.DRAWplt(y1,0,1200)
    
    del x1,x2,y1
    gc.collect()
    

