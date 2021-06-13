# -*- coding: utf-8 -*-
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

    def load_page(self, url, time=5):
        self.browser.set_page_load_timeout(time)
        self.browser.set_script_timeout(time)
        try:
            self.browser.get(url)
        except:
            # 执行js脚本
            self.browser.execute_script("window.stop()")

    def crawl_search(self, num, main_key_words, additional_key_words, count=100):
        all_news = []
        real_key_word = (main_key_words+" " +
                         additional_key_words).replace(" ", "%20")
        search_url = "https://mb.com.ph/?s=" + real_key_word
        self.load_page(search_url)
        for li in self.browser.find_element_by_class_name("articles-list").find_elements_by_tag_name("li"):
            url = li.find_element_by_class_name(
                "title").find_element_by_tag_name("a").get_attribute('href')
            print(url)
            pass
