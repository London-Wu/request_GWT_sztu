#爬公文通2.0 对文章及文章选择器进行对象化
#已具备基本接口，便于后续开发

import requests
from bs4 import BeautifulSoup
import os

class Articals_chooser: #文章选择器类
    def __init__(self, page_num=1):
        self.articles = []

        self.page_num = page_num #页码
        main_page_url = f"http://nbw.sztu.edu.cn/list.jsp?PAGENUM={self.page_num}&urltype=tree.TreeTempUrl&wbtreeid=1029" #带页码参数的url
        main_page_acceptance = requests.get(main_page_url) #发出请求
        main_page_soup = BeautifulSoup(main_page_acceptance.text, 'html.parser') #soup对象化html

        main_structure = main_page_soup.find("ul",class_="news-ul")
        articles_source = main_structure.find_all("li", class_ = "clearfix")
        for article_source in articles_source:
            article_category = article_source.find("div", class_="width02").find("a").string  # 寻找类别
            article_author = article_source.find("div", class_="width03").find("a").string # 寻找作者
            article_title = article_source.find("div",  class_="width04").find("a").string #寻找标题
            article_ori_url = article_source.find("div",  class_="width04").find("a")["href"]  # 寻找url
            article_posted_date = article_source.find("div",  class_="width06").string  # 寻找发布日期
            article_url = f"http://nbw.sztu.edu.cn/{article_ori_url}"
            self.articles.append(Article(article_title, article_url, article_category, article_author, article_posted_date))

class Article: #文章类
    def __init__(self, title, url, category, author, posted_date):
        self.title = title
        self.url = url
        self.category = category
        self.author = author
        self.posted_date = posted_date

        #收集文章内容
        article_page_acceptance = requests.get(self.url)
        article_page_acceptance.encoding = "utf-8"
        article_page_soup = BeautifulSoup(article_page_acceptance.text, "html.parser")
        article_neirong = article_page_soup.find("div", class_="neirong")
        self.head_text = article_neirong.find("div", class_="article-sm").string
        self.detail_text = article_neirong.find("div", class_="v_news_content").text

        #收集附件链接
        self.appendix = []
        if article_neirong.find("ul", class_="fujian") != None:
            appendixes_source = article_neirong.find("ul", class_="fujian").find_all("li")
            for appendix_source in appendixes_source:
                appendix_ori_url = appendix_source.find("a")["href"]
                appendix_url = f"http://nbw.sztu.edu.cn/{appendix_ori_url}"
                self.appendix.append(appendix_url)

if __name__ == "__main__":
    print("深圳技术大学公文通:")
    print("当前排序：最新文章")
    print("正在获取公文通文章...")
    articles = Articals_chooser()
    num = 0
    print("序号\t标题\t类别\t作者\t日期")
    for article in articles.articles:
        num+=1
        print(f"{num}\t{article.title}\t{article.category}\t{article.author}\t{article.posted_date}")
    input_num = int(input("请输入要查看内容的文章序号："))
    print(articles.articles[input_num-1].detail_text)