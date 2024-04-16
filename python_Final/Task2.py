import urllib.request as req
import csv
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))# 獲取當前腳本的目錄

# 定義CSV檔的完整路徑
article_csv_path = os.path.join(script_dir, "article.csv")


def MyCrawler(url):
    def crawlerTime(url):
        request=req.Request(url,headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data=response.read().decode("utf-8")

        root=bs4.BeautifulSoup(data,"html.parser")
        time_tag=root.find("span",class_="article-meta-tag",string="時間")
        if time_tag:
            next_sibling = time_tag.find_next_sibling().string
            # print(next_sibling)
            return next_sibling
        else:
            return ""


    request=req.Request(url,headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        })

    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")

    import bs4
    root=bs4.BeautifulSoup(data,"html.parser")
    titles=root.find_all("div",class_="title")
    titles2=root.find_all("div",class_="nrec")

    mytitle=[]
    for title ,title2 in zip(titles,titles2):
        if title.a !=None:
            # mydic[title.a.string]=[title2.string,]
            myhre="https://www.ptt.cc"+title.a["href"]
            # print(myhre)
            if title2.string==None:
                title2.string="0"
            mytitle.append([title.a.string,str(title2.string),crawlerTime(myhre)])
            # mytitle.append(title.a.string+","+str(title2.string)+","+crawlerTime(myhre))
            # print(crawlerTime(myhre))
        else:
            cleanText=title.string.strip()
            mytitle.append([cleanText,"0",""])
            # mytitle.append(cleanText+","+"0"+"")
    pageURL=root.find("a",string="‹ 上頁")
    nextLink="https://www.ptt.cc"+pageURL["href"]

    return mytitle,nextLink   

url = "https://www.ptt.cc/bbs/Lottery/index.html"
mytitle=[]
count=0
while count<3:
    mycollection,url=MyCrawler(url)
    count+=1
    mytitle.extend(mycollection)

with open(article_csv_path, "w", newline="") as csvfile:
    csvData = csv.writer(csvfile)
    for itm in mytitle:
        csvData.writerow(itm)




