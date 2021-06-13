import os
import json
import hashlib


def save_news(dic, path, time):
    if path[-1] != "/":
        path = path+"/"
    try:
        os.makedirs(path+time+"/")
    except(Exception):
        pass
    md5hash = hashlib.md5(str(dic["URL"]).encode("utf-8"))
    md5 = md5hash.hexdigest()
    save_name = path+time+"/"+md5+".json"
    js = json.dumps(dic, ensure_ascii=False)
    if os.path.exists(save_name):
        # print("文件重复，已覆盖")
        pass
    with open(save_name, 'w', encoding="utf-8") as f:
        f.write(js)
    f.close()


if __name__ == "__main__":
    test = {"test": "test", "URL": "192.168.1.1"}
    save_news(test, "tmp", "2021-01-21")
