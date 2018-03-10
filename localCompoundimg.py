import cv2
import numpy as np





class SkinData():
    def __init__(self,id,data):
        self.id = id
        self.data = data
        self.xystack = [(-1,0)]
        self.key = True
    def __init__(self):
        self.key = False


    def DegreeOfComparability(self,data):
        degree = 0;
        for i in range(4):
            degree += abs(data[i] - self.data[i])
        degree += abs(data[4] - self.data[4]) * 2
        return 100/degree
    def __str__(self):
        return 'id:' + self.id + ' data:' + str(self.data)
    def pushAutoFitXY(self,xy,degree):
        self.xystack.append((xy,degree))
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


def optimalSolution(datas,n):
    Apartments = []
    for i in range(n*n):
        Apartments.append([])

    skdata = getSkinData()
    for skd in skdata:
        for k in range(n*n):
            doc = skd.DegreeOfComparability(datas[k])
            if doc > skd.MaxDegree():
                if not Apartments[k]:
                    skd.pushAutoFitXY(k,doc)
                else:
                    if Apartments[k].MaxDegree() < skd.MaxDegree():
                        skd.pushAutoFitXY(k,doc)
        if not Apartments[skd.Maxxy()]:
            Apartments[skd.Maxxy()] = skd
        else:
            robApartment(Apartments,Apartments[skd.Maxxy()])
            Apartments[skd.Maxxy()] = skd
    ids = []
    for apm in Apartments:
        ids.append(apm.id)
    return ids



def robApartment(Apartments,vagrant):
    if vagrant.popAutoFitXY():
        if not Apartments[vagrant.Maxxy()]:
            Apartments[vagrant.Maxxy()] = vagrant
            return
        else:
            if Apartments[vagrant.Maxxy()].MaxDegree() < vagrant.MaxDegree():
                robApartment(Apartments,Apartments[vagrant.Maxxy()])
                Apartments[vagrant.Maxxy()] = vagrant
            else:
                robApartment(Apartments,vagrant)



'''
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
'''






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


LCimg('test_img/riot.jpg')
