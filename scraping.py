import csv
import time
import urllib
import requests
from bs4 import BeautifulSoup as bs4
import openpyxl

wb = openpyxl.load_workbook('../ぐるたびスクレイピング結果.xlsx')

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

    # 各県のページから「エリアごとの人気スポット欄」　のURLをリストで取得
    area_links = ["https:" + link['href'] for div in soup.find_all("div",class_="top-area-list-group-thum") for link in div.find_all('a')]
    for link in area_links:
        # 「エリアごとの人気スポット欄」のリストから１つずつ取り出して解析
        favorite_spot_url = link
        r2 = requests.get(favorite_spot_url)
        soup2 = bs4(r2.content, "html.parser")
        # 人気スポットページの記事のURLをすべて取得
        article_url_list = ["https:" + link['href'] for div in soup.find_all("div",class_="panel") for link in div.find_all('a')]
        print("人気スポットのURL一覧")
        print(article_url_list)
        print("--------------------------------------------------")
        print("記事タイトル")
    #     記事からタイトルと内容をスクレイピング
        for article_link in article_url_list:
            r3 = requests.get(article_link)
            soup3 = bs4(r3.content, "html.parser")
            article_title = soup3.find("h1" ,class_="article-title")
            print(article_title.text)