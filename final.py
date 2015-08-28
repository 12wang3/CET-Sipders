# -*- coding: utf-8 -*-
__author__ = '12wang3'

import time
import xlrd
import xlwt
import numpy as np
import matplotlib.pyplot as plt

import re
import urllib.parse
import urllib.request
import http.cookiejar
import gzip

stuType = np.dtype([
    ('no', 'U5'),
    ('cet', 'U10'),
    ('schoolZone', 'U10'),
    ('room', 'U10'),
    ('seat', 'U10'),
    ('examNum', 'U50'),
    ('name', 'U50'),
    ('sex', 'U50'),
    ('papers', 'U50'),
    ('department', 'U50'),
    ('grade', 'U10'),
    ('class', 'U50'),
    ('stuID', 'U50'),
    ('baoNum', 'U50'),
    ('location', 'U50'),
])

sheetData = xlrd.open_workbook('s.xls')
sheet = sheetData.sheet_by_index(1)
stu = np.empty(sheet.nrows, dtype=stuType)
stuScore = np.empty((sheet.nrows,4),dtype = 'int32')
for i in range(sheet.nrows):
    stu[i] = np.array(tuple(sheet.row_values(i)), dtype=stuType)

headers = [
{
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
    #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'User-Agent': 'Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10245',
    'Host': 'www.chsi.com.cn',
    'Referer': 'http://www.chsi.com.cn/cet/',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'Keep-Alive',
}
,
{
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
    #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'User-Agent': 'Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.35',
    'Host': 'www.chsi.com.cn',
    'Referer': 'http://www.chsi.com.cn/cet/',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'Keep-Alive',
}
,
{
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
    #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'User-Agent': 'Mozilla/4.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.5',
    'Host': 'www.chsi.com.cn',
    'Referer': 'http://www.chsi.com.cn/cet/',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'Keep-Alive',
}
,
]
def makeMyOpener(head):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

def askScore(values,i):
    oper = makeMyOpener(headers[2-i%3])
    # print('********')
    url0 = 'http://www.chsi.com.cn/images/perf.gif?rt.start=navigation&nt_red_cnt=0&nt_nav_type=0&nt_nav_st=1440499148406&nt_red_st=0&nt_red_end=0&nt_fet_st=1440499148410&nt_dns_st=1440499148410&nt_dns_end=1440499148410&nt_con_st=1440499148410&nt_con_end=1440499148410&nt_req_st=1440499148411&nt_res_st=1440499148558&nt_res_end=1440499148558&nt_domloading=1440499148560&nt_domint=1440499148692&nt_domcontloaded_st=1440499148697&nt_domcontloaded_end=1440499148700&nt_domcomp=1440499148840&nt_load_st=1440499148840&nt_load_end=1440499148841&nt_unload_st=1440499148560&nt_unload_end=1440499148563&dns.t=577&v=0.9&u=http%3A%2F%2Fwww.chsi.com.cn%2Fcet%2F&rt.tstart=1440499148406&rt.bstart=1440499148674&rt.end=1440499196835&t_done=48429&r=http%3A%2F%2Fwww.chsi.com.cn%2Fcet%2Fquery%3Fzkzh%3D510020151200502%26xm%3D%25E6%259D%258E%25E8%2590%258C&rt.quit='
    #print(values['zkzh'], values['xm'])
    datal = urllib.parse.urlencode(values)
    url = 'http://www.chsi.com.cn/cet/query?'+datal
    uop = oper.open(url0)
    uop = oper.open(url)
    result = gzip.decompress(uop.read()).decode()
    print(result)

    answer=[]
    pattern = re.compile('<tr.*?>.*?</tr>', re.S)
    list = re.findall(pattern, result)
    # print(list[6])##################################################################################################
    pad = re.compile(r'<span class="colorRed">(.*?)</span>', re.S)
    listd = re.findall(pad, list[6])
    answer.append(int(listd[0].strip()))
    # print(listd[0].strip())
    pad = re.compile(r'</span>(.*?)[<br />|</td>]', re.S)
    listd = re.findall(pad, list[6])
    for i,e in enumerate(listd[1:]):
        answer.append(int(e.strip()))
        # print(i,e.strip())
    # print(answer)
    return answer

file = xlwt.Workbook()
ws0 = file.add_sheet('成绩')
for i in range(sheet.ncols):
    ws0.write(0,i,stu[0][i])
ws0.write(0,15,'总分')
ws0.write(0,16,'听力')
ws0.write(0,17,'阅读')
ws0.write(0,18,'写作与翻译')
print(sheet.nrows)
try:
    for i in range(12491,sheet.nrows):
        #print('########')
        stuValues = {}
        stuValues['zkzh'] = stu[i]['examNum']
        stuValues['xm'] = stu[i]['name']
        print(i)
        stuScore[i]=np.array(askScore(stuValues,i))
        for j in range(sheet.ncols):
            ws0.write(i,j,stu[i][j])
        for j in range(4):
            ws0.write(i,j+15,int(stuScore[i][j]))
        # time.sleep(1)
        #print('*******')
    file.save('w21.xls')
except:
    file.save('w21.xls')

'''for i in range(1,50):
    print(stuScore[i])'''
