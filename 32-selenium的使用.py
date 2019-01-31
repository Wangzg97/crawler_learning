from selenium import webdriver

chrome = webdriver.Chrome()
chrome.get("https://www.baidu.com")  # 打开指定网页

chrome.save_screenshot('baidu.png')  # 保存屏幕截图

html = chrome.page_source  # 获取网页源码


# chrome.quit()  # 退出浏览器
