from jsonpath import jsonpath
import json
import requests
from fake_useragent import UserAgent

url = "https://www.lagou.com/lbs/getAllCitySearchLabels.json"
headers = {
    "User-Agent": UserAgent().chrome
}
response = requests.get(url, headers=headers)

names = jsonpath(json.loads(response.text), '$..name')
codes = jsonpath(response.json(), '$..code')

for name, code in zip(names, codes):
    print(name+":"+code)
