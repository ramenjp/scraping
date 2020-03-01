import csv
import time
import urllib
import requests
from bs4 import BeautifulSoup as bs4
import openpyxl

with open('../ぐるたびスクレイピング結果.csv','w') as f:
    writer = csv.writer(f)



for i in range(1,6):
    if i<10:
        prefectureNum = "0"+str(i)
    else:
        prefectureNum = str(i)
    # トップページから県ごとのURLを取得
    base_url = "http://gurutabi.gnavi.co.jp/p{}/".format(prefectureNum)
    r = requests.get(base_url)
    pref_soup = bs4(r.content, "html.parser")

    # 県名取得
    prefecture_name = pref_soup.find("h1",class_="area-top-header__ttl").text
    prefecture_name = prefecture_name[:prefecture_name.find("の")]

    # 地域名取得
    if prefecture_name == "北海道":
        area_name = "北海道"
    elif prefecture_name == "沖縄":
        area_name = "沖縄"
    else:
        area_name = pref_soup.find("ol",class_="breadcrumb__list").find_all("a").text
        print(area_name[1])
        print("--------------------------------------------------")

    # 各県のページから「エリアごとの人気スポット欄」　のURLをリストで取得
    area_links = ["https:" + link['href'] for div in pref_soup.find_all("div",class_="top-area-list-group-thum") for link in div.find_all('a')]
    print(area_links)
    print("----------------------------------------------------------------------------------------------------------")
    for favorite_spot_url in area_links:
        # 「エリアごとの人気スポット欄」のリストから１つずつ取り出して解析
        r2 = requests.get(favorite_spot_url)
        areas_soup = bs4(r2.content, "html.parser")
        # 人気スポットページの記事のURLをすべて取得
        article_url_list = ["https:" + link['href'] for div in areas_soup.find_all("div",class_="btn-container",limit=1) for link in div.find_all('a')]
        print("エリアの記事一覧url")
        print(article_url_list)
        r_article_list = requests.get(article_url_list[0])
        article_list_soup = bs4(r_article_list.content, "html.parser")
        article_num_description = article_list_soup.find("p",class_="main-content__outline").text
        article_num = article_num_description[article_num_description.find("記事が")+3:article_num_description.find("件")]
        print(article_num)
        if int(article_num) > 30:
            page_num = int(int(article_num)/30) + 1
            i = 2
            while i <= page_num:
                article_url_list.append(article_url_list[0]+"pg"+str(i))
                i = i +1
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
             # writer.writerow(area_name,prefecture_name,article_title.text,article.text)

            print("-----------------------------------------------------------------------------------------------")
