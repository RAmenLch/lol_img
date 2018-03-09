from PIL import Image
import os
SUM = 137

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

def  mergeSameImgSet():
    idsar = getidarray()
    delSet = set()
    for i in range(SUM):
        if i in delSet:
            continue
        setTemp1 = set(idsar[i])
        delSet.add(i)

        flag = True
        while flag == True:
            flag = False
            for j in range(SUM):
                if j in delSet:
                    continue
                setTemp2 = set(idsar[j])
                if setTemp1 & setTemp2 != set():
                    setTemp1 = setTemp1 | setTemp2
                    delSet.add(j)
                    flag = True
        with open('MSImgid.txt','a') as file:
            file.write(str(setTemp1) + ';\n')
    print(delSet)

#mergeSameImgSet()

def saveSameImg():
    idsar = getidarray('MSImgid.txt')
    for i in idsar:
        os.mkdir('select_img/' + i[0])
        for j in i:
            with Image.open('img/' + j + '.jpg') as img:
                img.save('select_img/' + i[0] + '/' + j + '.jpg')

def delImgToPure():
    idsar = getidarray('MSImgid.txt')
    for i in idsar:
        for j in i:
            os.remove('img_Pure/' + j + '.jpg')
            print('remove' + j)

def savePureImgids():
    file_dir = 'img_Pure'
    for root, dirs, files in os.walk(file_dir):
        strids = str(files).replace('\'','').replace(' ', '')
    with open('pureImgids.txt','w') as file:
        file.write(strids)
