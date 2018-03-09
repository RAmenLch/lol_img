import cv2
import numpy as np


class SkinData():
    def __init__(self,id,data):
        self.id = id
        self.data = data
    def DegreeOfComparability(self,data):
        degree = 0;
        for i in range(4):
            degree += abs(data[i] - self.data[i])
        degree += abs(data[4] - self.data[4]) * 0.5
        return 100/degree
    def __str__(self):
        return 'id:' + self.id + ' data:' + str(self.data)


def getSkinData():
    skdata = []
    with open('pskindict.txt','r') as file:
        while 1:
            strdict = file.readline()
            if not strdict:
                break
            id,data = strdict.split(':')
            data = data[:-1].split(',')
            data = list(map(float,data))
            skdata.append(SkinData(id,data))
    return skdata


def optimalSolution(datas):
    skdata = getSkinData()
    ids = []

    for data in datas:
        maxdg = 0
        for i in skdata:
            if i.id in ids:
                continue
            dg = i.DegreeOfComparability(data)
            if dg > maxdg:
                maxdg = dg
                maxid = i.id
        ids.append(maxid)
    return ids



#max_size = 28
def LCimg(imgPath,size = 16):
    img = cv2.imread(imgPath)
    img_r = cv2.resize(img,(size,size))
    img_g = cv2.cvtColor(img_r,cv2.COLOR_BGR2GRAY)
    cv2.imshow('',img)
    cv2.waitKey()
    datalist = []
    for i in range(0,16,2):
        for j in range(0,16,2):
            data = np.array([img_g[i][j],img_g[i][j+1],img_g[i+1][j],img_g[i+1][j+1]])
            data = np.append(data,np.mean(data))
            datalist.append(data)
    ids = optimalSolution(datalist)
    getNewImg(ids,int(size/2))

#####!!
def getNewImg(ids,n):

    listi = []
    for i in range(n):
        listj = []
        for j in range(n):
            id = ids[i*n + j]
            img = cv2.imread('img/' + id)
            img_r = cv2.resize(img,(int(980/n),int(500/n)))
            listj.append(img_r)
        listi.append(listj)
    A = True
    for i in listi:
        imageQAQ = np.hstack(i)
        if A:
            imageTAT = imageQAQ
            A = False
        else:
            imageTAT = np.vstack((imageTAT,imageQAQ))
    cv2.imshow('',imageTAT)
    cv2.waitKey()


LCimg('test_img/penta1.jpg')
