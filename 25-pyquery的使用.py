# 抓取https://www.xicidaili.com/nn的高匿IP存入文件中
from pyquery import PyQuery as pq
import requests
from fake_useragent import UserAgent

url = "https://www.xicidaili.com/nn"
headers = {"User-Agent": UserAgent().random}
response = requests.get(url, headers=headers)
doc = pq(response.text)
trs = doc("#ip_list tr")
with open("ip_port_type.txt", "w", encoding="utf-8") as f:
    for num in range(1, len(trs)):
        ip = trs.eq(num).find("td").eq(1).text()
        port = trs.eq(num).find("td").eq(2).text()
        type = trs.eq(num).find("td").eq(5).text()
        f.write(ip+"---"+port+"---"+type+"\n")
