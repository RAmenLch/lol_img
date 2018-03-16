import nphash
from PIL import Image
import cv2
import datetime


'''
相似皮肤寻找模块:
    英雄联盟皮肤有些是共用的,此模块寻找彼此相似的皮肤并保存其skinid
输入:
    skinid.txt:全部皮肤的id
    img/*.jpg:爬取到的皮肤
输出:
    sameskin.txt:保存每个有相似皮肤的皮肤 的'相似皮肤id集合'

此模块缺点:速度巨慢,预计4个小时,没有进行优化,建议晚上睡觉前运行
'''





def getids():
        ids = []
        with open('skinid.txt','r') as file:
            data =  file.read();
        ids = data.split(',')
        return ids
def main():
    #已知有皮肤964个
    ids = getids()
    SUM = len(ids)
    for i in range(SUM):
    #    timeA = datetime.datetime.now()
        flag = False
        #除了霞洛默认皮肤和第一个皮肤不可能同原画
        if int(ids[i])%1000 == 0 ||  int(ids[i])%1000 == 1:
            continue
        print(ids[i])
        #读取皮肤1的数据
        im1 = cv2.imread('img/' + ids[i] + '.jpg')
        #一个集合A,保存和皮肤1相似的皮肤id
        setSameSkinTemp = set()
        #i+1 不重复比较
        for j in range(i + 1,SUM):
            if int(ids[j])%1000 == 0 || int(ids[i])%1000 == 1:
                continue
            #同英雄的皮肤不可能和皮肤1同原画 PS:皮肤id的规律 str(int(英雄id *1000) + int(弱_皮肤id))
            elif abs(int(ids[j]) - int(ids[i])) <=20:
                continue
            else:
                #读取皮肤2
                im2 = cv2.imread('img/' + ids[j] + '.jpg')
                #比较皮肤1和皮肤的相似度
                Hdis = nphash.classify_hist_with_split(im1,im2)
                #若足够相似,则将皮肤2加入集合A
                if Hdis >= 0.74 :
                    flag = True
                    print(' ' + ids[j] + '!!')
                    setSameSkinTemp.add(ids[j])
        #如果出现一次相似,则皮肤1加入集合A,并保存集合A
        if flag == True:
                setSameSkinTemp.add(ids[i])
                with open('sameskin.txt','a') as file :
                    file.write(str(setSameSkinTemp) + ';\n')
        #timeB = datetime.datetime.now()
        #print(timeB - timeA)




main()
