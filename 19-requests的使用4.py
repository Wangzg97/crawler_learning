import requests
from fake_useragent import UserAgent

url = "http://httpbin.org/get"
headers = {
    "User-Agent": UserAgent().chrome
}
# verify=False 忽略证书验证
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings()
response = requests.get(url, headers=headers, verify=False)
response.encoding = "utf-8"
print(response.text)
