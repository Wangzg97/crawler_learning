from urllib.request import Request, ProxyHandler, build_opener
from fake_useragent import UserAgent

url = "http://httpbin.org/get"
headers = {
    "User-Agent": UserAgent().chrome
}
request = Request(url, headers=headers)
# handler = ProxyHandler({"http": "username:password@ip:port"})
handler = ProxyHandler({"http": "119.101.113.58:9999"})
opener = build_opener(handler)
response = opener.open(request)
print(response.read().decode())
