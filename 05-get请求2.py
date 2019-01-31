from urllib.request import Request,urlopen
from urllib.parse import urlencode
#转码
args = {
    "wd": "游戏",
    "ie": "utf-8"
}
# print(urlencode(args))

url = "https://www.baidu.com/s?{}".format(urlencode(args))
print(url)
