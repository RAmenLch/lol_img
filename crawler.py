import requests
import time
hurl = 'http://ossweb-img.qq.com/images/lol/web201310/skin/big'
def getids():
    ids = []
    with open('skinid.txt','r') as file:
        data =  file.read();
    ids = data.split(',')
    return ids

def main():
    ids = getids()
    for i in ids:
        try:
            url = hurl + i + '.jpg'
            html = requests.get(url)
            html.raise_for_status()
            time.sleep(0.2)
            with open('img/' + i + '.jpg', 'wb') as file:
                file.write(html.content)
        except Exception as e:
            print(e)
main()
