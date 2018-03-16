champion.js -> [getskinids.py] -> skinid.txt
skinid.txt  -> [crawler.py]    -> img/*.jpg
skinid.txt | img/*.jpg ->[SameImage.py]->sameskin.txt
sameskin.txt -> [select.py] -> MSImgid.txt
MSImgid.txt ->  [select.py] + [人工操作] ->select_img/;img_Pure/;
pureImgids.txt -> [SkinsAnalyse.py] -> pskindict.txt
pskindict.txt->[adjustpskd.py]-> pskindict_aj.txt
pskindict_aj.txt ->[localCompoundimg.py]->imgshow!
