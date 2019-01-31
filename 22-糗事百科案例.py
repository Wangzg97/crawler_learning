import requests
from fake_useragent import UserAgent
import re

url = "https://www.qiushibaike.com/text/page/1"
headers = {
    "User-Agent": UserAgent().random
}
response = requests.get(url, headers=headers)
info = response.text
infos = re.findall(r'<div class="content">\s*<span>\s*(.+)\s*</span>', info)
with open("糗事百科.txt", "w", encoding="utf-8") as f:
    for info in infos:
        f.write(info + "\n\n")
