import requests
from fake_useragent import UserAgent

session = requests.Session()
login_url = "http://www.sxt.cn/index/login/login.html"
headers = {
    "User-Agent": UserAgent().chrome
}
params = {
    "user": "17703181473",
    "password": "123456"
}
response = session.post(login_url, headers=headers, data=params)

info_url = "http://www.sxt.cn/index/user.html"
response = session.get(info_url, headers=headers)
print(response.text)
