import cv2
import numpy as np

img = cv2.imread('test_img/test2.jpg', cv2.IMREAD_GRAYSCALE)
img_r = cv2.resize(img,(29,29))
print(img_r)
