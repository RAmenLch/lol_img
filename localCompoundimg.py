import cv2
import numpy as np
from SkinsAnalyse import Skin_Id_Data


'''
利用本地的图片来合成想要的图像
输入:
    pskindict_aj.txt
    img_Pure/
    想要被合成的图片.jpg
输出:
    getNewImg()输出的图片

'''
class SkinData(Skin_Id_Data):
    def __init__(self,id,data):
        super().__init__(id,data)
        #保存'选用图片'的像素坐标列表,排序为拟合程度从小到大,第一个参数是像素坐标,第二个参数是拟合程度
        self.xystack = [(-1,0)]
    #输出data和self.data的拟合程度:100/(边角灰度值的1-范数*权 +平均灰度值的1-范数*权)
    def DegreeOfComparability(self,data):
        degree = 0;
        for i in range(4):
            degree += abs(data[i] - self.data[i])
        degree = degree*2 + abs(data[4] - self.data[4])*1
        return 100/(degree + 1)
    #遍历添加像素点坐标和与其的拟合程度,排序为拟合程度从小到大
    def pushAutoFitXY(self,xy,degree):
        self.xystack.append((xy,degree))
        self.xystack.sort(key=lambda x:x[1])
    #将最适合的像素点删除(因为这个像素点有更适合的图片呢)
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


def getSkinData(txtname):
    skdata = []
    with open(txtname,'r') as file:
        while 1:
            strdict = file.readline()
            if not strdict:
                break
            id,data = strdict.split(':')
            data = data[:-1].split(',')
            #批量转换类型
            data = list(map(float,data))
            skdata.append(SkinData(id,data))
    return skdata



#自称:快占茅坑算法(误 多快好省的让公寓住着最适合的人算法(逃
def optimalSolution(datas,n):
    #先来个公寓
    Apartments = {}
    #这是避免算法错误用的透明图层
    fuck = SkinData('test1.jpg',[0,0,0,0])
    #调整过的皮肤资料
    skdata = getSkinData('pskindict_aj.txt')
    #先让人对房子进行评价
    for skd in skdata:
        #对房子进行评价
        for k in range(n*n):
            #评价函数
            doc = skd.DegreeOfComparability(datas[k])
            #如果房子没住人,大胆把房间号写到小本本里
            if not k in Apartments:
                skd.pushAutoFitXY(k,doc)
            else:
                #如果这个房子你比他更适合住,就写到小本本里
                if Apartments[k].MaxDegree() < skd.MaxDegree():
                    skd.pushAutoFitXY(k,doc)
        #如果这个人最适合的房子没人住,直接入住
        if not skd.Maxxy() in Apartments:
            Apartments[skd.Maxxy()] = skd
        else:
            #否则,赶走房子里面的人,叫他去[抢房子],然后入住
            robApartment(Apartments,Apartments[skd.Maxxy()])
            Apartments[skd.Maxxy()] = skd
    #所有人搞定后,将公寓住的人保存在ids中
    ids = []
    for k in range(n*n):
        ids.append(Apartments.get(k, fuck).id)
    return ids


#被赶出来的人抢房子函数(公寓表,流离失所的人)
def robApartment(Apartments,vagrant):
    #首先把最适合自己的房子从小本本上删了,如果返回F就是真的变成流浪汉了
    if vagrant.popAutoFitXY():
        #现在的最适合的房子如果没有房客,就直接入住
        if not vagrant.Maxxy() in Apartments:
            Apartments[vagrant.Maxxy()] = vagrant
            return
        else:
            #否则判断自己与这个房客对这个房子的适合程度,如果胜利
            if Apartments[vagrant.Maxxy()].MaxDegree() < vagrant.MaxDegree():
                #则赶走房子里面的人,叫他去[抢房子],然后入住
                robApartment(Apartments,Apartments[vagrant.Maxxy()])
                Apartments[vagrant.Maxxy()] = vagrant
            else:
                #否则重新抢房子,直到找到房子或成为流浪汉
                robApartment(Apartments,vagrant)


#合成图片主函数('合成源图片位置',使用N*N张图片合成)
#max_size = 29
def LCimg(imgPath,N = 29):
    #读取
    img = cv2.imread(imgPath)
    #缩小
    img_r = cv2.resize(img,(N*2,N*2))
    #灰度
    img_g = cv2.cvtColor(img_r,cv2.COLOR_BGR2GRAY)
    cv2.imshow('',img)
    cv2.waitKey()
    #收集数据和pskindict_aj.txt中data配对
    datalist = []
    for i in range(0,N*2,2):
        for j in range(0,N*2,2):
            #对于四个角的灰度
            data = np.array([img_g[i][j],img_g[i][j+1],img_g[i+1][j],img_g[i+1][j+1]])
            #对应平均值的灰度
            data = np.append(data,np.mean(data))
            datalist.append(data)
    #计算数据,返回配对成功的文件名列表
    ids = optimalSolution(datalist,N)
    getNewImg(ids,N)


#####!!
#拼合图像
def getNewImg(ids,n):
    listi = []
    for i in range(n):
        listj = []
        for j in range(n):
            #将一维的列表折成二维
            id = ids[i*n + j]
            img = cv2.imread('img_Pure/' + id)
            img_r = cv2.resize(img,(33,17))
            listj.append(img_r)
        listi.append(listj)
    A = True
    for i in listi:
        #横向拼合
        imageQAQ = np.hstack(i)
        if A:
            imageTAT = imageQAQ
            A = False
        else:
            #纵向拼合
            imageTAT = np.vstack((imageTAT,imageQAQ))
    #imageTAT = cv2.cvtColor(imageTAT,cv2.COLOR_BGR2GRAY)
    #展示图像
    cv2.imshow('',imageTAT)
    cv2.waitKey()


LCimg('test_img/riot1.jpg')
