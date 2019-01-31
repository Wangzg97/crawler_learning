from lxml import etree
import requests
from fake_useragent import UserAgent

url = "https://www.qidian.com/rank/yuepiao?chn=21"
headers = {
    "User-Agent": UserAgent().random
}
response = requests.get(url, headers=headers)
e = etree.HTML(response.text)
names = e.xpath("//h4/a/text()")
authors = e.xpath('//p[@class="author"]/a[1]/text()')

# for i in range(len(names)):
#     print(names[i]+"--"+authors[i])

for name, author in zip(names, authors):
    print(name+"--"+author)
