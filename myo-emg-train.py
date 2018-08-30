# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 13:39:13 2018

@author: Hassan
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
import csv


# Complete code for training and predicting EMG data in Python using RandomForestClassifier via Myo Armband 2

def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]

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


def featurize(array):
    n = []
    for a in array:
        n.append(rms(a))
    return n

status = 0

X = []

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


init()
hub = Hub()
listener = Listener()
hub.run(1000, listener)

status = 9999

sleep(1)

myX = []

req_iter = 20
train_1 = []
train_2 = []
train_3 = []
train_4 = []
train_5 = []

ges1 = ['Rock', 'Paper', 'Scissors', 'Lizard', 'Spock']
ges2 = ['Number 1', 'Number 2', 'Number 3', 'Number 4', 'Number 5']
ges3 = ["Spread Fingers", "Wave Out", "Wave In", "Fist", "Rest"]

ges = ges3


for a in range(1,4):

    print("\nGesture -- ", ges[0]," : Ready?")
    input("Press Enter to continue...")
    X = []
    while(1):
        if len(X) > 20:
            # print(X[-1])
            train_1.append(np.asarray(X))
            X = []
            if len(train_1) > a*req_iter:
                break
            myFile = open('dataemg.csv', 'a')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(train_1)

    print("\nGesture -- ", ges[1]," : Ready?")
    input("Press Enter to continue...")
    X = []
    while(1):
        if len(X) > 20:
            # print(X[-1])
            train_2.append(np.asarray(X))
            X = []
            if len(train_2) > a*req_iter:
                break
            myFile = open('dataemg.csv', 'a')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(train_2)

    print("\nGesture -- ", ges[2]," : Ready?")
    input("Press Enter to continue...")
    X = []
    while(1):
        if len(X) > 20:
            # print(X[-1])
            train_3.append(np.asarray(X))
            X = []
            if len(train_3) > a*req_iter:
                break
            myFile = open('dataemg.csv', 'a')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(train_3)

    print("\nGesture -- ", ges[3]," : Ready?")
    input("Press Enter to continue...")
    X = []
    while(1):
        if len(X) > 20:
            # print(X[-1])
            train_4.append(np.asarray(X))
            X = []
            if len(train_4) > a*req_iter:
                break
            myFile = open('dataemg.csv', 'a')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(train_4)


    print("\nGesture -- ", ges[4]," : Ready?")
    input("Press Enter to continue...")
    X = []
    while(1):
        if len(X) > 20:
            # print(X[-1])
            train_5.append(np.asarray(X))
            X = []
            if len(train_5) > a*req_iter:
                break
            myFile = open('dataemg.csv', 'a')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(train_5)

sleep(1)
hub.shutdown()