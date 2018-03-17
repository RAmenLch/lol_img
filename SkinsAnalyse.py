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


解决:adjust()
    由于'选用图片'的灰度值区间为[0,255] 而'皮肤插画'的灰度值区间为[min,max],min>0,max<255
    故在拟合'选用图片'和'皮肤插画'后并不真实
    使用adjust()调整数据并将数据保存在pskindict_aj.txt
    添加一个Skin_Id_Data类,储存并使用皮肤插画的的灰度值信息



'''
def cutStick(img):
    A = np.mean(img)
    B = np.median(img)
    for i in img:
        for j in i:
            if abs(j - A) >80 and abs(j - B) >100:
                j -= (j-A)/2
    return img
def to22(img):
    len1 = int(len(img[0])/2)
    A = np.mean(          cutStick(img[:len1,:len1]) )
    AA = np.mean(         cutStick(img[:len1,len1:]) )
    AAA = np.mean(        cutStick(img[len1:,:len1]) )
    AAAA = np.mean(       cutStick(img[len1:,len1:]) )
    return np.array([[A,AA],[AAA,AAAA]])





def getPureSkinFileName():
    with open('pureImgids.txt','r') as file:
        strids = file.read()
    fNames = strids[1:-1].split(',')
    return fNames


def analyseSkin(size = (2,2)):
    with open('pskindict.txt','w') as file:
        file.write('')
    fns = getPureSkinFileName()
    for i in fns:
        img = cv2.imread('img_Pure/' + i, cv2.IMREAD_GRAYSCALE)
        #img = cv2.resize(img,size,cv2.INTER_AREA)
        img = to22(img)
#        print(img)
        with open('pskindict.txt','a') as file:
            file.write(i + ':')
            for i in range(2):
                for j in range(2):
                    file.write(str(img[i][j]) + ',')
            file.write(str(np.mean(img)) + '\n')


#参数:id:图片文件名;data = ['左上平均灰度','右上平均灰度','左下平均灰度','右下平均灰度','整体平均灰度']
class Skin_Id_Data():
    def __init__(self,id,data):
        self.id = id
        self.data = data
        #保存'选用图片'的像素坐标列表,排序为拟合程度从小到大,第一个参数是像素坐标,第二个参数是拟合程度
    def __str__(self):
        return  self.id + ':' + str(self.data)[1:-1]

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
            skdata.append(Skin_Id_Data(id,data))
    return skdata


#调整：将data的上下界[min,max]全部转换为[0,255]
def adjust():
    skds = getSkinData('pskindict.txt')
    for i in range(5):
        skds.sort(key = lambda x:x.data[i])
        min = skds[0].data[i]
        max = skds[-1].data[i]
        for skd in skds:
            #核心
            skd.data[i] = int(((skd.data[i] - min) / (max - min)) *255)
    with open('pskindict_aj.txt','w') as file:
        file.write('')
    for skd_aj in skds:
        #保存为转换完的数据
        with open('pskindict_aj.txt','a') as file:
            file.write(str(skd_aj) + '\n')


if __name__ == '__main__':
    analyseSkin()
    adjust()
