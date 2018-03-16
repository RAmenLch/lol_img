from PIL import Image
import os

'''
定义: 集合A与集合B 冗余:则是集合A & 集合B 非空

SameImage 计算出的相似皮肤集还有缺点,此模块优化此缺点:'N个集合中皮肤id冗余'
并对后续的人工挑选进行辅助
经此役,img_Pure/ 重复皮肤者仅余霞洛,人工删掉即可,为保证多个英雄的皮肤插画均被挑选出来,
故在SameImage设置得比较严格,MSImgid.txt有非多个英雄的皮肤插画少量,故需要人工操作


输入:
    sameskin.txt 保存若干集合,集合中保存相似的皮肤id,但皮肤id有冗余
输出:
    ---人工挑选前---
    MSImgid.txt 保存经'集合合并:mergeSameImgSet()'的不冗余的相似皮肤集合
    select_img/'id'/*.jpg:供人工挑选的图片文件:saveSameImg()

    ---人工挑选所需要做的事---
        将select_img/ 中 各文件夹中重复的皮肤删剩下一个
    ---人工挑选后---
    img_Pure/*jpg:
        img_Pure/ 人工复制于 img/
        将img_Pure/*.jpg 中 MSIgid.txt中保存id 对应的图片删除:delImgToPure()
        将select_img/ 文件夹中仅剩的图片 复制进 img_Pure/
    savePureImgids.txt:
        保存img_Pure/ 中剩余的"纯净的"皮肤 文件名

'''


#取出sameskin.txt 或 MSImgid.txt 中的数据
def getidarray(str1 = 'sameskin.txt'):
    idsar = []
    with open(str1,'r') as file:
        while 1:
            STR = file.readline()
            if not STR:
                break
            ids = STR[1:-3].split(', ')
            idsar.append(ids)
    return idsar
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

#复制MSImgid.txt 标记的皮肤
def saveSameImg():
    idsar = getidarray('MSImgid.txt')
    for i in idsar:
        os.mkdir('select_img/' + i[0])
        for j in i:
            with Image.open('img/' + j + '.jpg') as img:
                img.save('select_img/' + i[0] + '/' + j + '.jpg')
#删除img_Pure/(img/复件)中MSImgid.txt标记的皮肤
def delImgToPure():
    idsar = getidarray('MSImgid.txt')
    for i in idsar:
        for j in i:
            os.remove('img_Pure/' + j + '.jpg')
            print('remove' + j)
#保存"删除相同皮肤"成果:img_Pure中所有皮肤的文件名
#pureImgids.txt与skinids的区别在,前者减去了 人工挑选 中删除的重复皮肤的id 并添加了.jpg的后缀
def savePureImgids():
    file_dir = 'img_Pure'
    for root, dirs, files in os.walk(file_dir):
        strids = str(files).replace('\'','').replace(' ', '')
    with open('pureImgids.txt','w') as file:
        file.write(strids)
