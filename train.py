# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 13:39:13 2018

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
import _pickle as cPickle

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
ges = ["Spread Fingers", "Wave Out", "Wave In", "Fist", "Rest"]

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

train_x = []
train_y = []

for a in train_1:
    train_x.append(np.asarray(a))
    train_y.append(1)

for a in train_2:
    train_x.append(np.asarray(a))
    train_y.append(2)

for a in train_3:
    train_x.append(np.asarray(a))
    train_y.append(3)

for a in train_4:
    train_x.append(np.asarray(a))
    train_y.append(4)

for a in train_5:
    train_x.append(np.asarray(a))
    train_y.append(5)

train_x_f = []

for a in train_x:
    x_f_h = []
    for b in range(0,8):
        x_f_h.append(rms(a[:, b]))
        x_f_h.append(iav(a[:, b]))
        x_f_h.append(ssi(a[:, b]))
        x_f_h.append(var(a[:, b]))
        # x_f_h.append(tm3(a[:, b]))
        x_f_h.append(wl(a[:, b]))
        x_f_h.append(aac(a[:, b]))
    train_x_f.append(x_f_h)

# print(len(train_x_f), len(train_x))
clf = sklearn.ensemble.AdaBoostClassifier(n_estimators=7, learning_rate=1) #, random_state=np.random.randint(0,9))
clf2 = sklearn.ensemble.RandomForestClassifier()
clf3 = sklearn.ensemble.RandomForestClassifier(n_estimators=25)

clf.fit(train_x_f, train_y)
clf2.fit(train_x_f, train_y)
clf3.fit(train_x_f, train_y)

y_i = clf.predict(train_x_f)
print('SkLearn : ', metrics.accuracy_score(train_y, y_i))

print(train_x_f[0])

print("Training Complete!")

with open('META001.pkl', 'wb') as fid:
    cPickle.dump(clf, fid)

with open('META002.pkl', 'wb') as fid:
    cPickle.dump(clf2, fid)

with open('META003.pkl', 'wb') as fid:
    cPickle.dump(clf3, fid)
sleep(1)
hub.shutdown()