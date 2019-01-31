from urllib.request import urlopen
from urllib.request import Request
from random import choice

url = "https://www.baidu.com"
# 随即使用不同的ua
user_agents = ["Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
             "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"]

# print(choice(user_agents))
headers = {
    "User-Agent": choice(user_agents)
}
request = Request(url, headers=headers)
print(request.get_header('User-agent'))
response = urlopen(request)

info = response.read()

print(info.decode())
