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

SameImage()缺点:速度巨慢,预计2个小时,没有进行优化,建议晚上睡觉前运行

定义: 集合A与集合B 冗余:则是集合A & 集合B 非空

SameImage() 计算出的相似皮肤集还有缺点,此模块优化此缺点:'N个集合中皮肤id冗余'
于是添加了mergeSameImgSet()
输入:
    sameskin.txt 保存若干集合,集合中保存相似的皮肤id,但皮肤id有冗余
输出:
    MSImgid.txt 保存经'集合合并:mergeSameImgSet()'的不冗余的相似皮肤集合
    select_img/'id'/*.jpg:供人工挑选的图片文件:saveSameImg()
'''



def getids():
        ids = []
        with open('skinid.txt','r') as file:
            data =  file.read();
        ids = data.split(',')
        return ids[:-1]


#取出sameskin.txt 或 MSImgid.txt 中的数据
def getidarray(str1 = 'sameskin.txt'):
    idsar = []
    with open(str1,'r') as file:
        while 1:
            STR = file.readline()
            if not STR:
                break
            STR = STR.replace('\'','')
            ids = STR[1:-3].split(', ')
            idsar.append(ids)
    return idsar



def SameImage():
    #已知有皮肤964个
    ids = getids()
    SUM = len(ids)
    for i in range(SUM):
        #timeA = datetime.datetime.now()
        flag = False
        #除了霞洛默认皮肤和第一个皮肤不可能同原画
        if int(ids[i])%1000 == 0 or int(ids[i])%1000 == 1:
            continue
        print(ids[i])
        #读取皮肤1的数据
        im1 = cv2.imread('img/' + ids[i] + '.jpg')
        #一个集合A,保存和皮肤1相似的皮肤id
        setSameSkinTemp = set()
        #i+1 不重复比较
        for j in range(i + 1,SUM):
            if int(ids[j])%1000 == 0 or int(ids[i])%1000 == 1:
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

#合并冗余集合函数
def  mergeSameImgSet():
    idsar = getidarray()
    SUM = (len(idsar))

    #冗余的集合列表,合并后删除,先存进此集合
    delSet = set()
    for i in range(SUM):
        #如果i 在删除的集合中,就不判断了,因为前面判定为冗余集合已经并入其他集合中了
        if i in delSet:
            continue
        #建立一个临时的集合1,保存i的数据
        setTemp1 = set(idsar[i])
        #为了后面的反复比较不与自己比较
        delSet.add(i)
        #flag 判断是否还有集合与自己冗余
        flag = True
        #当有集合可能与自己冗余时继续运行
        while flag == True:
            #假设已经没有集合与其冗余
            flag = False
            #与其他集合比较
            for j in range(SUM):
                #避免与自己和已经被合并的集合比较
                if j in delSet:
                    continue
                #设置一个临时set2保存j的数据
                setTemp2 = set(idsar[j])
                #如果set1 与 set2 冗余:合并2于1并标记在delSet中
                if setTemp1 & setTemp2 != set():
                    setTemp1 = setTemp1 | setTemp2
                    delSet.add(j)
                    #假设还有集合可能与自己冗余时继续运行
                    flag = True
        #得到一个不与其他集合冗余的集合,保存进MSImgid.txt
        with open('MSImgid.txt','a') as file:
            file.write(str(setTemp1) + ';\n')
    #合理输出0 ~ SUM-1
    #print(delSet)

#运行,并得到MSImgid.txt
#mergeSameImgSet()


if __name__ == '__main__':
    SameImage()
    mergeSameImgSet()
