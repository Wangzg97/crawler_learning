from urllib.request import Request,urlopen
from fake_useragent import UserAgent

headers = {
    "User-Agent": UserAgent().chrome
}
url = "https://www.baidu.com"
request = Request(url, headers=headers)
print(request.get_header('User-agent'))
response = urlopen(request)