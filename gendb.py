"""
用于生成 topic.json 和 timeline.json
"""
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

from tqdm import tqdm

if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    timeline_db_path = Path("./data/db/timeline.json")
    topic_db_path = Path("./data/db/topic.json")
    timeline_db = {}
    topic_db = {}

    topic_dir = Path("./data/hotspot/daily/topic/")
    kg_dir = Path("./data/kg/")

    topic_files = topic_dir.glob("*-[0-9].json")
    # 这一步是按照文件的日期升序迭代的, 时间一定是由前到后
    for topic_file in tqdm(topic_files):
        with topic_file.open("r", encoding="utf8") as f:
            topic = json.load(f)[0]

        date = re.findall(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", topic_file.stem)[0]
        topic_title = topic.get("topic", "")

        # 统计某一天出现的所有的话题
        if date not in timeline_db:
            timeline_db[date] = [topic_title]
        else:
            timeline_db[date].append(topic_title)

        # 统计出现过的每一个话题的信息, 添加历史热度指数记录
        if topic_title not in topic_db:
            topic_db[topic_title] = {
                "hotscore": {
                    date: topic.get("hotscore")
                },
                "detail": "",
                "keywords_cloud": [],
                "knowledge": []
            }

        else:
            topic_db[topic_title]["hotscore"][date] = topic.get("hotscore", 1)

        # 用当前最新则更新话题详细信息, 词云, 知识图谱内容
        topic_db[topic_title]["detail"] = topic.get("detail", "detail")
        topic_db[topic_title]["keywords_cloud"] = sorted(
            map(lambda x: [x[0], (1/x[1])], topic.get("keywords_cloud")),
            key=lambda x: x[1],
            reverse=True
        )
        with kg_dir.joinpath(topic_file.stem).with_suffix(".txt").open("r", encoding="utf8") as f:
            kg_data = [line.strip("\n").split("\t") for line in f.readlines()[:30]]
        topic_db[topic_title]["knowledge"] = kg_data

    # 生成数据库
    with timeline_db_path.open("w", encoding="utf8") as f:
        json.dump(timeline_db, f, ensure_ascii=False)
    with topic_db_path.open("w", encoding="utf8") as f:
        json.dump(topic_db, f, ensure_ascii=False)
