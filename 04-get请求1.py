from urllib.request import Request,urlopen
# 转码用
from urllib.parse import quote

url = "https://www.baidu.com/s?wd={}".format(quote("游戏"))
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
}
request = Request(url, headers=headers)
response = urlopen(request)
print(response.read().decode())
