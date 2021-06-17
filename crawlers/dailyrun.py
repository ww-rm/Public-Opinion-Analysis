import datetime
from hashlib import md5
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from warnings import warn

from tqdm import tqdm

from .scripts.urllib_crawlers.crawler_google import GoogleNews


def run(save_dir="./data/crawler_data", proxies: dict = None) -> bool:
    """
    Args:
        save_dir: data save path
        proxies: proxies params for requests
    """
    spider = GoogleNews()
    spider.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    }

    # 发现 Google 需要这个东西允许使用 cookie
    spider.cookies.set("CONSENT", "YES+cb.20210609-02-p0.en-SG+FX+425")
    if proxies:
        spider.proxies = proxies.copy()

    # use Bejjing datetime stamp
    day_time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")

    # create save dir
    save_dir = Path(save_dir, day_time)
    save_dir.mkdir(parents=True, exist_ok=True)

    try:
        url_articles = spider.get_article_urls("en-SG")
    except:
        # raise
        warn("获取文章链接失败")
        url_articles = []
        return False

    for url in tqdm(url_articles, desc="爬取文章内容", ncols=100):
        content = spider.get_article(url)
        text: str = content["Text"]
        md5_id = md5(text.encode("utf8")).hexdigest()

        with save_dir.joinpath(md5_id+".json").open("w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False)

    return True
