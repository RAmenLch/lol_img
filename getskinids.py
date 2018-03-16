import requests
import re
import time

'''
副爬虫:
    爬取crawler.py所需皮肤id
资源文件:
    champion.js: 保存所有英雄名和对应的英雄id 例:'266:Aatrox,'
副产物:
    name.txt:    保存所有英雄名
输出:
    skinid.txt:  记录皮肤id对应的所有皮肤
'''



def write_id_name():
    names = []
    with open('champion.js','r') as file:
        data =  file.read();
        nameids = data.split(',')
        for i in nameids:
            names.append(i.split(':')[1])
    with open('name.txt','w') as file:
        for i in names:
            file.write(i + ',')


def writeskinids():
    with open('name.txt','r') as file:
        names = file.read()
    name = names.split(',')
    for i in name:
        #爬取包含英雄皮肤信息的文件 'name'.js
        html = requests.get('http://lol.qq.com/biz/hero/' + i + '.js')
        time.sleep(0.1)
        #使用正则表达式得到相应的皮肤id
        data = re.findall(r'"skins":\[(.*?)\]', str(html.content))
        skinids = re.findall(r'"id":"(.*?)"',str(data))
        #将皮肤id存入文件skinid.txt中
        for i in skinids:
            with open('skinid.txt','a') as file:
                file.write(str(i) + ',')
