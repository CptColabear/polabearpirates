import math
import os
import pandas as pd
import glob
import numpy as np
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
from dtaidistance import dtw
import csv
# from pprint import pprint

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
for t in listTime:
    Morning = {}
    Afternoon = {}
    Evening = {}
    Night = {}
    # daylist = {}

    for line in dictTime[t]:

        start = datetime.strptime(line[2], '%Y-%m-%d %H:%M:%S')  # str datetime 으로 타입변환
        stop = datetime.strptime(line[3], '%Y-%m-%d %H:%M:%S')

        # x = int(i[0] / 0.015)  # 일단 좌표로 찍어버리기 ( 튜플 )
        # y = int(i[1] / 0.015)
        x = int(line[0] / 0.015) # 일단 좌표로 찍어버리기 ( 튜플 )
        y = int(line[1] / 0.015)
        #         z = [x,y,start,stop]
        z = (x, y)

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

        Graphmodeling[t] = {}
        Graphmodeling[t]['M'] = Morning
        Graphmodeling[t]['A'] = Afternoon
        Graphmodeling[t]['E'] = Evening
        # Graphmodeling[t]['N'] = Night

threshold = 4
count = 0
Graphmodeling
for user in Graphmodeling:
    result = {}
    for tz in Graphmodeling[user]: #각 타임존에 대하여 반복
        for day, pattern in Graphmodeling[user][tz].items():
            # pattern = Graphmodeling[user][tz][day]
            # print(user,tz,day, pattern, len(pattern))
            if len(pattern) >= threshold:
                result[day] = pattern
            print(user,tz,result)
            
                
                
