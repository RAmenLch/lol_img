import cv2
import numpy as np





class SkinData():
    def __init__(self,id,data):
        self.id = id
        self.data = data
        self.xystack = [(-1,0)]
    def DegreeOfComparability(self,data):
        degree = 0;
        for i in range(4):
            degree += abs(data[i] - self.data[i])
        degree = degree*2 + abs(data[4] - self.data[4])*1
        return 100/(degree + 1)
    def __str__(self):
        return  self.id + ':' + str(self.data)[1:-1]
    def pushAutoFitXY(self,xy,degree):
        self.xystack.append((xy,degree))
        self.xystack.sort(key=lambda x:x[1])
    def popAutoFitXY(self):
        if self.xystack:
            self.xystack.pop(-1)
            if self.xystack:
                return True
            else:
                return False
        else:
            return False
    def MaxDegree(self):
            return self.xystack[-1][1]
    def Maxxy(self):
        return self.xystack[-1][0]

def getSkinData():
    skdata = []
    with open('pskindict_aj.txt','r') as file:
        while 1:
            strdict = file.readline()
            if not strdict:
                break
            id,data = strdict.split(':')
            data = data[:-1].split(',')
            data = list(map(float,data))
            skdata.append(SkinData(id,data))
    return skdata


def optimalSolution(datas,n):
    Apartments = {}
    fuck = SkinData('test1.jpg',[0,0,0,0])
    skdata = getSkinData()
    for skd in skdata:
        for k in range(n*n):
            doc = skd.DegreeOfComparability(datas[k])
            if not k in Apartments:
                skd.pushAutoFitXY(k,doc)
            else:
                if Apartments[k].MaxDegree() < skd.MaxDegree():
                    skd.pushAutoFitXY(k,doc)
        if not skd.Maxxy() in Apartments:
            Apartments[skd.Maxxy()] = skd
        else:
            robApartment(Apartments,Apartments[skd.Maxxy()])
            Apartments[skd.Maxxy()] = skd
    ids = []
    for k in range(n*n):
        ids.append(Apartments.get(k, fuck).id)
    return ids



def robApartment(Apartments,vagrant):
    if vagrant.popAutoFitXY():
        if not vagrant.Maxxy() in Apartments:
            Apartments[vagrant.Maxxy()] = vagrant
            return
        else:
            if Apartments[vagrant.Maxxy()].MaxDegree() < vagrant.MaxDegree():
                robApartment(Apartments,Apartments[vagrant.Maxxy()])
                Apartments[vagrant.Maxxy()] = vagrant
            else:
                robApartment(Apartments,vagrant)



#max_size = 29
def LCimg(imgPath,N = 29):
    img = cv2.imread(imgPath)
    img_r = cv2.resize(img,(N*2,N*2))
    img_g = cv2.cvtColor(img_r,cv2.COLOR_BGR2GRAY)
    cv2.imshow('',img)
    cv2.waitKey()
    datalist = []
    for i in range(0,N*2,2):
        for j in range(0,N*2,2):
            data = np.array([img_g[i][j],img_g[i][j+1],img_g[i+1][j],img_g[i+1][j+1]])
            data = np.append(data,np.mean(data))
            datalist.append(data)
    ids = optimalSolution(datalist,N)
    getNewImg(ids,N)


#####!!
def getNewImg(ids,n):
    listi = []
    for i in range(n):
        listj = []
        for j in range(n):
            id = ids[i*n + j]
            img = cv2.imread('img_Pure/' + id)
            img_r = cv2.resize(img,(33,17))
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
    #imageTAT = cv2.cvtColor(imageTAT,cv2.COLOR_BGR2GRAY)
    cv2.imshow('',imageTAT)
    cv2.waitKey()


LCimg('test_img/riot1.jpg')
