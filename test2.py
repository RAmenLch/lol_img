import numpy as np
import cv2


class ttt():
    def __init__(self,A):
        self.A = A


t = []
for i in range(10):
    t.append(ttt(i))
for i in t:
    i.A = 233

for i in t:
    print(i.A)
