import requests
from fake_useragent import UserAgent

url = "http://httpbin.org/get"
headers = {
    "User-Agent": UserAgent().chrome
}
proxies = {
    "http": "http://119.101.114.37:9999"
}
response = requests.get(url, headers=headers, proxies=proxies)
print(response.text)
