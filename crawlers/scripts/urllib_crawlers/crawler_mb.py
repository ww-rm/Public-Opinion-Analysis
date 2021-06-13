# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tqdm import tqdm


class Crawler():
    def __init__(self, globle_config):
        self.config = globle_config
        self.ua = UserAgent().random
        self.headers = ("User-Agent", self.ua)
        self.opener = urllib.request.build_opener()
        self.opener.addheaders = [self.headers]

    def crawl_search(self, num, main_key_words, additional_key_words='', count=100):
        flag = 0
        max_page = 3
        all_news = []
        news_urls = []
        page = 1
        if additional_key_words == '':
            real_key_word = main_key_words.replace(" ", "%20")
        else:
            real_key_word = (main_key_words+" " +
                             additional_key_words).replace(" ", "%20")
        search_url = "https://mb.com.ph/page/"+str(page)+"/?s=" + real_key_word
        print("搜索关键词为："+str((main_key_words+" " +
                             additional_key_words))+"，目标数目为："+str(num))
        while not flag:
            try:
                data = self.opener.open(search_url).read()
                soup_data = BeautifulSoup(data, features="lxml")
                flag = 1
            except Exception:
                self.__init__(self.config)
        while len(news_urls) < num and page <= max_page:
            try:
                search_url = "https://mb.com.ph/page/" + \
                    str(page)+"/?s=" + real_key_word
                data = self.opener.open(search_url).read()
                soup_data = BeautifulSoup(data, features="lxml")
                for news in soup_data.find_all(class_="article"):
                    news_urls.append(
                        news.find(class_="title").find(name="a").get("href"))
                print("遍历第"+str(page)+"页，已爬取"+str(len(news_urls))+"/"+str(num))
                page += 1
                max_page += 1
            except Exception:
                max_page -= 1
        if len(news_urls) < num:
            print("可爬取数量不足目标数量")
        print("爬取url完成，爬取"+str(len(news_urls))+"/"+str(num))
        print("开始爬取内容新闻：")
        for url in tqdm(news_urls):
            try:
                news = self.crawl_news(url)
                news["MainKeyWord"] = main_key_words
                news["AdditionalKeyWord"] = additional_key_words
                all_news.append(news)
            except Exception:
                pass
        return all_news

    def crawl_news(self, url):
        data = self.opener.open(url).read()
        soup_data = BeautifulSoup(data, features="lxml")
        artical = ""
        for p in soup_data.find(class_="article-content").find_all(name="p"):
            artical += p.text
        title = soup_data.title.string
        time = url[18:28].replace("/", "-")
        tmp = {
            "Type": "",
            "Time": time,
            "Headline": title,
            "Text": artical,
            "Section": "",
            "Writers": "",
            "URL": url,
            "MainKeyWord": "",
            "AdditionalKeyWord": "",
            "Source": "MB"
        }
        return tmp
