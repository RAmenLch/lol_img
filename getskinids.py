import requests
import re
import time
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
        html = requests.get('http://lol.qq.com/biz/hero/' + i + '.js')
        time.sleep(0.1)
        data = re.findall(r'"skins":\[(.*?)\]', str(html.content))
        skinids = re.findall(r'"id":"(.*?)"',str(data))
        for i in skinids:
            with open('skinid.txt','a') as file:
                file.write(str(i) + ',')
