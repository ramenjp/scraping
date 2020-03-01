import csv
import requests
from bs4 import BeautifulSoup as bs4
def writecsv(result_list):
    with open('../ぐるたびスクレイピング結果.csv','a', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(result_list)

for i in range(1,48):
    if i<10:
        prefectureNum = "0"+str(i)
    else:
        prefectureNum = str(i)
    # トップページから県ごとのURLを取得してbase_urlに格納
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

    # 各都道府県のページから「エリアごとの人気スポット欄」　のURLをリストで取得 ex.札幌、函館....etc
    # top-area-list-group-thumクラスから取得する県（北海道、沖縄）
    if pref_soup.find("div",class_="top-area-list-group-thum") != None:
        area_links = ["https:" + link['href'] for div in pref_soup.find_all("div",class_="top-area-list-group-thum") for link in div.find_all('a')]
    #tn-link-listクラスから取得する県（ex.青森、宮城...etc）
    else:
        area_links = ["https:" + link['href'] for div in pref_soup.find_all("ul",class_="btn-link-list") for link in div.find_all('a')]
    print("----------------------------------------------------------------------------------------------------------")
    for favorite_spot_url in area_links:
        # 「エリアごとの人気スポット欄」から１つずつ取り出して解析
        r2 = requests.get(favorite_spot_url)
        areas_soup = bs4(r2.content, "html.parser")

        # 詳細エリア名取得(ex.日光・鬼怒川)
        detail_area_name = areas_soup.find("h1", class_="area-top-header__ttl").text
        detail_area_name = detail_area_name[:detail_area_name.find("の")]
        # 「エリアごとの人気スポット」ページの記事一覧のURL取得
        articles_url_list = ["https:" + link['href'] for div in areas_soup.find_all("div",class_="btn-container",limit=1) for link in div.find_all('a')]
        # print("「エリアごとの人気スポット」の記事一覧URL")
        # print(articles_url_list)
        r_article_list = requests.get(articles_url_list[0])
        article_list_soup = bs4(r_article_list.content, "html.parser")

        # 記事がないエリアを対象外に
        if article_list_soup.find("p",class_="main-content__outline") != None:
            article_text = " "
            article_num_description = article_list_soup.find("p",class_="main-content__outline").text

            # 「記」という文字から＋３文字～「件」という文字までを取得することで、文章中から記事数を取得＆整数化
            article_num = int(article_num_description[article_num_description.find("記事が")+3:article_num_description.find("件")])
            # print(article_num)
            try: # 旅行ガイド記事のないエリアは例外としてpassする
                if article_num > 30:
                    # ページ数計算
                    page_num = int(article_num/30) + 1
                    j = 2
                    # 複数ページある場合は記事一覧のURLに２ページ目以降を追加
                    while j <= page_num:
                        articles_url_list.append(articles_url_list[0]+"pg"+str(j))
                        j = j +1
                # 人気スポットページの記事のURLをすべて取得
                for articles_url in articles_url_list:
                    r_article_url = requests.get(articles_url)
                    article_soup = bs4(r_article_url.content, "html.parser")
                    article_url_list = ["https:" + link['href'] for div in article_soup.find_all("div",class_="panel") for link in div.find_all('a')]
                    # print("-----------------------------------------------------------------------------------------------------")
                    # 記事からタイトルと内容をスクレイピング
                    for article_link in article_url_list:
                        r3 = requests.get(article_link)
                        soup3 = bs4(r3.content, "html.parser")
                        # 記事タイトル取得
                        article_title = soup3.find("h1" ,class_="article-title")
                        article_title = article_title.text.strip().strip("\n")
                        # print("【タイトル】"+article_title)
                        #記事内容取得
                        article_result = []
                        for article in soup3.find_all(class_=["article__description--head","article__description"]):
                            article_result.append(article.text.strip("\n"))
                        article_text = ''.join(article_result).strip().strip("\n")
                        result_list = [area_name,prefecture_name,detail_area_name,article_title,article_text,article_link]
                        writecsv(result_list)
            except:
                pass