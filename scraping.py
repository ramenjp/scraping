import csv
import time
import urllib
import requests
from bs4 import BeautifulSoup as bs4
import openpyxl

with open('../ぐるたびスクレイピング結果.csv','w') as f:
    writer = csv.writer(f)


for i in range(1,48):
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
    print(prefecture_name)
    # 地域名取得
    if prefecture_name == "北海道":
        area_name = "北海道"
    elif prefecture_name == "沖縄県":
        area_name = "沖縄県"
    else:
        area_name = pref_soup.find_all("ol",class_="breadcrumb__list")[0].find_all("a")[1].text
        print(area_name)
        print("--------------------------------------------------")

    # 各都道府県のページから「エリアごとの人気スポット欄」　のURLをリストで取得
    if pref_soup.find("div",class_="top-area-list-group-thum") != None:
        area_links = ["https:" + link['href'] for div in pref_soup.find_all("div",class_="top-area-list-group-thum") for link in div.find_all('a')]
    else:
        area_links = ["https:" + link['href'] for div in pref_soup.find_all("ul",class_="btn-link-list") for link in div.find_all('a')]
    # print(area_links)
    print("----------------------------------------------------------------------------------------------------------")
    for favorite_spot_url in area_links:
        # 「エリアごとの人気スポット欄」のリストから１つずつ取り出して解析
        r2 = requests.get(favorite_spot_url)
        areas_soup = bs4(r2.content, "html.parser")
        # 人気スポットページの記事のURLをすべて取得
        articles_url_list = ["https:" + link['href'] for div in areas_soup.find_all("div",class_="btn-container",limit=1) for link in div.find_all('a')]
        # print("エリアの記事一覧url")
        # print(articles_url_list)
        r_article_list = requests.get(articles_url_list[0])
        article_list_soup = bs4(r_article_list.content, "html.parser")
        if article_list_soup.find("p",class_="main-content__outline") != None:
            article_num_description = article_list_soup.find("p",class_="main-content__outline").text
            print(article_num_description)
            article_num = article_num_description[article_num_description.find("記事が")+3:article_num_description.find("件")]
            print(article_num)
            try: # 旅行ガイド記事のないエリアは例外としてpassする
                if int(article_num) > 30:
                    page_num = int(int(article_num)/30) + 1
                    i = 2
                    while i <= page_num:
                        articles_url_list.append(articles_url_list[0]+"pg"+str(i))
                        i = i +1
                # print(articles_url_list)
                print("-----------------------------------------------------------------------------------------------------")
                # 人気スポットページの記事のURLをすべて取得
                for articles_url in articles_url_list:
                    r_article_url = requests.get(articles_url)
                    article_soup = bs4(r_article_url.content, "html.parser")
                    article_url_list = ["https:" + link['href'] for div in article_soup.find_all("div",class_="panel") for link in div.find_all('a')]
                    # print("人気スポットのURL一覧")
                    # print(article_url_list)
                    # print("-----------------------------------------------------------------------------------------------------")
                    # 記事からタイトルと内容をスクレイピング
                    # for article_link in article_url_list:
                    #     r3 = requests.get(article_link)
                    #     soup3 = bs4(r3.content, "html.parser")
                    #     article_title = soup3.find("h1" ,class_="article-title")
                    #     print("【タイトル】"+article_title.text)
                    #     for article in soup3.find_all(class_=["article__description--head","article__description"]):
                    #         print(article.text)
                    #         # writer.writerow(area_name,prefecture_name,article_title.text,article.text)
                    #     print("-----------------------------------------------------------------------------------------------")
            except:
                pass