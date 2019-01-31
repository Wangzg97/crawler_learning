from urllib.request import Request, urlopen
from urllib.error import URLError
from fake_useragent import UserAgent

url = "http://www.sxt.cn/index/login/login.html"
headers = {
    "User-Agent": UserAgent().chrome
}
try:
    req = Request(url, headers=headers)
    resp = urlopen(req)
    print(resp.read().decode())
except URLError as e:
    if e.args == ():
        print(e.code)
    else:
        print(e.args[0].errno)
print("访问完成")
