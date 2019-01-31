from threading import Thread
from queue import Queue
import requests
from fake_useragent import UserAgent
from lxml import etree


# 爬虫类
class Crawler(Thread):
    def __init__(self, url_queue, html_queue):
        Thread.__init__(self)
        self.url_queue = url_queue
        self.html_queue = html_queue

    def run(self):
        headers = {
            "User-Agent": UserAgent().random
        }
        while not self.url_queue.empty():
            response = requests.get(self.url_queue.get(), headers=headers)
            if response.status_code == 200:
                self.html_queue.put(response.text)


# 解析类
class Parse(Thread):
    def __init__(self, html_queue):
        Thread.__init__(self)
        self.html_queue = html_queue

    def run(self):
        while not self.html_queue.empty():
            e = etree.HTML(self.html_queue.get())
            span_contents = e.xpath('//div[@class="content"]/span[1]')
            with open("糗事百科多线程抓取.txt", "a", encoding='utf-8') as f:
                for span in span_contents:
                    info = span.xpath('string(.)')
                    f.write(info)


if __name__ == '__main__':
    # 存放url的容器
    url_queue = Queue()
    # 存储内容的容器
    html_queue = Queue()
    base_url = "https://www.qiushibaike.com/text/page/{}/"
    for i in range(1, 14):
        new_url = base_url.format(i)
        url_queue.put(new_url)
    # 创建多线程爬虫
    crawler_list = []
    for i in range(0, 3):
        crawler = Crawler(url_queue, html_queue)
        crawler_list.append(crawler)
        crawler.start()
    for crawler in crawler_list:
        crawler.join()  # 等待子线程结束
    # 开启多线程解析'
    parse_list = []
    for i in range(0, 3):
        parse = Parse(html_queue)
        parse_list.append(parse)
        parse.start()
    for parse in parse_list:
        parse.join()
