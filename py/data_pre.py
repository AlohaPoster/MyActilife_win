#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 18:02:55 2020

@author: test
"""


window_size = 5.12

import pandas as pd
from scipy import signal,interpolate
import numpy as np

def getdata(filepath,filename):
    dfacc = pd.read_csv(filepath + filename + ".csv")
    #print(dfacc.columns)
    abs_time = list(dfacc["abs_time"])
    time = list(dfacc['rel_time'])
    acc_x = list(dfacc['x_acc'])
    acc_y = list(dfacc['y_acc'])
    acc_z = list(dfacc['z_acc'])
    # abs_time = [n for n in abs_time if n!="abs_time"]
    # time = [n for n in time if n!="rel_time"]
    # acc_x = [n for n in acc_x if n!="x_acc"]
    # acc_y = [n for n in acc_y if n!="y_acc"]
    # acc_z = [n for n in acc_z if n!="z_acc"]
    #窗口采样
    length = int(window_size*50)
    window_num = int(len(acc_x)/length)
    end = int(window_num*length)
    abs_time = abs_time[:end]
    time = time[:end]
    abs_time = abs_time[0:end:length]
    time = time[0:end:length]
    accx = np.array(acc_x[:end]).reshape(window_num,length).astype('float32')
    accy = np.array(acc_y[:end]).reshape(window_num,length).astype('float32')
    accz = np.array(acc_z[:end]).reshape(window_num,length).astype('float32')

    ab_time = []
    time = [round(l,2) for l in time]
    for l in abs_time:
        if l.find('.')!=-1:
            l = l[0:l.find('.')]
            ab_time.append(l)
        else:
            ab_time.append(l)

            
    x = np.hstack((accx,np.hstack((accy,accz))))
    x = x.reshape(window_num,length,3)

    return x, ab_time, time



if __name__ == "__main__":

    x,t,tt= getdata("/Users/zhangruilin/Desktop/","ceshi1")
    print(tt)
    print(t)