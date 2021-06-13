import json
import re
import time
import urllib.parse as urlparser
from pathlib import Path
from pprint import pprint
from time import sleep
from warnings import warn

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class PageParser:
    """
    在这个类里面做不同域名的页面解析,
    对于写好的方法在 __init__ 里面的方法表上登记
    """

    def __init__(self):
        self.parse_method_table = {
            # "www.example.com": PageParser.method
            "www.channelnewsasia.com": self.www_channelnewsasia_com,
            "www.straitstimes.com": self.www_straitstimes_com

        }

    def __call__(self, domain, text) -> dict:
        parse_method = self.parse_method_table.get(domain)
        if not parse_method:
            # warn("没有用来解析域名 {} 页面的方法!".format(domain))
            parse_method = self.www_default_com

        try:
            return parse_method(text)
        except Exception:
            warn("页面内容解析失败: {}".format(domain))
            return {
                "Type": "",
                "Time": time.strftime("%Y-%m-%d", time.gmtime()),
                "Headline": "",
                "Text": "",
                "Section": "",
                "Writers": "",
                "URL": "",
                "MainKeyWord": "",
                "AdditionalKeyWord": ""
            }

    def www_default_com(self, text) -> dict:
        result = {
            "Type": "",
            "Time": time.strftime("%Y-%m-%d", time.gmtime()),
            "Headline": "",
            "Text": "",
            "Section": "",
            "Writers": "",
            "URL": "",
            "MainKeyWord": "",
            "AdditionalKeyWord": ""
        }
        soup = BeautifulSoup(text, "lxml")
        text = ""
        ps = soup.find_all("p")
        for p in ps:
            text += p.text
        result["Headline"] = soup.title.string
        result["Text"] = text
        return result

    def www_straitstimes_com(self, text) -> dict:
        result = {
            "Type": "",
            "Time": time.strftime("%Y-%m-%d", time.gmtime()),
            "Headline": "",
            "Text": "",
            "Section": "",
            "Writers": "",
            "MainKeyWord": "",
            "AdditionalKeyWord": ""
        }
        soup = BeautifulSoup(text, "lxml")
        date = soup.find("li", {"class": "story-postdate"})
        if date.content is not None:
            result["Time"] = date.content[1]
        result["Headline"] = soup.title.string
        result["Text"] = "".join([i.text for i in soup.find_all("p")])
        return result

    def www_channelnewsasia_com(self, text) -> dict:
        result = {
            "Type": "",
            "Time": time.strftime("%Y-%m-%d", time.gmtime()),
            "Headline": "",
            "Text": "",
            "Section": "",
            "Writers": "",
            "MainKeyWord": "",
            "AdditionalKeyWord": ""
        }
        article = BeautifulSoup(text, "lxml").find("article")

        result["Type"] = (
            article.find("header")
            .find("span", {"class": "article__category"})
            .get_text(strip=True)
        )
        result["Headline"] = article.find("h1").get_text(strip=True)
        result["Text"] = "".join([
            p.get_text(strip=True)
            for p in article.find_all("p")
        ])
        result["MainKeyWord"] = ",".join([
            li.get_text(strip=True)
            for li in article.find("footer").find("ul").find_all("li")
        ])

        return result


class GoogleNews(requests.Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_topstories = "https://news.google.com/topstories"
        self.pageparser = PageParser()

    def get(self, url, **kwargs):
        try:
            return super().get(url, **kwargs)
        except Exception as e:
            print(e)
            warn("Error in response: {}".format(url))
            return None

    def get_article_urls(self, hl) -> list:
        """获得所有文章的 url

        Args:
            hl: 国家地区, 来自于 url 中的 hl 参数, 比如 "en-SG", "en-ID", ...

        Returns:
            一个列表, 包含所有文章的真实 url 字符串
        """

        # 获取首页
        response = self.get(self.url_topstories, params={"hl": hl})

        if not response:
            warn("无响应, 检查网络")
            return []
        sleep(0.1)
        # Path("a.html").write_text(response.text, "utf8")

        # 获取 More Headlines
        Path("./tmp/a.html").write_text(response.text, encoding="utf8")
        url_more_headlines = BeautifulSoup(response.text, "lxml").find(
            text="More Headlines").parent.get("href")
        response = self.get(urlparser.urljoin(
            response.url, url_more_headlines))
        if not response:
            warn("无响应, 检查网络")
            return []
        sleep(0.1)
        # Path("b.html").write_text(response.text, "utf8")

        # 获取 Google 的文章伪链接
        url_articles = [
            # 这里加了一个点, 不知道为什么url的相对路径有问题
            urlparser.urljoin(response.url, "."+e.a["href"])
            for e in BeautifulSoup(response.text, "lxml").find_all("article")
        ]

        # 获取文章的真实链接
        url_real = []
        for url in tqdm(url_articles, desc="获取文章真实链接", ncols=100):
            response = self.get(url)
            if not response:
                continue
            sleep(0.1)
            # Path("c.html").write_text(response.text, "utf8")
            url_real.append(BeautifulSoup(
                response.text, "lxml").find("noscript").a.get("href"))

        return url_real

    def get_article(self, url_article) -> dict:
        """返回结构化的文章数据"""
        # XXX: 这地方如果有requests解决不了的 url, 可以通过urlparse判断域名, 然后用无头浏览器去访问页面
        # 无头浏览器部分暂时没写, 如果很多都没办法用 requests 获取, 可能也要加一个表来记录哪些域名要用无头浏览器解析
        response = self.get(url_article)
        sleep(0.1)

        # 给 parser 解析
        result = self.pageparser(
            urlparser.urlparse(url_article).netloc,
            (response.text if response else "")
        )
        result["URL"] = url_article  # 补充两个数据
        result["Source"] = "google"
        return result


def get_domains(urls) -> set:
    """返回不重复的所有域名集合"""
    return set(urlparser.urlparse(url).netloc for url in urls)


if __name__ == "__main__":
    spider = GoogleNews()
    spider.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    }

    url_articles = spider.get_article_urls("en-SG")
    pprint(url_articles)
    with Path("urls.json").open("w", encoding="utf8") as f:
        json.dump(url_articles, f)

    text = spider.get_article(url_articles[0])
    with Path("example.json").open("w", encoding="utf8") as f:
        json.dump(text, f, ensure_ascii=False)
