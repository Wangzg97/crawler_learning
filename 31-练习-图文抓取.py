import requests
from fake_useragent import UserAgent
from lxml import etree

url = 'http://www.farmer.com.cn/xwpd/rdjj1/201807/t20180726_1393916.htm'
headers = {
    "User-Agent": UserAgent().random
}

response = requests.get(url, headers=headers)
e = etree.HTML(response.text)  # xpath解析

title = e.xpath('//h1/text()')  # 文章标题

content = e.xpath('//div[@class="content"]//p')  # 文章内容
# content优化格式
content_list = []
for c in content:
    info = c.xpath('string(.)')  # 格式化当前节点
    content_list.append(info)
content_str = ''.join(content_list)  # 字符串化

img_urls = e.xpath('//div[@class="content"]//img/@src')  # 图片链接

img_names = e.xpath('//div[@align="center"]')  # 图片标题
for num in range(1, len(img_names), 2):
    img_name = img_names[num].xpath('string(.)')
