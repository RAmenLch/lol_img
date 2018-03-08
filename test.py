import dhash
import phash
from PIL import Image
import datetime


'''
im1 = Image.open("2004.jpg")
im2 = Image.open("30004.jpg")
im3 = Image.open("37002.jpg")
im4 = Image.open("82003.jpg")
im5 = Image.open("83002.jpg")
im6 = Image.open("254011.jpg")
imT = im5 = Image.open("83002(T).jpg")
a = dhash.classfiy_dHash(im1,im2)
b = phash.classify_DCT(im1,im2)
c = phash.classify_DCT(im1,im3)

d = phash.classify_DCT(im1,im4)
e = phash.classify_DCT(im1,im5)
f = dhash.classfiy_dHash(im1,im5)
T = phash.classify_DCT(im1,imT)
ET = phash.classify_DCT(im5,imT)

g =  phash.classify_DCT(im1,im6)
h = dhash.classfiy_dHash(im1,im6)

print(d,e,f,T,ET)
'''
starttime = datetime.datetime.now()



XX = Image.open("XX.jpg")
XX2 = Image.open("XX2.jpg")
V = Image.open("V.jpg")
N = Image.open("ni.jpg")
xx2xxd = dhash.classfiy_dHash(XX2,N)
xx2xx = phash.classify_DCT(XX2,N,size = (96,96),part_size=(8,8))
print(xx2xxd,xx2xx)

#long running

endtime = datetime.datetime.now()
print(endtime - starttime)
