# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 19:38:39 2017

@author: destiny
"""

"""
将pays.csv中的内容按照星期进行划分
"""
import csv
import tools

date_dictionary = {}

def writebyweek(date,words):
    weekday = tools.get_week(date)
    file_name = 'week' + str(weekday) + ".csv"
    if not date_dictionary.has_key(weekday):
        date_dictionary[weekday] = True
        f = open('../dataset/week/'+file_name,'ab+')
        write = csv.writer(f)
        write.writerow(['shop_id','time','pays'])
        write.writerow(words)
        f.close()
    else:
        f = open('../dataset/week/'+file_name,'ab+')
        write = csv.writer(f)
        write.writerow(words)
        f.close()

def split_by_week():
    f = open('../pay.csv')
    rows = csv.reader(f)
    rows.next()
    for row in rows:
        date = row[1]
        writebyweek(date,row)