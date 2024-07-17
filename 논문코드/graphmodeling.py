import math
import os
import pandas as pd
import glob
import numpy as np
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
from dtaidistance import dtw
import csv
from pprint import pprint
import matplotlib.pyplot as plt


user_device_0 = 'C:\\논문코드\\데이터가공소\\dataset\\userdevice\\user-device_0.csv' #유저와 디바이스 관계
private_mobile_devices_0 = 'C:\\논문코드\\데이터가공소\\dataset\\mobiledevice\\private_mobile_devices_0.csv' #유저 디바이스 위치 시간

graph1 = 'C:\\논문코드\\데이터가공소\\dataset\\분석중\\time2.csv'
# graph1 = 'time2.csv'
user_device = open(graph1, 'r')
dictTime = {}

for line in user_device:
    line = line.replace('\n', '').split(',')

    # print(i)

    if line[1] == 'id_user':
        continue

    # print(i)
    xy = list(map(float, line[2:4]))
    time = line[4:6]

    allcol = xy + time

    # print(allcol)
    # i[1] 은 id_user 이다.
    if line[1] in dictTime:
        dictTime[line[1]].append(allcol)
    else:
        dictTime[line[1]] = [allcol]
    # pprint(dictTime)

# id_user 를 리스트타임[] 안에 넣음
listTime = list(dictTime.keys())
Graphmodeling = {}
# pprint(Graphmodeling[t])
# t 는 user i 는 내용물
for userid in listTime:
    Morning = {}
    Afternoon = {}
    Evening = {}
    Night = {}
    # daylist = {}

    for line in dictTime[userid]:

        start = datetime.strptime(line[2], '%Y-%m-%d %H:%M:%S')  # str datetime 으로 타입변환
        stop = datetime.strptime(line[3], '%Y-%m-%d %H:%M:%S')

        # x = int(i[0] / 0.015)  # 일단 좌표로 찍어버리기 ( 튜플 )
        # y = int(i[1] / 0.015)
        x = int(line[0] / 0.015) # 일단 좌표로 찍어버리기 ( 튜플 )
        y = int(line[1] / 0.015)
        #         z = [x,y,start,stop]
        
        a = start.strftime('%H:%M:%S')
        b = stop.strftime('%H:%M:%S')
        
        z = (x,y)
        # z = ((x, y), (a, b))

        # 시간대 별로 나누어서 리스트에 저장
        if 5 <= start.hour <= 12:
            if stop.day in Morning:
                Morning[stop.day].append(z)
            else:
                Morning[stop.day] = [z]
        elif 10 <= start.hour <= 18:
            if stop.day in Afternoon:
                Afternoon[stop.day].append(z)
            else:
                Afternoon[stop.day] = [z]
        elif 16 <= start.hour <= 21:
            if stop.day in Evening:
                Evening[stop.day].append(z)
            else:
                Evening[stop.day] = [z]
        elif 20 <= start.hour <= 6:
            if stop.day in Night:
                Night[stop.day].append(z)
            else:
                Night[stop.day] = [z]

        Graphmodeling[userid] = {}
        Graphmodeling[userid]['M'] = Morning
        Graphmodeling[userid]['A'] = Afternoon
        Graphmodeling[userid]['E'] = Evening
        # Graphmodeling[t]['N'] = Night
        
pprint(Graphmodeling["548"])

plt.scatter(*zip(*Graphmodeling['548']['M'][27]))
# plt.plot(*zip(*Graphmodeling['548']['M'][27]))
# plt.scatter(*Graphmodeling['555']['A'])
# plt.scatter(*Graphmodeling['555']['E'])
plt.grid(True)
plt.show()