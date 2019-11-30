#-*- coding: utf-8 -*-
"""
Created on Wed Nov 13 15:11:54 2019

@author: Duzi Huang
@email: amduzi@foxmail.com
Convolution Algorithm
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import gc

class SimROM(object):
#{
#--------------------------------------------------------------------
    def CONV(f1,f2,n1,n2):                                                      #{#f1:initial, f2:single impluse, n1: startT for f2, n2: endT for f2
        res=f1
        #m1=len(f1)
        m2=len(f2)
        z=[0]
        f2=np.insert(f2,0,values=n1*z,axis=0)                                   #insert 1 row
        for i in range(0,n2-n1):
            f2=np.insert(f2,0,values=z,axis=0)                                  #d = np.insert(a, 0, values=b, axis=1) #insert 1 col
            for j in range(0,m2):
                res[j]=res[j]+f2[j]  
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
#        f1=1*f1/1
#        f2=1*f2/1
        if n1<n2:    
            for i in range(n1,len(f1)-1):
                f1[i+1] += f2[i-n1]
            n1 += 1
#            print(n1,n2)                                                       #debug point
#            print(f1)                                                          #debug point
            SimROM.REGRCONV(f1,f2,n1,n2)
        else:
#            SimROM.DRAWplt(f1,0,1200)                                          #debug point
            return f1
        return f1      
#--------------------------------------------------------------------
#}

#--------------------------------------------------------------------        

#--------------------------------------------------------------------    
if __name__=="__main__": #{

#    x1=SimROM.OPENCSV('1s10a_implus.csv',',',1)                                #10A implus
#    x2=SimROM.OPENCSV('1s8a_implus.csv',',',1)                                 #8A implus
  
#    y1=25+SimROM.CONV(SimROM.CONV(SimROM.OPENCSV('1s10a_implus.csv',',',1) ,\
#                                  SimROM.OPENCSV('1s10a_implus.csv',',',1) ,0,300),\
#    SimROM.OPENCSV('1s8a_implus.csv',',',1),300,1200)
    y2=25+SimROM.REGRCONV(SimROM.REGRCONV(SimROM.OPENCSV('1s10a_implus.csv',',',1),\
                          SimROM.OPENCSV('1s10a_implus.csv',',',1),0,300),\
    SimROM.OPENCSV('1s8a_implus.csv',',',1),300,1200)
    
#    SimROM.DRAWplt(y1,0,1200)
    SimROM.DRAWplt(y2,0,500)
#    print(y1[300],"~",y2[300])                                                 #debug point
#    print(y1[600],"~",y2[600])                                                 #debug point
#    print(y1[1200],"~",y2[1200])                                               #debug point
    del y2
    gc.collect()  #}
    

