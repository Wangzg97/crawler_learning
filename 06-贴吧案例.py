from urllib.request import urlopen, Request
from urllib.parse import urlencode
from fake_useragent import UserAgent

def get_html(url):
    headers = {
        "User-Agent": UserAgent().chrome
    }
    request = Request(url, headers=headers)
    response = urlopen(request)
    return response.read()

def save_html(filename, html):
    with open(filename, "wb") as f:
        f.write(html)

def main():
    content = input("下载内容： ")
    num = input("下载页数： ")
    url_base = "https://tieba.baidu.com/f?ie=utf-8&{}"
    for pn in range(int(num)):
        args = {
            "wd": content,
            "pn": pn * 50
        }
        args = urlencode(args)
        html = get_html(url_base.format(args))
        filename = "第{}页.html".format(pn)
        print("正在下载", filename)
        save_html(filename, html)

if __name__ == '__main__':
    main()
    print("下载完毕！")
