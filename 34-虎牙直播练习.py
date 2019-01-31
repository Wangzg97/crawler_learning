from selenium import webdriver
from time import sleep

chrome = webdriver.Chrome()
chrome.get("https://www.huya.com/g/lol")
i = 1
while True:
    print("第" + str(i) + "页-------------------------------------------")
    i += 1
    sleep(10)
    html = chrome.page_source
    names = chrome.find_elements_by_xpath('//i[@class="nick"]')
    counts = chrome.find_elements_by_xpath('//i[@class="js-num"]')
    for name, count in zip(names, counts):
        print(name.text + ":" + count.text)
    if chrome.page_source.find('laypage_next') != -1:
        chrome.find_element_by_xpath('//a[@class="laypage_next"]').click()
    else:
        break
