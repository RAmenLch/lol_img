import numpy as np
import cv2


img = cv2.imread('test_img/test1.jpg')
img_r = cv2.resize(img,(64,64))
imgA = np.vstack((img_r, img_r))
imgB =  np.vstack((imgA, img_r))
#imgB = np.concatenate([img_r, img_r], axis=1)

cv2.imshow('fuck',imgB)
cv2.waitKey()
