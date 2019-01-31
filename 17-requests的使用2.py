import requests
from fake_useragent import UserAgent

url = "http://www.sxt.cn/index/login/login.html"
headers = {
    "User-Agent": UserAgent().chrome
}
params = {
    "user": "17703181473",
    "password": "123456"
}
response = requests.post(url, headers=headers, data=params)
print(response.text)
