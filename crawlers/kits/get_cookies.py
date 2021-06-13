import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar

URL_ROOT = 'http://www.dailynews.lk/line/bbc'  # 目标网址
values = {'name': '******', 'password': '******'}  # post内容
cookie_filename = 'cookie.txt'  # cookie存放目标


postdata = urllib.parse.urlencode(values).encode()
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {'User-Agent': user_agent}


cookie = http.cookiejar.LWPCookieJar(cookie_filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

request = urllib.request.Request(URL_ROOT, data=postdata, headers=headers)
try:
    response = opener.open(request)
except urllib.error.URLError as e:
    print(e.reason)

cookie.save(ignore_discard=True, ignore_expires=True)  # 保存cookies到目标文件


# 打印cookies
for item in cookie:
    print('Name = ' + item.name)
    print('Value = ' + item.value)


# 提取存储在文件的cookie并以此访问网站
"""
import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar

cookie_filename = 'cookie_jar.txt'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

get_url = 'http://www.jobbole.com/'  # 利用cookie请求访问另一个网址
get_request = urllib.request.Request(get_url)
get_response = opener.open(get_request)
print(get_response.read().decode())
"""
