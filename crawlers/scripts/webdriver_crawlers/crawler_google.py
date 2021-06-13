import time
from tqdm import tqdm
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse as urlparser


class Crawler():
    def __init__(self, globle_config, local_config=None, location="Singapore"):
        # platform_ = platform.system()
        # self.browser = webdriver.Firefox()
        # if platform_ == "Windows":
        #     self.browser = webdriver.PhantomJS(
        #         globle_config["path"]["phantomjs_windows_path"])
        # elif platform_ == "Linux":
        #     print("不支持暂时")
        #     exit(-1)
        # elif platform_ == "Darwin":
        #     self.browser = webdriver.PhantomJS(
        #         globle_config["path"]["phantomjs_macos_path"])
        self.tmp_path = globle_config["path"]["tmp_path"]
        self.tmp_files = []
        self.target_url = "http://news.google.com/topstories?" + \
            globle_config["Google_Crawler"][location]
        self.time = time.strftime("%Y-%m-%d", time.gmtime())
        self.location = location

    def load_page(self, url, time=5):
        self.browser.set_page_load_timeout(time)
        self.browser.set_script_timeout(time)
        try:
            self.browser.get(url)
        except Exception:
            # 执行js脚本

            pass

    def crawl_urls(self):
        response = urllib.request.urlopen(self.target_url)
        html = response.read()
        urls = []
        articles = None
        url_more_headlines = BeautifulSoup(html).find(
            text="More Headlines").parent.get("href")
        response = urllib.request.urlopen(
            urlparser.urljoin(response.url, url_more_headlines))
        html = response.read()
        articles = BeautifulSoup(html).find_all("article")
        print("开始爬取urls")
        for article in tqdm(articles):
            url = urlparser.urljoin(response.url, "."+article.a["href"])
            # print(url)
            try:
                url = self.get_real_url(url)
                urls.append(url)
            except Exception:
                pass
        return urls

    def get_articles(self, urls):
        news = []
        print("开始爬取文章")
        for url in tqdm(urls):
            try:
                tmp, status = self.crawl_single_page_default(url)
                if not status:
                    continue
                news.append(tmp)
            except Exception:
                pass
        return news

    def get_real_url(self, url):
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, features="html.parser")
        noscript = soup.find("noscript").find("a", href=True)
        url_1 = noscript["href"]
        return url_1

    def www_channelnewsasia_com(self, url):
        status = 1
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, features="html.parser")
        article = soup.find("article")
        type_ = (
            article.find("header")
            .find("span", {"class": "article__category"})
            .get_text(strip=True)
        )
        title = article.find("h1").get_text(strip=True)
        text = "".join([
            p.get_text(strip=True)
            for p in article.find_all("p")
        ])
        KeyWords = ",".join([
            li.get_text(strip=True)
            for li in article.find("footer").find("ul").find_all("li")
        ])
        tmp = {
            "Type": type_,
            "Time": self.time,
            "Headline": title,
            "Text": text,
            "Section": "",
            "Writers": "",
            "URL": url,
            "MainKeyWord": KeyWords,
            "AdditionalKeyWord": "",
            "Source": "google-"+self.location
        }
        return tmp, status

    def crawl_single_page_default(self, url):
        tmp = {
            "Type": "",
            "Time": self.time,
            "Headline": "",
            "Text": "",
            "Section": "",
            "Writers": "",
            "URL": url,
            "MainKeyWord": "",
            "AdditionalKeyWord": "",
            "Source": "google-"+self.location
        }
        status = 1
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, features="html.parser")
        text = ""
        ps = soup.find_all("p")
        for p in ps:
            text += p.text
        if text == "":
            status = 0
        tmp["Headline"] = soup.title.string
        return tmp, status

    def clean_tmp(self):
        if len(self.tmp_files) == 0:
            pass
        else:
            for tmp_file in self.tmp_files:
                import os
                os.remove(self.tmp_path + tmp_file)
