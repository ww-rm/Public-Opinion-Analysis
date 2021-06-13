def save_urls(path, urls):
    try:
        urls = '\n'.join(urls)
        with open(path, 'w') as f:
            f.write(urls)
            f.close
        return 1
    except Exception:
        return 0


def load_urls(path):
    try:
        with open(path) as f:
            urls = f.read()
            urls = urls.split("\n")
            return urls
    except Exception:
        return 0
