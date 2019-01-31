from selenium import webdriver
from lxml import etree
from time import sleep

chrome = webdriver.Chrome()
url = "https://search.jd.com/Search?keyword=macbook&enc=utf-8&suggest=4.def.0.V13&pvid=b929e83e486f4016ae2846d35ecab2f1"
chrome.get(url)
# 滚动条滚动至最底部
js = "document.documentElement.scrollTop=10000"
chrome.execute_script(js)

sleep(10)
html = chrome.page_source
e = etree.HTML(html)
prices = e.xpath('//li[@class="gl-item"]//strong/i/text()')
names = e.xpath('//li/div/div[3]/a/em/text()')
print(len(names))

for name, price in zip(names, prices):
    print(name, ":", price)
