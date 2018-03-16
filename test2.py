import numpy as np
import cv2

def getidarray(str1 = 'sameskin.txt'):
    idsar = []
    with open(str1,'r') as file:
        while 1:
            STR = file.readline()
            if not STR:
                break
            ids = STR[1:-3].split(', ')
            idsar.append(ids)
    return idsar
print(len(getidarray()))
