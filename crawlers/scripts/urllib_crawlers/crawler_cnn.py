# -*- coding: utf-8 -*-
import urllib.request
import json
import jsonpath


class Crawler():
    def __init__(self, globle_config):
        pass

    def crawl_search(self, num, main_key_words, additional_key_words, count=100):
        real_key_word = (main_key_words+" " +
                         additional_key_words).replace(" ", "%20")
        all_news = []
        counter = 0
        p_size = count
        p_from = 0
        page = 1
        print("搜索关键词为："+str((main_key_words+" " +
                             additional_key_words))+"，目标数目为："+str(num))
        while counter < num:
            current_url = "https://search.api.cnn.io/content?size=" + \
                str(p_size)+"&q="+str(real_key_word)+"&page=" + \
                str(page) + "&from="+str(p_from)
            response = urllib.request.urlopen(current_url)
            text_data = json.loads(response.read())
            print("遍历第"+str(page)+"页，已爬取"+str(counter)+"/"+str(num))
            if not len(text_data['result']):
                print("可爬取数量不足目标数量")
                break
            for news in text_data['result']:
                try:
                    tmp = {
                        "Type": jsonpath.jsonpath(news, '$..type')[0],
                        "Time": jsonpath.jsonpath(news, '$..firstPublishDate')[0][0:10],
                        # 避免编码问题
                        "Headline": jsonpath.jsonpath(news, '$..headline')[0],
                        "Text": jsonpath.jsonpath(news, '$..body')[0],
                        "Section": jsonpath.jsonpath(news, '$..section')[0],
                        "Writers": jsonpath.jsonpath(news, '$..contributors')[0],
                        "URL": jsonpath.jsonpath(news, '$..url')[0],
                        "MainKeyWord": main_key_words,
                        "AdditionalKeyWord": additional_key_words,
                        "Source": "CNN"
                    }
                    all_news.append(tmp)
                    counter += 1
                except Exception:
                    pass
            page = page + 1
            p_from = counter
        print("爬取完成，爬取"+str(counter)+"/"+str(num))
        return all_news
