from PIL import Image
import os

'''
为保证多个英雄的皮肤插画均被挑选出来,
故在SameImage设置得比较严格,MSImgid.txt有非多个英雄的皮肤插画少量,故需要人工操作
并对后续的人工挑选进行辅助


---人工挑选前---
将img/中复制到一个新文件夹起名img_Pure/
使用函数saveSameImg()建立select_img/
---人工挑选所需要做的事---
将select_img/ 中 各文件夹中重复的皮肤删剩下一个
---人工挑选后---
    img_Pure/*jpg:
        使用函数:delImgToPure()将img_Pure/*.jpg 中 MSIgid.txt中保存id 对应的图片删除
        将select_img/ 文件夹中仅剩的图片 复制进 img_Pure/
    savePureImgids.txt:
        使用函数 savePureImgids() 保存img_Pure/ 中剩余的"纯净的"皮肤 文件名

经此役,img_Pure/ 重复皮肤者仅余霞洛,人工删掉即可

'''


#取出sameskin.txt 或 MSImgid.txt 中的数据
def getidarray(str1 = 'MSImgid.txt'):
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


#复制MSImgid.txt 标记的皮肤
def saveSameImg():
    idsar = getidarray('MSImgid.txt')
    if not os.path.exists('select_img'):
        os.mkdir('select_img')
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
            #print('remove' + j)

#保存"删除相同皮肤"成果:img_Pure中所有皮肤的文件名
#pureImgids.txt与skinids的区别在,前者减去了 人工挑选 中删除的重复皮肤的id 并添加了.jpg的后缀
def savePureImgids():
    file_dir = 'img_Pure'
    for root, dirs, files in os.walk(file_dir):
        strids = str(files).replace('\'','').replace(' ', '')
    with open('pureImgids.txt','w') as file:
        file.write(strids)

if __name__ == '__main__':
    #saveSameImg()
    #delImgToPure()
    #----人工后------#
    #savePureImgids()
