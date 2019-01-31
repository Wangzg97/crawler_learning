from selenium import webdriver


# 使用Chrome无头浏览器
options = webdriver.ChromeOptions()
options.add_argument('--headless')
chrome = webdriver.Chrome(chrome_options=options)

chrome.get("http://cn.bing.com")
chrome.find_element_by_id('sb_form_q').send_keys("python")
chrome.find_element_by_id('sb_form_go').click()
html = chrome.page_source
print(html)
