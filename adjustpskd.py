'''
本模块:解决:实际的灰度值并不完美,需要经过调整的问题
            由于'选用图片'的灰度值区间为[0,255] 而'皮肤插画'的灰度值区间为[min,max],min>0,max<255
            故在拟合'选用图片'和'皮肤插画'后并不真实
        添加一个SkinData类,储存并使用皮肤插画的的灰度值信息
        添加一个getSkinData函数,取出'pskindict.txt'(包括调整前,调整后)文件,并生成一个SkinData实例列表
'''


#参数:id:图片文件名;data = ['左上平均灰度','右上平均灰度','左下平均灰度','右下平均灰度','整体平均灰度']
class SkinData():
    def __init__(self,id,data):
        self.id = id
        self.data = data
        #保存'选用图片'的像素坐标列表,排序为拟合程度从小到大,第一个参数是像素坐标,第二个参数是拟合程度
        self.xystack = [(-1,0)]
    #输出data和self.data的拟合程度:100/(边角灰度值的1-范数*权 +平均灰度值的1-范数*权)
    def DegreeOfComparability(self,data):
        degree = 0;
        for i in range(4):
            degree += abs(data[i] - self.data[i])
        degree = degree*2 + abs(data[4] - self.data[4])*1
        return 100/(degree + 1)
    def __str__(self):
        return  self.id + ':' + str(self.data)[1:-1]
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







#调整：将data的上下界[min,max]全部转换为[0,255]
def aj():
    skds = getSkinData('pskindict.txt')
    for i in range(5):
        skds.sort(key = lambda x:x.data[i])
        min = skds[0].data[i]
        max = skds[-1].data[i]
        for skd in skds:
            #核心
            skd.data[i] = int(((skd.data[i] - min) / (max - min)) *255)
    for skd_aj in skds:
        #保存为转换完的数据
        with open('pskindict_aj.txt','a') as file:
            file.write(str(skd_aj) + '\n')

aj()
