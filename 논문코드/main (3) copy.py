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

graph1 = 'time2.csv'
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

# user = '685'
# pprint(Graphmodeling[user])
# print(f"------------------------------------------------------------")
print("Step 1 ...")
time_zone_list = ['M', 'A', 'E', 'N'] #아침, 점심, 저녁, 밤

for user in Graphmodeling:
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
    # # pprint(Graphmodeling)
    # print(f"------------------------------------------------------------")
#
# def get_counts(seq):
#     counts = {}
#     for x in seq:
#         if x in counts:
#             counts[x] += 1
#         else:
#             counts[x] = 1
#     return counts

#
#
# for i in Graphmodeling:
#     for j in Graphmodeling[i]:
#         for k in Graphmodeling[i][j]:
#             # print(Graphmodeling[i][j][k])
#             # print(i,j,k,get_counts(Graphmodeling[i][j][k]))
print("Step 2 ...")
dtw_res = []
best_paths = []
from dtaidistance import dtw_ndim
for line in Graphmodeling: #user
    for j in Graphmodeling[line]: #tz
        tz_res = []
        listDay = list(Graphmodeling[line][j].keys()) #date
        # print(listDay)
        for d in listDay: #첫번째날
            # print(d,j)
            # print(Graphmodeling[i][j][d])
            s1 = np.array(Graphmodeling[line][j][d])

            for k in range(1,10): #10일치라서 10까지
                if d+k in listDay:
                        # print(d,k,d+k,Graphmodeling[i][j][d+k])
                        if (len(Graphmodeling[line][j][d]) > 1) and (len(Graphmodeling[line][j][d + k]) > 1):
                            s2 = np.array(Graphmodeling[line][j][d + k])
                            distance = dtw_ndim.distance(s1, s2) #calculate DTW 거리
                            # dtw_ndim.warping_paths(s1, s2)
                            # dd, paths = dtw.warping_paths(s1, s2)
                            wj_path = dtw_ndim.warping_path(s1, s2) #DTW 최적 경로
                            # best_paths.append(wj_path)
                            d_res = (line, j, d, d + k, distance, wj_path)
                            # dtw_res.append(d_res)
                            tz_res.append(d_res)

                            # dtw_res.append(tz_res[0])
                            # print(j,d,k,d+k,s1,s2,dd)
                else:
                    continue

        if len(tz_res) > 0:
            #pprint(tz_res[0])
            tz_res.sort(key=lambda x: x[4]) #distance 정렬
            dtw_res.append(tz_res[0])
    # pprint(dtw_res)
#
# tmp1 = []
#
# for data in dtw_res:
#     user = data[0]
#     tz = data[1]
#     date1 = data[2]
#     date2 = data[3]
#     dtw_distance = data[4]
#     dtw_path = data[5]
#
#     s1 = Graphmodeling[user][tz][date1]
#     s2 = Graphmodeling[user][tz][date2]
#     path_avg = []
#
#     for hb_path in dtw_path:
#         h1 = hb_path[0]
#         h2 = hb_path[1]
#         b1 = s1[h1]
#         b2 = s2[h2]
#         print(b1, b2)
#         point = ((b1[0] + b2[0]) / 2, (b1[1] + b2[1]) / 2)
#         path_avg.append(point)
#
#     tmp_res = [user, tz, date1, date2, dtw_distance, dtw_path, path_avg]
#     tmp1.append(tmp_res)
print("Step 3 ...")
user_tz_patterns = []
# Graphmodeling2 = {}
# Pattern = {}
# Pattern = {}
# Graphmodeling2 = {}
for data in dtw_res:
    user = data[0]
    tz = data[1]
    date1 = data[2]
    date2 = data[3]
    dtw_distance = data[4]
    dtw_path = data[5]
    s1 = Graphmodeling[user][tz][date1]
    s2 = Graphmodeling[user][tz][date2]
    path_avg = []
    for hb_path in dtw_path:
        h1 = hb_path[0]
        h2 = hb_path[1]
        b1 = s1[h1]
        b2 = s2[h2]
        # print(b1, b2)
        point = ((b1[0] + b2[0]) / 2, (b1[1] + b2[1]) / 2)
        path_avg.append(point)
    # tmp_res = [user, tz, date1, date2, dtw_distance, dtw_path, path_avg]
    tmp_res2 = [user, tz, path_avg]
    user_tz_patterns.append(tmp_res2)
    # print(user,tz,path_avg)


all_users_sim = {}
tmp_len1 = len(user_tz_patterns)
tmp_cnt = 0
for line in user_tz_patterns:
    print(f"processing ==> {tmp_cnt} / {tmp_len1}")
    dtw_sim_list = []
    sim_user_list = []

    uid = line[0]
    tz = line[1]
    def my_filter1(cmp_val):
        if cmp_val[0] != uid and cmp_val[1] == tz:
            return True
        else:
            return False

    to_compare_users = list(filter(my_filter1, user_tz_patterns))
    for another_user in to_compare_users:
            a = np.array(line[-1])
            b = np.array(another_user[-1])
            user_distance = dtw_ndim.distance(a, b)
            if user_distance < 41:
                dtw_sim_list.append(user_distance)
                sim_user_list.append(another_user[0])
            dtw_sim_set = set(dtw_sim_list)
            sim_user_set = set(sim_user_list)

    if uid in all_users_sim: #
        all_users_sim[uid] = all_users_sim[uid] + sim_user_list
    else:
        all_users_sim[uid] = sim_user_list
    tmp_cnt += 1
    # if tmp_cnt == 10:
    #     break
    # if tmp_cnt % 10 == 0:


        # tmp_len1 = len(user_tz_patterns)

# print(dtw_sim_set)
# print(sim_user_set)

user_file = 'user7.csv'
user_device = open(user_file, 'r')

ud = []

import csv
with open(user_file, newline='\n') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        ud.append(row)

ud = ud[1:]
ud_dict = {}
for row in ud:
    id = int(row[0])
    dd = row[1].replace("\'","").replace("[","").replace("]","").split(" ")
    gg = []

    for data in dd: #전처리
        d1 = list(filter(None, data.split(",")))
        d1 = list(map(int, d1))
        gg.append(d1)

    if id in ud_dict: #
        ud_dict[id].append(gg)
    else:
        ud_dict[id] = gg

from collections import Counter
# Counter({'apple': 3, 'egg': 2, 'banana': 1})
all_rcmd_lists = {}
all_rcmd_lists_cnt = {}
for user in all_users_sim:
    key = user
    uid = int(key)
    rcmd_list = list(map(int, all_users_sim.get(user)))
    rcmd_lists = []
    for user2 in sim_user_set:
        t_uid = int(user2)
        for item in ud_dict[t_uid]:
            rcmd_lists.append(item[1])
    counts = Counter(rcmd_lists)
    all_rcmd_lists_cnt[uid] = counts
    all_rcmd_lists[uid] = list(set(rcmd_lists))
# counts = Counter(rcmd_lists)
# 성능비교 추가예정
# all_rcmd_lists

rcmd_range_set = set(list(range(1,17))) #1~16
all_recall_precision = {}

for key in all_rcmd_lists:
    if key in ud_dict:
        current_rcmd_list = all_rcmd_lists.get(key)
        current_rcmd_set = set(current_rcmd_list)
        answer_rcmd_list = ud_dict.get(key)
        answer_rcmd_set = set(map(lambda item: item[1], answer_rcmd_list))

        TP = current_rcmd_set.intersection(answer_rcmd_set)
        FP = current_rcmd_set.difference(answer_rcmd_set)
        FN = answer_rcmd_set.difference(current_rcmd_set)
        TN = rcmd_range_set.difference(answer_rcmd_set).intersection(rcmd_range_set.difference(current_rcmd_set))


        # TP/TP+FP
        t_precision = len(TP) / (len(TP) + len(FP))
        # TP/TP+FN
        t_recall =  len(TP) / (len(TP) + len(FN))
        result = (t_precision, t_recall)
        all_recall_precision[key] = result
    else:
        print(f"No Recommend Lists for User : {key}")