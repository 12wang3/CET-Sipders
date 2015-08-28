# -*- coding: utf-8 -*-
__author__ = '12wang3'

import re
import urllib.parse
import urllib.request
import http.cookiejar
import gzip
headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
    'Host': 'www.chsi.com.cn',
    'Referer': 'http://www.chsi.com.cn/cet/',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'Keep-Alive',
}

def makeMyOpener(head):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

oper = makeMyOpener(headers)
values = {}
values['zkzh'] = '510020151200420'
values['xm'] = '徐莉'
url0 = 'http://www.chsi.com.cn/images/perf.gif?rt.start=navigation&nt_red_cnt=0&nt_nav_type=0&nt_nav_st=1440499148406&nt_red_st=0&nt_red_end=0&nt_fet_st=1440499148410&nt_dns_st=1440499148410&nt_dns_end=1440499148410&nt_con_st=1440499148410&nt_con_end=1440499148410&nt_req_st=1440499148411&nt_res_st=1440499148558&nt_res_end=1440499148558&nt_domloading=1440499148560&nt_domint=1440499148692&nt_domcontloaded_st=1440499148697&nt_domcontloaded_end=1440499148700&nt_domcomp=1440499148840&nt_load_st=1440499148840&nt_load_end=1440499148841&nt_unload_st=1440499148560&nt_unload_end=1440499148563&dns.t=577&v=0.9&u=http%3A%2F%2Fwww.chsi.com.cn%2Fcet%2F&rt.tstart=1440499148406&rt.bstart=1440499148674&rt.end=1440499196835&t_done=48429&r=http%3A%2F%2Fwww.chsi.com.cn%2Fcet%2Fquery%3Fzkzh%3D510020151200502%26xm%3D%25E6%259D%258E%25E8%2590%258C&rt.quit='
print(values['zkzh'], values['xm'])
datal = urllib.parse.urlencode(values)
url = 'http://www.chsi.com.cn/cet/query?'+datal
uop = oper.open(url0)
uop = oper.open(url)
result = gzip.decompress(uop.read()).decode()
print(result)

answer=[]
pattern = re.compile('<tr.*?>.*?</tr>', re.S)
list = re.findall(pattern, result)
print(list[6])
pad = re.compile(r'<span class="colorRed">(.*?)</span>', re.S)
listd = re.findall(pad, list[6])
answer.append(int(listd[0].strip()))
# print(listd[0].strip())
pad = re.compile(r'</span>(.*?)[<br />|</td>]', re.S)
listd = re.findall(pad, list[6])
for i,e in enumerate(listd[1:]):
    answer.append(int(e.strip()))
    # print(i,e.strip())
print(answer)
