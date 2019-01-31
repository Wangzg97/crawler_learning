from urllib.request import urlopen, Request
from urllib.parse import urlencode
from fake_useragent import UserAgent

url = "http://www.sxt.cn/index/login/login.html"
form_data = {
    "user": "17703181473",
    "password": "123456"
}
form_data = urlencode(form_data)
headers = {
    "User-agent": UserAgent().chrome
}
request = Request(url, data=form_data.encode(), headers=headers)
response = urlopen(request)
print(response.read().decode())
