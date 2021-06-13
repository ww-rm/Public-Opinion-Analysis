from scripts.urllib_crawlers.crawler_google import GoogleNews
import pprint
from tqdm import tqdm
from pathlib import Path
import json
import os
import datetime
import re
import hashlib


def generate_dir_trees(country: str, urls: list,day_time: str) -> None:
    url_set = set(map(lambda s: re.match(
        r"(.*)//([a-z0-9\.]*)/(.*)", s).group(2).replace(".", "_"), urls))
    for url in url_set:
        try:
            os.makedirs("./results/" + day_time + "/" + country + "/" + url)
        except FileExistsError:
            pass


def get_direction(country: str, day_time: str, url: str) -> str:
    url_set = re.match(
        r"(.*)//([a-z0-9\.]*)/(.*)", url).group(2).replace(".", "_")
    return "./results/" + day_time + "/" + country + "/" + url_set + '/'


if __name__ == "__main__":
    spider = GoogleNews()
    spider.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    }
    md5 = hashlib.md5()
    day_time = datetime.datetime.today().__str__(
    )[:16].replace(" ", "_").replace(":", "_").replace("-", "_")
    url_articles = spider.get_article_urls("en-SG")
    os.makedirs("./results/" + day_time + "/")
    # generate_dir_trees("en_SG", url_articles,day_time)
    for url in tqdm(url_articles,desc="爬取文章内容", ncols=100):
        content = spider.get_article(url)
        text = content["Text"]
        md5.update(text.encode("utf-8"))
        # path = get_direction("en_SG", day_time, url)
        path = "./results/" + day_time + "/"
        with Path(path+md5.hexdigest()+".json").open("w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False)
