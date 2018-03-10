from localCompoundimg import SkinData,getSkinData
def aj():
    skds = getSkinData()
    for i in range(5):
        skds.sort(key = lambda x:x.data[i])
        min = skds[0].data[i]
        max = skds[-1].data[i]
        for skd in skds:
            skd.data[i] = int(((skd.data[i] - min) / (max - min)) *255)
    for skd_aj in skds:
        with open('pskindict_aj.txt','a') as file:
            file.write(str(skd_aj) + '\n')

aj()
