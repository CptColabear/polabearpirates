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
import copy

user_device_0 = 'C:\\논문코드\\데이터가공소\\dataset\\userdevice\\user-device_0.csv' #유저와 디바이스 관계
private_mobile_devices_0 = 'C:\\논문코드\\데이터가공소\\dataset\\mobiledevice\\private_mobile_devices_0.csv' #유저 디바이스 위치 시간

graph1 = 'C:\\논문코드\\데이터가공소\\dataset\\분석중\\time2.csv'
# graph1 = 'time2.csv'
user_device = open(graph1, 'r')
dictTime = {}

for line in user_device:
    line = line.replace('\n', '').split(',')

    if line[1] == 'id_user':
        continue

    xy = list(map(float, line[2:4]))
    time = line[4:6]

    allcol = xy + time

    if line[1] in dictTime:
        dictTime[line[1]].append(allcol)
    else:
        dictTime[line[1]] = [allcol]

listTime = list(dictTime.keys())
Graphmodeling = {}

for userid in listTime:
    Morning = []
    Afternoon = []
    Evening = []
    Night = []

    for line in dictTime[userid]:

        start = datetime.strptime(line[2], '%Y-%m-%d %H:%M:%S')  # str datetime 으로 타입변환
        stop = datetime.strptime(line[3], '%Y-%m-%d %H:%M:%S')

        x = int(line[0] / 0.015) # 일단 좌표로 찍어버리기 ( 튜플 )
        y = int(line[1] / 0.015)
        
        a = start.strftime('%H:%M:%S')
        b = stop.strftime('%H:%M:%S')
        
        z = (x,y)
       

        # 시간대 별로 나누어서 리스트에 저장
        if 5 <= start.hour <= 12:
                Morning.append(z)
                
        elif 10 <= start.hour <= 18:
                Afternoon.append(z)

        elif 16 <= start.hour <= 21:
                Evening.append(z)


        Graphmodeling[userid] = {}

        Graphmodeling[userid]['M'] = Morning
        Graphmodeling[userid]['A'] = Afternoon
        Graphmodeling[userid]['E'] = Evening


wjlist = []
ptnlist = []

for userid in Graphmodeling:
    wjdict = {}
    wjdict['user'] = userid
    for tmz in Graphmodeling[userid]:
        wjdict['time'] = tmz
        for ptn in Graphmodeling[userid][tmz]:
            if userid in wjdict:
                ptnlist.append(ptn)
            else:
                ptnlist = ptn
            wjdict['pattern'] = ptnlist
            # print(wjdict)
        wjlist.append(wjdict)
           
print(wjlist)

# with open("dict12.csv", 'w') as file:
#     header = ['user', 'time', 'pattern']
#     writer = csv.DictWriter(file, fieldnames=header)
#     writer.writeheader()
            
#     for element in wjlist:
#         writer.writerow(element)

  

