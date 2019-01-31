from urllib.request import Request, build_opener, HTTPHandler
from fake_useragent import UserAgent

url = "https://www.baidu.com"
headers = {
    "User-Agent": UserAgent().chrome
}
request = Request(url, headers=headers)
handler = HTTPHandler()
opener = build_opener(handler)
reponse = opener.open(request)
print(reponse.read().decode())
