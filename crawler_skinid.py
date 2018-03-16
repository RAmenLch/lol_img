import requests
import re
import time

'''
副爬虫:
    爬取主爬虫所需皮肤id
资源文件:
    champion.js: 保存所有英雄名和对应的英雄id 例:'266:Aatrox,'
输出:
    skinid.txt:  记录皮肤id对应的所有皮肤
'''



def getHeroNameList():
    names = []
    with open('champion.js','r') as file:
        data =  file.read();
        nameids = data.split(',')
        for i in nameids:
            names.append(i.split(':')[1])
    return names



def writeskinids():
    names = getHeroNameList()
    for name in names:
        #爬取包含英雄皮肤信息的文件 'name'.js
        html = requests.get('http://lol.qq.com/biz/hero/' + name + '.js')
        time.sleep(0.1)
        #使用正则表达式得到相应的皮肤id
        data = re.findall(r'"skins":\[(.*?)\]', str(html.content))
        skinids = re.findall(r'"id":"(.*?)"',str(data))
        #将皮肤id存入文件skinid.txt中,
        with open('skinid.txt','w') as file:
            file.write('')
        for i in skinids:
            with open('skinid.txt','a') as file:
                file.write(str(i) + ',')

#writeskinids()
