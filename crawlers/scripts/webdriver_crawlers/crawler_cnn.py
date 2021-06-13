import sys
import re
from selenium import webdriver
import platform
import time


class Crawler():
    def __init__(self, globle_config, local_config=None):
        platform_ = platform.system()
        self.browser = webdriver.Firefox()
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
        self.target_url = "https://us.cnn.com"

    def load_page(self, url, time=5):
        self.browser.set_page_load_timeout(time)
        self.browser.set_script_timeout(time)
        try:
            self.browser.get(url)
        except:
            # 执行js脚本
            self.browser.execute_script("window.stop()")

    def crawl_search(self, text, num, count=10):
        urls = []
        counter = 0
        p_size = count
        p_from = 0
        page = 1
        current_url = self.target_url+"/search?size=" + \
            str(p_size)+"&q="+text+"&from="+str(p_from)+"&page="+str(page)
        self.load_page(current_url)
        print("搜索关键词为："+str(text)+"，目标数目为："+str(num))
        while counter < num:
            print("遍历第"+str(page)+"页...")
            for result in self.browser.find_elements_by_class_name("cnn-search__result"):
                url = result.find_element_by_tag_name(
                    "a").get_attribute('href')
                urls.append(url)
                counter += 1
            print("找到"+str(counter)+"/"+str(num)+"条内容")
            page += 1
            p_from += p_size
            current_url = self.target_url+"/search?size=" + \
                str(p_size)+"&q="+text+"&from="+str(p_from)+"&page="+str(page)
            self.load_page(current_url)
        print("搜索完成")
        return urls

    def crawl_urls(self):
        self.load_page(self.target_url)
        title = self.browser.title
        top_hit = ""
        hot_urls = []
        other_urls = []
        # 头条
        top_hit = self.browser.find_elements_by_class_name("zn__containers")[
            0].find_element_by_tag_name("li").find_element_by_tag_name("a").get_attribute('href')
        # 热门新闻
        hot_li = self.browser.find_elements_by_class_name(
            "zn__containers")[1].find_elements_by_tag_name("li")
        for li in hot_li:
            url = li.find_element_by_tag_name("a").get_attribute('href')
            hot_urls.append(url)
        # 其他分类
        others_column = self.browser.find_elements_by_class_name(
            "zn__containers")[2].find_elements_by_class_name("column")
        for col in others_column:
            other_li = col.find_elements_by_tag_name("li")
            for li in other_li:
                url = self.target_url + \
                    col.find_element_by_tag_name("a").get_attribute('href')
                other_urls.append(url)

    def crawl_single_page_1(self, url):
        self.load_page(url)
        title = self.browser.title
        text = ""
        self.browser.execute_script(
            "window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        data = self.browser.find_elements_by_tag_name("p")  # 匹配url的所有网页源码
        for tag in data:  # 遍历出所有内容
            text += tag.text  # 把所有的文本打印出来
        return title, text

    def crawl_single_page_2(self, url):
        self.load_page(url)
        title = self.browser.title
        text = ""
        self.browser.execute_script(
            "window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        data = self.browser.find_elements_by_class_name(
            "zn-body__paragraph")  # 匹配url的所有网页源码
        for tag in data:  # 遍历出所有内容
            text += tag.text  # 把所有的文本打印出来
        return title, text

    def crawl_single_page_3(self, url):
        self.load_page(url)
        title = self.browser.title
        text = ""
        self.browser.execute_script(
            "window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        data = self.browser.find_elements_by_tag_name("span")  # 匹配url的所有网页源码
        for tag in data:  # 遍历出所有内容
            text += tag.text  # 把所有的文本打印出来
        return title, text

    def clean_tmp(self):
        if len(self.tmp_files) == 0:
            pass
        else:
            for tmp_file in self.tmp_files:
                import os
                os.remove(self.tmp_path + tmp_file)
