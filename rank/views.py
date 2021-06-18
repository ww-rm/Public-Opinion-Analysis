from django.shortcuts import render
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Graph, Line, Liquid, WordCloud
from pyecharts.globals import SymbolType
import json
import math
from datetime import datetime
from urllib.parse import quote, unquote

from pyecharts.globals import CurrentConfig
default_host = CurrentConfig.ONLINE_HOST
print(default_host)
custom_host = "/static/js/" 
CurrentConfig.ONLINE_HOST = custom_host

from pyecharts.types import Tooltip

area_color_js = (
    "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
    "[{offset: 0, color: 'white'}, {offset: 1, color: '#3fbbff0d'}], false)"
)
background_color_js = (  # 小标题有解释
    "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
    "[{offset: 0, color: '#06a7ff'}, {offset: 1, color: 'black'}], false)"
)


def get_data():
    with open('./data/db/timeline.json',encoding='utf8')as f:
        timeline=json.load(f)
    with open('./data/db/topic.json',encoding='utf8') as f:
        topic_data=json.load(f)
    today = datetime.now().strftime("%Y-%m-%d")
    topic=timeline[today]
    hotscore=[]
    detail=[]
    cloud_word=[]
    for t in topic:
        detail.append(topic_data[t]["detail"])
        hotscore.append(topic_data[t]["hotscore"])
        cloud_word.append(topic_data[t]["keywords_cloud"])
    return topic,detail,hotscore,cloud_word

def search(request):
    topic_request = request.GET.get("topic")
    topic,detail,hotscore,*_=get_data()
    r_topic=[]
    r_detail=[]
    r_hostscore=[]
    for i in range(len(topic)):
        for r in topic_request.lower().split(' '):
            if r in topic[i].lower():
                r_topic.append(topic[i])
                r_detail.append(detail[i])
                r_hostscore.append(hotscore[i])
    if r_topic:
        zipped = zip(r_topic,r_detail,r_hostscore)
        sort_zipped = sorted(zipped,key=lambda x:x[2],reverse=True)  
        result = zip(*sort_zipped)
        r_topic,r_detail,r_hostscore = [list(x) for x in result]
    else:
        r_topic=["no relative topic"]
        r_detail=["no relative topic"]
        r_hostscore=[0]

    rank_message = list(zip(r_topic, r_detail))

    data = {"rank_message": rank_message}
    return render(request, "search.html", data)


def render_line_chart(timeData, hotscoreData):
    line_chart = (
        Line(init_opts=opts.InitOpts())
        .add_xaxis(xaxis_data=timeData)
        .add_yaxis(
            series_name="热度",
            y_axis=hotscoreData,
            is_smooth=True,         #开启平滑
            is_symbol_show=True,    #显示 symbol
            symbol="circle",        #设置symbol类型
            symbol_size=6,          #设置symbol大小
            linestyle_opts=opts.LineStyleOpts(color="#fff"),    #设置线条颜色
            label_opts=opts.LabelOpts(
                is_show=True, position="top", color="white"),   #设置symbol的label样式
            itemstyle_opts=opts.ItemStyleOpts(
                color="red", border_color="#fff", border_width=3#设置symbol样式
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),       #设置提示框组件
            areastyle_opts=opts.AreaStyleOpts(
                color=JsCode(area_color_js), opacity=1),        #设置图表背景颜色
        )
        .set_global_opts(
            title_opts=opts.TitleOpts( #标题设置
                title="近期热度变化",
                pos_top="5%",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(
                        color="#fff", font_size=16),
            ),
            axispointer_opts=opts.AxisPointerOpts( #设置坐标轴指示器
                is_show=True,
                type_="line",
            ),
            xaxis_opts=opts.AxisOpts( 
                #坐标轴配置项 
                #详情见（https://pyecharts.org/#/zh-cn/）
                type_="category",
                boundary_gap=False,
                axislabel_opts=opts.LabelOpts(
                    margin=30, color="#ffffffff"),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=25,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            yaxis_opts=opts.AxisOpts( #坐标轴配置项
                type_="value",
                position="right",
                axislabel_opts=opts.LabelOpts(
                    margin=20, color="#ffffffff"),
                axisline_opts=opts.AxisLineOpts(
                    is_show=False,
                    # linestyle_opts=opts.LineStyleOpts(
                    #     width=2, color="#0000001f")
                ),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=15,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    return line_chart


def render_score_chart(hot_score,max_hotscore):
    score = (
        Liquid(init_opts=opts.InitOpts(width='300px', height='300px',))
        .add("热度", [hot_score/max_hotscore, 0.1, 0.2, 0.3,hot_score], is_outline_show=False, shape=SymbolType.DIAMOND)
        .set_global_opts(title_opts=opts.TitleOpts(title=""),)
    )
    return score


def test_render(request):
    timeData = [
        "2021/6/11 1:00",
        "2021/6/11 2:00",
        "2021/6/11 3:00",
        "2021/6/11 4:00",
        "2021/6/11 5:00",
        "2021/6/11 6:00",
        "2021/6/11 7:00",
        "2021/6/11 8:00",
        "2021/6/11 9:00",
        "2021/6/11 10:00"
        "2021/6/12 1:00",
        "2021/6/12 2:00",
        "2021/6/12 3:00",
        "2021/6/12 4:00",
        "2021/6/12 5:00",
        "2021/6/12 6:00",
        "2021/6/12 7:00",
        "2021/6/12 8:00",
        "2021/6/12 9:00",
        "2021/6/12 10:00", ]
    hotscoreData = [93, 138, 185, 196, 289, 299, 210, 200, 210, 260,393, 438, 485, 631, 689, 824, 987, 1000, 1100, 1200]
    cloud_words = [
        ("花鸟市场", 1446),
        ("汽车", 928),
        ("视频", 906),
        ("电视", 825),
        ("Lover Boy 88", 514),
        ("动漫", 486),
        ("家居风格", 187),
        ("家居家装关注品牌", 140),
        ("家纺", 107),
        ("厨具", 47),
        ("灯具", 43),
        ("家居饰品", 29),
        ("家居日常用品", 10)]
    dat=[]
    with open('./rank/data.txt', 'r')as f:
        for i in f.read().split('\n'):
            dat.append(i.split(','))
    c = render_graph_chart(dat)
    data = {"i": c.render_embed()}
    return render(request, "test.html",data)








def rank(request):
    topic,detail,hotscore,*_=get_data()
    today = datetime.now().strftime("%Y-%m-%d")
    score_chart = []
    line_charts = []
    last_hostscore=[]
    
    for i in range(len(topic)):
        last_hostscore.append(round(hotscore[i][today],2))
    max_hostscore=max(last_hostscore)
    print(hotscore)
    for i in range(len(topic)):
        score = render_score_chart(hotscore[i][today],max_hostscore)
        line_chart = render_line_chart(list(hotscore[i].keys()), list(hotscore[i].values()))
        score_chart.append(score.render_embed())
        line_charts.append(line_chart.render_embed())

    zipped = zip(topic,score_chart,line_charts,last_hostscore)
    sort_zipped = sorted(zipped,key=lambda x:x[3],reverse=True)  
    result = zip(*sort_zipped)
    topic,score_chart,line_charts,last_hostscore = [list(x) for x in result]

    rank_message = list(zip(topic, detail, score_chart, line_charts,last_hostscore))
    data = {"rank_message": rank_message}
    return render(request, "rank.html", data)

 
def render_graph_chart(dat):
    nodes_data = []
    links_data = []
    node = []
    #准备节点与节点间数据
    for i in dat:
        # print(int(i[0]), i[1], i[2])
        if i[0] not in node:
            node.append(i[0])
        if i[1] not in node:
            node.append(i[1])
        links_data.append(opts.GraphLink(source=i[1], target=i[0], value=0))
    for i in node:
        nodes_data.append(opts.GraphNode(name=i, symbol_size=10, value=10,label_opts=opts.LabelOpts(color="white"), category=0))

    graph_chart = (
        Graph()
        .add(
            "",
            nodes_data,     #节点数据
            links_data,     #节点间关系数据
            is_draggable=True,  #开启拖拽功能
            layout='circular',  #使用圆型排列
            is_focusnode=True,  #是否在鼠标移到节点上的时候突出显示节点以及节点的边和邻接节点
            edge_label=opts.LabelOpts(  #图节点边的Label配置
                is_show=False, position="middle", formatter="{c}"
            ),
            is_rotate_label=True,   #节点label旋转
            linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),   #线条样式
            categories=[{
                "itemStyle": {
                    "normal": {
                        "color": '#bbffff',
                    }
                }
            }]
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="关系图")
        )
    )
    return graph_chart

def render_detail_line_chart(timeData, hotscoreData):
    line_chart = (
        Line(init_opts=opts.InitOpts(width='75%'))
        .add_xaxis(timeData)
        .add_yaxis("热度",
                   hotscoreData,
                   is_smooth=True,  # 平滑曲线
                   is_symbol_show=True,  # 显示数字标签
                   symbol="circle",
                   symbol_size=6,  # 圆点大小
                   linestyle_opts=opts.LineStyleOpts(color="#fff"),  # 线的颜色
                   label_opts=opts.LabelOpts(
                       is_show=True, position="top", color="white"),  # 数字标签的位置
                   itemstyle_opts=opts.ItemStyleOpts(
                       color="red", border_color="#fff", border_width=3  # 设置填充颜色以及边框
                   ),
                   tooltip_opts=opts.TooltipOpts(is_show=False),
                   areastyle_opts=opts.AreaStyleOpts(color=JsCode(area_color_js), opacity=1),)

        .set_global_opts(
            #全局配置项
            #详情见（https://pyecharts.org/#/zh-cn/）
            datazoom_opts=[
                opts.DataZoomOpts(
                    type_="slider", range_start=0, range_end=100),
            ],
            axispointer_opts=opts.AxisPointerOpts(
                is_show=True,
                type_="line",
            ),
            title_opts=opts.TitleOpts(  # 标题设置
                title="热度变化",
                pos_top="5%",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(
                    color="#fff", font_size=16),
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                # type_="time",
                boundary_gap=False,

                axislabel_opts=opts.LabelOpts(
                    margin=0, color="#ffffffff"),
                axisline_opts=opts.AxisLineOpts(
                    is_show=False,
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                position="right",
                axislabel_opts=opts.LabelOpts(margin=20, color="#ffffffff"),
                axisline_opts=opts.AxisLineOpts(
                    is_show=False,
                ),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=15,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            legend_opts=opts.LegendOpts(
                type_='plain', is_show=False, pos_left='20%'),
        )
    )
    return line_chart


def render_word_clound(cloud_words):
    word_cloud = (
        WordCloud(init_opts=opts.InitOpts(width='75%'))
        .add("", cloud_words, word_size_range=[20, 80], rotate_step=45)
        .set_global_opts(title_opts=opts.TitleOpts(  # 标题设置
            title="Word Cloud",
            pos_top="5%",
            pos_left="center",
            title_textstyle_opts=opts.TextStyleOpts(
                    color="#fff", font_size=32),
        ),
            legend_opts=opts.LegendOpts(type_='plain', is_show=False, pos_left='center'))
    )
    return word_cloud


def details(request):
    topic_request = request.GET.get("topic")
    # print(request.GET)
    # print(topic_request)
    topic,detail,hotscore,cloud_word=get_data()
    with open('./data/db/topic.json',encoding='utf8') as f:
        topic_data=json.load(f)
    cloud_word=topic_data[topic_request]["keywords_cloud"]
    # print(cloud_word)
    today = datetime.now().strftime("%Y-%m-%d")
    word_cloud = render_word_clound(cloud_word)
    # print(list(topic_data[topic_request]["hotscore"].keys()))
    line_chart = render_detail_line_chart(list(topic_data[topic_request]["hotscore"].keys()),list(topic_data[topic_request]["hotscore"].values()))
    
    dat = topic_data[topic_request]["knowledge"]
    graph_chart = render_graph_chart(dat)

    data = {'line_chart': line_chart.render_embed(
    ), "word_cloud": word_cloud.render_embed(), "topic": topic_request, "graph_chart": graph_chart.render_embed()}

    return render(request, "details.html", data)
