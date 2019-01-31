from urllib.request import Request, build_opener, HTTPCookieProcessor, ProxyHandler
from fake_useragent import UserAgent
from urllib.parse import urlencode

# 登录
login_url = "https://u.njtech.edu.cn/cas/login"
headers = {
    "User-Agent": UserAgent().chrome
}
form_data = {
    "username": "1401160226",
    "password": "w1401160226"
}
form_data = urlencode(form_data).encode()
request = Request(login_url, headers=headers, data=form_data)
proxy_handler = ProxyHandler({"http": "119.101.113.58:9999"})
handler = HTTPCookieProcessor()
opener = build_opener(handler, proxy_handler)
response = opener.open(request)
# print(response.read().decode())
# 访问页面
info_url = "https://i.njtech.edu.cn/index.html"
request = Request(info_url, headers=headers)
response = opener.open(request)
print(response.read().decode())
