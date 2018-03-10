import numpy as np
import cv2


im = cv2.imread('test_img/test1.jpg',cv2.COLOR_BGR2GRAY)
im = cv2.resize(im,(8,8))
print(im)
