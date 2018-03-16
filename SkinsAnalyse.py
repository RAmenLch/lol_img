import cv2
import numpy as np
'''
本模块主要分析皮肤原画,左上左下右上右下四个区域的灰度值和平均灰度值,将其保存在pskindict.txt

输入:
    'pureImgids.txt:保存所有的纯净无重复皮肤的皮肤文件名
输出:
    pskindict.txt:每个皮肤插画的左上左下右上右下平均灰度值

缺点:
    实际的灰度值并不完美,需要经过调整
'''
def getPureSkinFileName():
    with open('pureImgids.txt','r') as file:
        strids = file.read()
    fNames = strids[1:-1].split(',')
    return fNames


def analyseSkin(size = (2,2)):
    fns = getPureSkinFileName()
    for i in fns:
        img = cv2.imread('img_Pure/' + i, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img,size)
#        print(img)
        with open('pskindict.txt','a') as file:
            file.write(i + ':')
            for i in range(2):
                for j in range(2):
                    file.write(str(img[i][j]) + ',')
            file.write(str(np.mean(img)) + '\n')


analyseSkin()
