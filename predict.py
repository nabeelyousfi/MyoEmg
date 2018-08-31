# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 12:26:53 2018

@author: Hassan Yousuf & Nabeel Hussain
"""
from __future__ import print_function
import sklearn.ensemble
from sklearn import metrics
from myo import init, Hub, DeviceListener, StreamEmg
from time import sleep
import numpy as np
import threading
import collections
import math
import _pickle as cPickle
X=[]
ges3 = ["Spread Fingers", "Wave Out", "Wave In", "Fist", "Rest"]

ges = ges3
class Listener(DeviceListener):
    def __init__(self, queue_size=1):
        self.lock = threading.Lock()
        self.emg_data_queue = collections.deque(maxlen=queue_size)
        self.ori_data_queue = collections.deque(maxlen=queue_size)

    def on_connect(self, myo, timestamp, firmware_version):
        myo.set_stream_emg(StreamEmg.enabled)

    def on_emg_data(self, myo, timestamp, emg):
        if(status):
            X.append(np.asarray(emg))

    def on_orientation_data(self, myo, timestamp, quat):
        # print("Orientation:", quat.x, quat.y, quat.z, quat.w)
        with self.lock:
            self.ori_data_queue.append(quat)

    def get_ori_data(self):
        with self.lock:
            return list(self.ori_data_queue)
        
def rms(array):
    n = len(array)
    sum = 0
    for a in array:
        sum =+ a*a
    return np.sqrt((1/float(n))*sum)
     
def iav(array):
    sum = 0
    for a in array:
        sum += np.abs(a)
    return sum

def ssi(array):
    sum = 0
    for a in array:
        sum += a*a
    return sum

def var(array):
    n = len(array)
    sum = 0
    for a in array:
        sum += a*a
    return ((1/float(n-1))*sum)

def tm3(array):
    n = len(array)
    print('n : ', n)
    sum = 0
    for a in array:
        sum =+ a*a*a
    return np.power((1/float(n))*sum,1/float(3))
def wl(array):
    sum = 0
    for a in range(0,len(array)-1):
        sum =+ array[a+1] - array[a]
    return sum

def aac(array):
    n = len(array)
    sum = 0
    for a in range(0,n-1):
        sum =+ array[0+1] - array[0]
    return sum/float(n)

def toEuler(quat):
    quat = quat[0]

    # Roll
    sin = 2.0 * (quat.w * quat.w + quat.y * quat.z)
    cos = +1.0 - 2.0 * (quat.x * quat.x + quat.y * quat.y)
    roll = math.atan2(sin, cos)

    # Pitch
    pitch = math.asin(2 * (quat.w * quat.y - quat.z * quat.x))

    # Yaw
    sin = 2.0 * (quat.w * quat.z + quat.x * quat.y)
    cos = +1.0 - 2.0 * (quat.y * quat.y + quat.z * quat.z)
    yaw = math.atan2(sin, cos)
    return [pitch, roll, yaw]


init()
hub = Hub()
listener = Listener()
hub.run(1000, listener)

status = 9999
# load it again
with open('META001.pkl', 'rb') as fid:
    gnb_loaded1 = cPickle.load(fid)

with open('META002.pkl', 'rb') as fid:
    gnb_loaded2 = cPickle.load(fid)

with open('META003.pkl', 'rb') as fid:
    gnb_loaded3 = cPickle.load(fid)



X = []

#toEuler(listener.get_ori_data())

while(1):
    # myo = feed.get_connected_devices()
    if len(X) > 20:
        x_f_h = []
        X1 = np.asarray(X)
        x_f_h = []
        for b in range(0, 8):
            x_f_h.append(rms(X1[:, b]))
            x_f_h.append(iav(X1[:, b]))
            x_f_h.append(ssi(X1[:, b]))
            x_f_h.append(var(X1[:, b]))
            # x_f_h.append(tm3(X1[:, b]))
            x_f_h.append(wl(X1[:, b]))
            x_f_h.append(aac(X1[:, b]))
        # y_i = model.predict(np.column_stack(np.asarray(x_f_h)), verbose=0)
        # y_i_class = y_i.argmax(axis=-1)
       
        '''
        a_i = 0
        y_i = y_i[0]
        max_var = max(y_i)
        for a in range(len(y_i)):
            if (y_i[a] == max_var):
                a_i = a + 1
        '''''
        p2 = gnb_loaded2.predict([x_f_h])
        p3 = gnb_loaded3.predict([x_f_h])
        if p2 == p3:
            if p2[0] == 1:
                print('Pred --- ', ges[0])
            if p2[0] == 2:
                print('Pred --- ', ges[1])
            if p2[0] == 3:
                print('Pred --- ', ges[2])
            if p2[0] == 4:
                print('Pred --- ', ges[3])
            if p2[0] == 5:
                print('Pred --- ', ges[4])

        X = []

sleep(1)
hub.shutdown()