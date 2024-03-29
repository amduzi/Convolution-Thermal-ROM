# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 08:45:06 2019

@author: Duzi Huang
@email: amduzi@foxmail.com
LTI ROM with thermal control sample
"""

from ThermalConvolution import SimROM as TConv
import configparser as cpr
import ctypes
import numpy as np
import pandas as pd
import sys
import time
import gc


#--------------------------------------------------------------------
class LTIROM(object): 
#{
#--------------------------------------------------------------------
    def __init__(self):
        pass
#--------------------------------------------------------------------
    def DYNEFF(dt2):
        CLIB=ctypes.cdll.LoadLibrary("./dyncef.dll")
        CLIB.TDCEF.argtypes=(ctypes.c_float,)
        CLIB.TDCEF.restype=ctypes.c_float
        err=CLIB.TDCEF(dt2)
        return int(10000*err+0.5)/10000
#--------------------------------------------------------------------
    def EFF(dt1):
        CLIB=ctypes.cdll.LoadLibrary("./dyncef.dll")                              #chip efficiency
        CLIB.PCEF.argtypes=(ctypes.c_float,)
        CLIB.PCEF.restype=ctypes.c_float
        err=CLIB.PCEF(dt1)
        return int(10000*err+0.5)/10000
#--------------------------------------------------------------------
    def GETCOL(n):
        F=TConv.OPENCSV('implus_Conv.csv',',',1)
        Fn=F[:,n]
        return Fn 
#--------------------------------------------------------------------
    def GETCOL_N(n,t):
        F=TConv.OPENCSV('LTImatrix.csv',',',1)
        Fn=F[:,n]
        return Fn[t]    
#--------------------------------------------------------------------
    def GETSM(fname):
        config = cpr.ConfigParser()
        config.read(fname)
        s=config.items('source')
        m=config.items('monitor')
        fx=config.items('factor')
        fx1=config.items('factor1')
        return s,m,fx,fx1
#--------------------------------------------------------------------
    def LTICORE(Pfactor,ConvMatrix,ScrNum,MonNum,Ssec,Esec,Ambient,Bias):
        X0=ConvMatrix
        df=LTIROM.GETCOL(0)                                                    #for data saving_______
        #romResult=np.zeros((ScrNum*MonNum,len(X0)))                            #backup for GETCOL
        monT=np.zeros((MonNum,len(X0))) 
        StResult=np.zeros(MonNum)
        dt=0
    
        for i in range(0,MonNum):#{
            pass
            for k in range (0,ScrNum):#{
                #romResult[i*ScrNum+k]=X0[:,i*ScrNum+k+1]                       #backup for GETCOL
#                Y=Pfactor[k]*LTIROM.GETCOL_N(i*ScrNum+k+1,Esec)                 #use LTI matrix
                Y = Pfactor[k] * TConv.CONV(LTIROM.GETCOL(i*ScrNum+k+1),\
                           LTIROM.GETCOL(i*ScrNum+k+1),Ssec,Esec)              #convolve method
#                Y = TConv.CONV(Pfactor[k] * TConv.CONV(LTIROM.GETCOL(i*ScrNum+k+1),LTIROM.GETCOL(i*ScrNum+k+1),\
#                           0,1800),LTIROM.GETCOL(i*ScrNum+k+1),1800,3600)      #for multi_power_policy
                monT[i] += Y#Bias*Y #} #very carefull about this ......if using multi phase.
        for i in range(0,MonNum):#{
            dt += monT[i][Esec]#}
        Bias=LTIROM.DYNEFF(dt/MonNum)
        print(Bias)                                                            #debug point
        for i in range(0,MonNum):#{
            StResult[i]=monT[i][Esec]*Bias + Ambient #} 

#===========code for XXXX, to using these codes,you need:
#uncomment l62,comment l72, change l77 Bias, and uncomment l73-74, l87-96
        for i in range(0,len(X0)):#{
            dt=0
            for k in range(0,MonNum):#{
                dt += monT[k][i] #}
            for j in range(0,MonNum):#{    
                monT[j][i]=monT[j][i]*LTIROM.DYNEFF(dt/MonNum) #}#}
        for i in range(0,MonNum):#{
            df=np.column_stack((df,monT[i]))#}                                 #for data saving_______
        df=pd.DataFrame(df)                                                    #for data saving_______
        df.to_csv('./TransRes.csv',encoding='utf_8', header=False,index=False) #for data saving_______ 
#===========        
#        TConv.DRAWplt(monT[0],0,3600)                                          #debug point for multi_power
        return StResult
#--------------------------------------------------------------------
    def LTICORE_Tcon(Pfactor,P1factor,ConvMatrix,ScrNum,MonNum,Ssec,Esec,Ambient,Bias,TH,TL,step):
        X0=ConvMatrix
        monT=np.zeros((MonNum,len(X0))) 
        StResult=np.zeros(MonNum)
        Y=np.zeros((ScrNum,len(X0)))
        Z=np.zeros((ScrNum,len(X0)))
        A=[]
        i=0
        t=Ssec
    

        for k in range (0,ScrNum):#{
#            Y[k] = P1factor[k] * TConv.CONV(LTIROM.GETCOL(i*ScrNum+k+1),LTIROM.GETCOL(i*ScrNum+k+1),t,t+step)
            Y[k] = LTIROM.GETCOL(i*ScrNum+k+1)
            Z[k]=Y[k]#}
        
        StResult[i]=Ambient

        k=0
        sign=0
#        t += step
#        if t>= Esec:
#            return StResult
        
        while t< Esec:#{
            if StResult[i]>TH:
                A.append(StResult[i])                                           #debug point
                for k in range (0,ScrNum):#{
                    Y[k] = TConv.REGRCONV(Y[k],Pfactor[k]*Z[k],t,t+step)
                    monT[i] += Bias*Y[k] #}  
                StResult[i]=monT[i][t+step] + Ambient
                k=0
                t+=step
                sign=1
                monT[i]=0#}
#                pass
            if StResult[i]<TL:
                A.append(StResult[i])                                           #debug point
                for k in range (0,ScrNum):#{
                    Y[k] = TConv.REGRCONV(Y[k],P1factor[k]*Z[k],t,t+step)
                    monT[i] += Bias*Y[k] #}  
                StResult[i]=monT[i][t+step] + Ambient
                k=0
                t+=step
                sign=0
                monT[i]=0#}                
#                pass
            if (StResult[i]<=TH) and (StResult[i]>=TL):
                A.append(StResult[i])                                           #debug point
                if sign==1:
                    for k in range (0,ScrNum):#{
                        Y[k] = TConv.REGRCONV(Y[k],Pfactor[k]*Z[k],t,t+step)
                        monT[i] += Bias*Y[k] #}  
                    StResult[i]=monT[i][t+step] + Ambient
                    k=0
                    t+=step
                    monT[i]=0                    
                if sign==0:
                    for k in range (0,ScrNum):#{
                        Y[k] = TConv.REGRCONV(Y[k],P1factor[k]*Z[k],t,t+step)
                        monT[i] += Bias*Y[k] #}  
                    StResult[i]=monT[i][t+step] + Ambient
                    k=0
                    t+=step
                    monT[i]=0                     
            #}
        
        for k in range (0,ScrNum):
            monT[i] += Bias*Y[k]
        monT[i] += Ambient
        
#        print(monT[i][100])                                                    #debug point
        TConv.DRAWplt(monT[i],Ssec,Esec)                                        #debug point for full monitor plot        
#        TConv.DRAWplt(A,0,len(A))                                               #debug point for temperature-action plot
        return StResult
#}
#--------------------------------------------------------------------
if __name__=="__main__": #{
    sys.setrecursionlimit(1000000)
    X0=TConv.OPENCSV('Implus_Conv.csv',',',1)
    x,y,z,z1=LTIROM.GETSM('config.ini')
    pv=np.zeros(len(z))
    pv1=np.zeros(len(z1))
    res=np.zeros(len(y))
    AP=0
    AP1=0
    
   
    for i in range(0,len(z)):                                                   #get p
        pv[i]=z[i][1]
        pv1[i]=z1[i][1]
        
    for i in range(0,len(z1)):
        AP1 += pv1[i]
    AP1=LTIROM.EFF(AP1)
    print(AP1)                                                     #debug point
        
    t1=time.time()
#======Tcontrol to use this: comment l198-207, uncomment l194
    res=LTIROM.LTICORE_Tcon(pv,pv1,X0,len(x),len(y),0,3600,25,AP1,36,34,10)    #thermal control policy demo

#======LTI transient/steady calcation: uncomment l204-213, comment l200
#--------------------------------------------------------------------           #normal calc & result demo 
#    res=LTIROM.LTICORE(pv1,X0,len(x),len(y),0,3600,25,AP1)
#    print('\n')
#    print('Reduce Order Model for SmartPhone--by Duzi Huang')
#    print('================================================')
#    for i in range(0,len(z)):
#        print('\t',z1[i][0],'    \t',':', z1[i][1], ' W')
#    print('================================================')
#    for i in range(0,len(y)):
#        print('\t',y[i][1],'    \t',':',int(100*res[i])/100," 'C")
#        print('------------------------------------------------')
#--------------------------------------------------------------------
    t2=time.time()
    print('calculation time:',int(10*(t2-t1))/10,' sec')
    gc.collect()
#}