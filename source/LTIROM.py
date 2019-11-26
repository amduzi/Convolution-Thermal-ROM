# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 08:45:06 2019

@author: Duzi Huang
@email: amduzi@foxmail.com
"""

from ThermalConvolution import SimROM as TConv
import configparser as cpr
import numpy as np

#--------------------------------------------------------------------
class LTIROM(object): #{
    def GETSM(fname):
        config = cpr.ConfigParser()
        config.read(fname)
        s=config.items('source')
        m=config.items('monitor')
        fx=config.items('factor')
        return s,m,fx
#--------------------------------------------------------------------
    def LTICORE(Pfactor,ConvMatrix,ScrNum,MonNum,Ssec,Esec,Ambient,Bias):
        X0=ConvMatrix
        romResult=np.zeros((ScrNum*MonNum,len(X0)))
        monT=np.zeros((MonNum,len(X0))) 
        StResult=np.zeros(MonNum)
    
        for i in range(0,MonNum):
            pass
            for k in range (0,ScrNum):
                romResult[i*ScrNum+k]=X0[:,i*ScrNum+k+1]
                Y = Pfactor[k] * TConv.CONV(romResult[i*ScrNum+k],romResult[i*ScrNum+k],Ssec,Esec)
                monT[i] += Bias*Y   
            StResult[i]=monT[i][Esec] + Ambient
            
        return StResult
#--------------------------------------------------------------------
    
#}
#--------------------------------------------------------------------
if __name__=="__main__": #{
    X0=TConv.OPENCSV('Implus_Conv.csv',',',1)
    x,y,z=LTIROM.GETSM('config.ini')
    pv=np.zeros(len(z))
    res=np.zeros(len(z))
        
    for i in range(0,len(z)):
        pv[i]=z[i][1]
    
    res=LTIROM.LTICORE(pv,X0,len(x),len(y),0,3600,25,0.92)
    
    print('Reduce Order Model for SmartPhone--by Duzi Huang')
    print('------------------------------------------------')
    for i in range(0,len(z)):
        print(z[i][0],'\t',z[i][1],' W :',int(100*res[i])/100)
        print('------------------------------------------------')            
#}