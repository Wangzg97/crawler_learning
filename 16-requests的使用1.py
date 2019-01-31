import requests
from fake_useragent import UserAgent

url = "https://www.baidu.com/s"
headers = {
    "User-Agent": UserAgent().chrome
}
params = {
    "wd": "百度"
}
response = requests.get(url, headers=headers, params=params)
print(response.text)
