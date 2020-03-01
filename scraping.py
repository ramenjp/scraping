import csv
import time
import urllib
import requests
from bs4 import BeautifulSoup as bs4
import openpyxl

# with open('../ぐるたびスクレイピング結果.csv') as f:
#     f.read()

# layer1[] トップページの地方
# layer2[]　地方ページの「エリアごとの人気スポット欄」　
# layer3[]　エリアごとのスポットからの記事一覧

for i in range(1,2):
    if i<10:
        prefectureNum = "0"+str(i)
    else:
        prefectureNum = str(i)
    # トップページから県ごとのURLを取得
    base_url = "http://gurutabi.gnavi.co.jp/p{}/".format(prefectureNum)
    r = requests.get(base_url)
    soup = bs4(r.content, "html.parser")

    # 県名取得
    prefecture_name = soup.find("h1",class_="area-top-header__ttl").text
    prefecture_name = prefecture_name[:prefecture_name.find("の")]

    # 地域名取得
    if prefecture_name == "北海道":
        area_name = "北海道"
    elif prefecture_name == "沖縄":
        area_name = "沖縄"
    else:
        area_name = soup.find("ol",class_="breadcrumb__list").find_all("a").text
        print(area_name[1])
        print("--------------------------------------------------")

    # 各県のページから「エリアごとの人気スポット欄」　のURLをリストで取得
    area_links = ["https:" + link['href'] for div in soup.find_all("div",class_="top-area-list-group-thum") for link in div.find_all('a')]
    print(area_links)
    print("----------------------------------------------------------------------------------------------------------")
    for favorite_spot_url in area_links:
        # 「エリアごとの人気スポット欄」のリストから１つずつ取り出して解析
        r2 = requests.get(favorite_spot_url)
        soup2 = bs4(r2.content, "html.parser")
        # 人気スポットページの記事のURLをすべて取得
        article_url_list = ["https:" + link['href'] for div in soup2.find_all("div",class_="panel") for link in div.find_all('a')]
        print("人気スポットのURL一覧")
        print(article_url_list)
        print("-----------------------------------------------------------------------------------------------------")
        # 記事からタイトルと内容をスクレイピング
        for article_link in article_url_list:
            r3 = requests.get(article_link)
            soup3 = bs4(r3.content, "html.parser")
            article_title = soup3.find("h1" ,class_="article-title")
            print("【タイトル】"+article_title.text)
            for article in soup3.find_all(class_=["article__description--head","article__description"]):
             print(article.text)
            print("-----------------------------------------------------------------------------------------------")
