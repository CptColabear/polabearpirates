import math
import os
import pandas as pd
import glob
import numpy as np
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
# from dtaidistance import dtw
import csv
from pprint import pprint

graph1 = 'time2.csv'
e = open(graph1, 'r')
dictTime = {}

for i in e:
    i = i.replace('\n', '').split(',')

    # print(i)

    if i[1] == 'id_user':
        continue

    # print(i)
    xy = list(map(float, i[2:4]))
    time = i[4:6]

    allcol = xy + time

    # print(allcol)
    # i[1] 은 id_user 이다.
    if i[1] in dictTime:
        dictTime[i[1]].append(allcol)
    else:
        dictTime[i[1]] = [allcol]
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
    daylist = {}

    for i in dictTime[t]:

        start = datetime.strptime(i[2], '%Y-%m-%d %H:%M:%S')  # str datetime 으로 타입변환
        stop = datetime.strptime(i[3], '%Y-%m-%d %H:%M:%S')

        # x = int(i[0] / 0.015)  # 일단 좌표로 찍어버리기 ( 튜플 )
        # y = int(i[1] / 0.015)
        x = int(i[0]/0.015) # 일단 좌표로 찍어버리기 ( 튜플 )
        y = int(i[1]/0.015)
        #         z = [x,y,start,stop]
        z = (x, y)

        # 시간대 별로 나누어서 리스트에 저장
        if 5 <= start.hour <= 12:
            if stop.day in Morning:
                Morning[stop.day].append(z)
            else:
                Morning[stop.day] = [z]
        elif 11 <= start.hour <= 18:
            if stop.day in Afternoon:
                Afternoon[stop.day].append(z)
            else:
                Afternoon[stop.day] = [z]
        elif 17 <= start.hour <= 23:
            if stop.day in Evening:
                Evening[stop.day].append(z)
            else:
                Evening[stop.day] = [z]
        elif 22 <= start.hour <= 6:
            if stop.day in Night:
                Night[stop.day].append(z)
            else:
                Night[stop.day] = [z]

        Graphmodeling[t] = {}
        Graphmodeling[t]['M'] = Morning
        Graphmodeling[t]['A'] = Afternoon
        Graphmodeling[t]['E'] = Evening
        Graphmodeling[t]['N'] = Night

    break

user = '685'
# pprint(Graphmodeling[user])
print(f"------------------------------------------------------------")

time_zone_list = ['M', 'A', 'E', 'N'] #아침, 점심, 저녁, 밤


for cnt in range(0, 51):
    # print(f"------------------------------{cnt} loop ... !------------------------------")
    for tz in Graphmodeling[user]: #각 타임존에 대하여 반복
        for day in Graphmodeling[user][tz]:
            x1 = Graphmodeling[user][tz][day]
            tlist = []
            close_list = []
            avg_list = {}
            for idx in range(0, len(x1)):
                for idx1 in range(idx+1, len(x1)):
                    p1 = x1[idx]
                    p2 = x1[idx1]
                    a = p1[0] - p2[0]  # 선 a의 길이
                    b = p1[1] - p2[1]  # 선 b의 길이
                    c = math.sqrt((a * a) + (b * b))
                    res = [p1, p2, c]
                    # print(res)
                    if c <= 2:
                        close_list.append(res)
                        a1 = (p1[0] + p2[0]) / 2 # 선 a의 길이
                        b1 = (p1[1] + p2[1]) / 2 # 선 b의 길이
                        avg_p = (a1, b1)
                        avg_list[p1] = avg_p
                        avg_list[p2] = avg_p
                        # print(avg_p)

            for p in range(0, len(x1)):
                if x1[p] in avg_list:
                    x1[p] = avg_list.get(x1[p])
                    Graphmodeling[user][tz][day] = x1
                    # print(f"Day: {day}, TZ: {tz}, {x1[p]}")
# pprint(Graphmodeling)
print(f"------------------------------------------------------------")

def get_counts(seq):
    counts = {}
    for x in seq:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts

#
#
# for i in Graphmodeling:
#     for j in Graphmodeling[i]:
#         for k in Graphmodeling[i][j]:
#             # print(Graphmodeling[i][j][k])
#             # print(i,j,k,get_counts(Graphmodeling[i][j][k]))

dtw_res = []

from dtaidistance import dtw_ndim
for i in Graphmodeling: #user
    for j in Graphmodeling[i]: #tz
        tz_res = []
        listDay = list(Graphmodeling[i][j].keys()) #date
        # print(listDay)
        for d in listDay: #첫번째날
            # print(d,j)
            # print(Graphmodeling[i][j][d])
            s1 = np.array(Graphmodeling[i][j][d])

            for k in range(1,10): #10일치라서 10까지
                if d+k in listDay:
                        # print(d,k,d+k,Graphmodeling[i][j][d+k])
                        if (len(Graphmodeling[i][j][d]) > 1) and (len(Graphmodeling[i][j][d+k]) > 1):
                            s2 = np.array(Graphmodeling[i][j][d + k])
                            dd = dtw_ndim.distance(s1, s2) #calculate
                            d_res = (j,dd,s1,s2)
                            # dtw_res.append(d_res)
                            tz_res.append(d_res)

                            # dtw_res.append(tz_res[0])
                            # print(j,d,k,d+k,s1,s2,dd)
                else:
                    continue

        if len(tz_res) > 0:
            #pprint(tz_res[0])
            tz_res.sort(key=lambda x: x[1])
            dtw_res.append(tz_res[0])




# dtw_res.sort(key=lambda x: x[1])

pprint(dtw_res)