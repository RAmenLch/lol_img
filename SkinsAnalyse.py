import cv2
import numpy as np

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
