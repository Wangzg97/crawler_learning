from urllib.request import Request, urlopen, HTTPCookieProcessor
from fake_useragent import UserAgent

url = "https://i.njtech.edu.cn/index.html"
headers = {
    "User-Agent": UserAgent().chrome,
    "Cookie": "JSESSIONID=E0F2A2E4CDA5C7944CD6F90148AA2A86.TomcatB; insert_cookie=67313298"
}
request = Request(url, headers=headers)
response = urlopen(request)
print(response.read().decode())
