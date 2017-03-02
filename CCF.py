# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 11:16:50 2016

@author: Administrator
"""
#抽取需要预测的产品的部分信息
def pre_product_market():
    f = open(r'product_market.csv')
    ff= open(r'predict.csv','w')
    con = f.readlines()
    for line in con:
        line = line.strip()
        array = line.split(',')
        ff.write('%s,%s,%s,%s\n'%(array[1],array[2],array[3],array[4]))
    f.close()
    ff.close()
#抽取需要预测的产品的数据信息
def pre_farm():
    f1 = open(r'farming.csv')
    f2= open(r'newdata.csv','w')
    f3 = open(r'predict.csv')
    a = []
    con = f3.readlines()
    for line in con:
        line = line.strip()
        array = line.split(',')
        if (array[0],array[1],array[2]) not in a:
            a.append((array[0],array[1],array[2]))
    print len(a)
    con = f1.readlines()
    for line in con:
        line = line.strip()
        array = line.split(',')
        if (array[1],array[2],array[3]) in a:
            f2.write('%s,%s,%s,%s,%s\n'%(array[1],array[2],array[3],array[-4],array[-1]))
    f1.close()
    f2.close()
    f3.close()
#获取最近一天价格
def base():
    f = open(r'newdata.csv')
    ff = open(r'last30_data.csv','w')
    con = f.readlines()
    for line in con:
        line = line.strip()
        array = line.split(',')
        date = array[-1].split('-')
        if date[0] == '2016' and date[1] == '06' :#and int(date[2]) >= 28:
            ff.write('%s\n'%line)
    f.close()
    ff.close()
    f1 = open(r'last30_data.csv')
    f2 = open(r'predict.csv')
    f3 = open(r'result.csv','w')
    dic1 = {}
    con1 = f1.readlines()
    con2 = f2.readlines()
    dd = 0
    old_index = (0,0,0)
    for line in con1:
        line = line.strip()
        array = line.split(',')
        index = (array[0],array[1],array[2])
        if index!=old_index:
            dd = 0
        date = array[-1].split('-')
        day = int(date[-1])        
        if day > dd:
            dd = day
            dic1[index] = array[-2]
            old_index = index
    print len(dic1)
    for line in con2:
        line = line.strip()
        array = line.split(',')
        index = (array[0],array[1],array[2])
        if index in dic1:            
            f3.write('%s,%s,%s,%s,%s\n'%(array[0],array[1],array[2],array[-1],dic1[index]))
        else:
            print index
    f1.close()
    f2.close()
    f3.close()
def avg(l):
    return float(sum(l)/len(l))
def last_avg(n):
    f1 = open(r'last30_data.csv')
    f2 = open(r'predict.csv')
    f3 = open(r'result_%d.csv'%n,'w')
    dic1 = {}
    con1 = f1.readlines()
    for line in con1:
        line = line.strip()
        array = line.split(',')
        index = (array[0],array[1],array[2])
        if index in dic1:
            dic1[index].append(float(array[-2]))
        else:
            dic1[index] = [float(array[-2])]
    print len(dic1)
    con2 = f2.readlines()
    ff = open(r'result.csv')
    conf = ff.readlines()
    dd = {}
    for line in conf:
        line = line.strip()
        array = line.split(',')
        index = (array[0],array[1],array[2])
        if index not in dic1:
            dd[index] = float(array[-1])
    print len(dd)
    for line in con2:
        line = line.strip()
        array = line.split(',')
        index = (array[0],array[1],array[2])
        if index in dic1:    
            f3.write('%s,%s,%s,%s,%s\n'%(array[0],array[1],array[2],array[-1],avg(dic1[index][-n:])))
        else:
            f3.write('%s,%s,%s,%s,%s\n'%(array[0],array[1],array[2],array[-1],dd[index]))
    ff.close()
    f1.close()
    f2.close()
    f3.close()
def revised():
    rate1 = dec_rate()#平均下降率0.831618327819
    rate2 = 1
    f = open(r'result.csv')
    con = f.readlines()
    ff = open(r'result_revised.csv','w')
    change = ['果品','蔬菜','客菜']
    change2 = ['玫瑰花','配花类','百合花','康乃馨']
    for line in con:
        line = line.strip()
        array = line.split(',')
        if array[1] not in change:
            if array[1] in change2:
                ff.write("%s,%s,%s,%s,%.1f\n"%(array[0],array[1],array[2],array[3],float(array[4])*rate2))#未调整
            else:
                ff.write("%s\n"%line)
        else:
            if array[3]>'2016-07-03':            
                ff.write("%s,%s,%s,%s,%.1f\n"%(array[0],array[1],array[2],array[3],float(array[4])*rate1))
            else:
                ff.write("%s\n"%line)
    f.close()
    ff.close()
def dec_rate():
    cla = ['果品','蔬菜','客菜']
    f = open(r'e:\newdata.csv')
    ff = open(r'e:\file_for_rate.csv','w')
    con = f.readlines()
    for line in con:
        line = line.strip()
        array = line.split(',')
        if (array[-1]>='2015-06-01' and  array[-1]<='2015-06-30')or(array[-1]>='2015-07-01' and  array[-1]<='2015-07-30'):
            ff.write("%s\n"%line)
    ff.close()
    f.close()
    f = open(r'e:\file_for_rate.csv')
    con = f.readlines()
    dic6={}#6月价格字典
    dic7={}#7月价格字典
    for line in con:
        line = line.strip()
        array = line.split(',')
        if array[1] in cla:
            index = (array[0],array[1],array[2])
            if array[-1]>'2015-07-01':
                if index in dic7:
                    dic7[index].append(float(array[-2]))
                else:
                    dic7[index]=[float(array[-2])]
            else:
                if index in dic6:
                    dic6[index].append(float(array[-2]))
                else:
                    dic6[index]=[float(array[-2])]
    keys = []
    for key in dic6:
        dic6[key] = avg(dic6[key])
        try:
            dic7[key] = avg(dic7[key])
        except:
            keys.append(key)
            continue
    ans = []
    for key in dic6:
        if key not in keys:
            if dic6[key]/dic7[key]*1.0 < 1.0:
                ans.append( dic6[key]/dic7[key]*1.0)
    for i in ans:
        if i <0.9 and i>0.8:
            print i
    print avg(ans)
    f.close()
dec_rate()