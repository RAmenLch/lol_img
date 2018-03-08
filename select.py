def getidarray():
    idsar = []
    with open('sameskin.txt','r') as file:
        while 1:
            STR = file.readline()
            if not STR:
                break
            ids = STR[1:-3].split(', ')
            idsar.append(ids)
    print(idsar)
getidarray()
test
