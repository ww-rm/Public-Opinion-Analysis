# Public Opinion Analysis

热度话题生成及指数分析

## Environment

- python 3.7
- requirements.txt
- enen_core_web_sm == 3.0.0

还需要去 Release 页面下载对应的与训练词向量文件, 文件是经过处理后的 `glove.840B.300d.txt `, 被打包成了一份索引文件和向量文件, 下载之后解压至 `data/hotspot/` 目录下

```plain
data/
    hotspot/
        stopwords.txt
        glove.840B.300d/
            pretrained_wv.index.json
            pretrained_wv.vec.dat
```

> **Note**
>
> You can just run `install_env.sh` to install needed local virtual python env.
>
> If you use `install_env.sh` to install local venv, remember to replace all "python3" to you "env/bin/python3" in below commands.

## Usage

- `python3 -m crawlers`
  
    爬取今天的所有新闻, 生成的数据位于 `data/crawler_data/` 下

    ```plain
    data/
        crawler_data/
            2021-06-12/
                xxx.json
                xxx.json
                ...
            2021-06-12/
            ...
    ```

    数据格式示例

    ```json
    {
        "Type": "World",
        "Time": "2021-06-12",
        "Headline": "G7 summit outlines health pact to stop future pandemics",
        "Text": "CARBIS BAY, United Kingdom: G7 leaders are on Saturday (Jun 12) set to ...",
        "Section": "",
        "Writers": "",
        "MainKeyWord": "G7,China,news and politics,summit",
        "AdditionalKeyWord": "",
        "URL": "https://www.channelnewsasia.com/news/world/g7-summit-covid-19-vaccinations-who-un-covax-14999302",
        "Source": "google"
    }
    ```

- `python3 -m hotspot`

    从爬取的数据下生成最近 7 天的热度话题以及构建知识图谱所需要的数据, 共十个话题, 生成的数据位于 `data/hotspot/` 下

    ```plain
    data/
        hotspot/
            local.model
            daily/
              2021-06-12.csv
              2021-06-12.txt
              ...
              topic/
                  2021-06-12-0.json
                  2021-06-1201.json
                  ...
              knowledge/
                  2021-06-12-0.txt
                  2021-06-12-1.txt
                  ...
    ```

    topic 下文件格式示例

    ```json
    [
        {
            "topic": "", 
            "detail": "", 
            "hotscore_time": "2021-06-13", 
            "hotscore": 90.36981731641997, 
            "keywords_cloud": [
                ["self-test kits", 0.1469056468783066], 
                ["vaccine dose", 0.05816931982174091]
            ]
        }
    ]
    ```

- `python3 -m kgraph`

    生成每个话题的知识图谱, 生成的内容位于目录 `data/kg/` 下

    ```plain
    data/
        kg/
            2021-06-12-0.txt
            2021-06-12-1.txt
            ...
    ```

    生成的图谱文件格式示例（中间使用 `\t` 进行分割）

    ```plain
    source target edge
    ```

- `python3 gendb.py`

    用于整合并生成项目所需的数据文件 `timeline.json` 和 `topic.json`, 位于目录 `data/db/` 下

    ```plain
    data/
        db/
            timeline.json
            topic.json
    ```

    `timeline.json` 包含每一天对应的话题, `topic.json` 包含每一个话题的历史热度和词云等详细信息

## Add crontabs

可以在 linux 平台上使用 `crontab` 命令将上述三个指令设定为每天定时运行

使用命令 `crontab -e` 编辑定时任务, 首次运行会提示选择想要使用的文本编辑器, 选择 vim 即可. 然后将任务内容修改如下, 需要将 `$PROJECT_DIR` 替换成本地的项目路径

```crontab
0 */8 * * * bash $PROJECT_DIR/dailyrun.sh
```

## Run server

使用 `python3 manage.py runserver` 启动服务器, 项目基于 Django 实现, 其余选项与 Django 相同.
