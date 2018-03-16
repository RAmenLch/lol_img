import requests
import time
'''
主爬虫:爬取LOL官网上的英雄皮肤

资源文件[输入]:
    skinid.txt: 保存所有皮肤相对应的皮肤id
输出:
    img/*.jpg:  skinid.txt记录的皮肤id对应的所有皮肤

'''
#爬取皮肤url前缀:hurl + 皮肤id + '.jpg'为整个爬取使用的url
hurl = 'http://ossweb-img.qq.com/images/lol/web201310/skin/big'


#解析资源文件 skinid.txt并返回皮肤id列表
def getids():
    ids = []
    with open('skinid.txt','r') as file:
        data =  file.read();
    ids = data.split(',')
    return ids

#运行主函数
def main():
    ids = getids()
    for i in ids:
        try:
            url = hurl + i + '.jpg'
            #开始爬取
            html = requests.get(url)
            #如果爬取到空网页404,抛出异常
            html.raise_for_status()
            time.sleep(0.2)
            with open('img/' + i + '.jpg', 'wb') as file:
                file.write(html.content)
        except Exception as e:
            print(e)
main()
