import nphash
from PIL import Image
import cv2

SUM = 964
def getids():
        ids = []
        with open('skinid.txt','r') as file:
            data =  file.read();
        ids = data.split(',')
        return ids
def main():
    ids = getids()
    setSameSkin = set([])
    for i in range(SUM):
        c = 0
        if int(ids[i])%1000 == 0:
            continue
        if ids[i] in setSameSkin:
            continue
        setSameSkin = setSameSkin | nphash.myclassify_gray_hist(ids,i)


#下一个目标,优化速度!


main()
