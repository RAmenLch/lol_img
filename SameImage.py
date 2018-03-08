import nphash
from PIL import Image
import cv2
import datetime

SUM = 964
def getids():
        ids = []
        with open('skinid.txt','r') as file:
            data =  file.read();
        ids = data.split(',')
        return ids
def main():
    ids = getids()
    for i in range(SUM):
    #    timeA = datetime.datetime.now()
        flag = False
        if int(ids[i])%1000 == 0:
            continue
        print(ids[i])
        im1 = cv2.imread('img/' + ids[i] + '.jpg')
        setSameSkinTemp = set()
        for j in range(i + 1,SUM):
            if int(ids[j])%1000 == 0:
                continue
            elif abs(int(ids[j]) - int(ids[i])) <=20:
                continue
            else:
                im2 = cv2.imread('img/' + ids[j] + '.jpg')
                Hdis = nphash.classify_hist_with_split(im1,im2)
                if Hdis >= 0.74 :
                    flag = True
                    print(' ' + ids[j] + '!!')
                    setSameSkinTemp.add(ids[j])
        if flag == True:
                setSameSkinTemp.add(ids[i])
                with open('sameskin.txt','a') as file :
                    file.write(str(setSameSkinTemp) + ';\n')
        #timeB = datetime.datetime.now()
        #print(timeB - timeA)




#下一个目标,优化速度!


main()
