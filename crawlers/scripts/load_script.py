def load_script(path):
    script = []
    f = open(path, "r")
    line = f.readline()  # 读取第一行
    while line:
        txt_data = str(line).split(" ")
        txt_data[-1] = txt_data[-1].replace('\n', '')
        script.append(txt_data)  # 列表增加
        line = f.readline()  # 读取下一行
    return script
