from SkinsAnalyse import getPureSkinFileName
import os
import cv2


def resizeImg(size = (33,17)):
    ids = getPureSkinFileName()
    for id in ids:
        img = cv2.imread('img_Pure/' + id)
        img_r = cv2.resize(img,size)
        if not os.path.exists('img_Pure_resize'):
            os.mkdir('img_Pure_resize')
        cv2.imwrite('img_Pure_resize/' + id, img_r)

if __name__ == '__main__':
    resizeImg()
