[TOC]
# Scrapy
## Scrapy项目结构

- 安装

  ```shell
  pip install scrapy # 或 conda install scrapy
  ```

- ```shell
  scrapy startproject PROJECT_NAME  # 创建名为PROJECT_NAME的scrapy工程
  ```

  scrapy startproject myspider创建名为myspider的工程，文件结构：

  > myspider
  >
  > > myspider
  > >
  > > > \_\_init\_\_.py
  > > >
  > > > _\_pycache\_\_
  > > >
  > > > items.py   # 需要爬取的内容
  > > >
  > > > middlewares.py  # 自定义中间件
  > > >
  > > > pipelines.py  # 管道，保存数据
  > > >
  > > > settings.py  # 设置文件
  > > >
  > > > spiders  # 存放spider，一个项目可以定义一多个爬虫
  > > >
  > > > > \_\_init\_\_.py
  > > > >
  > > > > \_\_pycache\_\_
  > >
  > > scrapy.cfg  #项目配置文件

- 在该工程下创建一个爬虫

  ```shell
  cd <PROJECT_NAME>  # 进入项目目录
  spider genspider <SPIDER_NAME> <DOMAIN>  # SPIDER_NAME爬虫名字，DOMAIN域名
  ```

  如：

  ```shell
  cd myspider
  spider genspider baidu baidu.com
  ```
  
  此时spiders文件夹内会生成baidu.py文件：
  
  ```python
  import scrapy
  
  class BaiduSpider(scrapy.Spider):
      name = 'baidu'  # 爬虫的名字SPIDER_NAME
      allowed_domains = ['baidu.com']  # 允许进行解析的域名DOMAIN，其他域名会被过滤掉
      start_urls = ['http://baidu.com/']  # 起始的解析网址
  
      # 对网址具体的解析操作
      def parse(self, response):
          pass
  ```
  
  

## Items

- 可以在items.py中声明需要爬取的字段，如

  ```python
  import scrapy
  
  # 定义一个个人信息的类
  class PersonItem(scrapy.Item):
      # define the fields for your item here like:
      name = scrapy.Field()
      sex = scrapy.Field()
      age = scrapy.Field()
  ```

###  使用

- 在spider中创建一个该类（PersonItem）的对象即可

  ```python
  import scrapy
  
  class ExampleSpider(scrapy.Spider):
      name = "example"
      allowed_domains = ['example.com']
      start_urls = ['http://example.com']
      
      def parse(self, response):
          item = PersonItem()
          # extract()与extract_first()联系与区别请自行搜索
          item["name"] = response.xpath("").extract_first()
          item["sex"] = response.xpath("").extract_first()
          item["age"] = response.xpath("").extract_first()
          
          yield item # 会传到pipeline进行处理
  ```

  

## Pipeline

- 可以定义多个pipeline的场景
  1. 有多个spider，不同的pipeline处理不同item的内容
  2. 一个spider的内容可能要做不同的操作，比如存入不同的数据库等

### 使用pipeline

1. 在pipelines.py中定义pipeline类

   ```python
   class MyspiderPipeline:
       def process_item(self, item, spider): # 注意方法名固定，item为从spider接收到的数据，spider代表爬虫类本身，可以通过spider.name获取爬虫的名字，spider.settings.get["NAME"]获取settings中定义的字段信息等，其他方法请自行搜索
           # 对数据item进行处理
           return item  # 如果有其他pipeline，则会传给优先级比这个低的其他pipeline继续处理
   ```

2. 在配置文件中声明

   ```python
   # Configure item pipelines
   # See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
   ITEM_PIPELINES = {
       'myspider.pipelines.MyspiderPipeline': 300,
       # 'myspider.pipelines.MyspiderPipeline2': 301,
   }
   ```

   **==pipeline的权重越小优先级越高==**

### pipeline类的常用方法

- 此处以将接收到的item信息存入json文件中为例

```python
import json

class JsonWriterPipeline:
    def open_spider(self, spider):  # 仅爬虫开启的时候运行一次
        self.file = open(spider.settings.get["SAVE_FILE"], 'w')
        
    def close_spider(self, spider):  # 仅爬虫结束的时候运行一次
        self.file.close()
        
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item  # 不return时其他权重较低的pipeline获取不到item
```



## CrawlSpider

### 简介

- crawlspider是Spider的派生类(一个子类)，Spider类的设计原则是只爬取start_url列表中的网页，而CrawlSpider类定义了一些规则(rule)来提供跟进link的方便的机制，从爬取的网页中获取link并继续爬取的工作更适合。

### 使用

1. 创建项目

   ```shell
   scrapy startproject <PROJECT_NAME>
   ```

2. 创建爬虫

   ```shell
   cd <PROJECT_NAME>
   scrapy genspider -t crawl <SPIDER_NAME> <DOMAIN>  # 爬虫名字，域名
   ```

3. 指定start_url

4. 完善Rules

### 爬虫文件详解

**==CrawlSpider类和Spider类的最大不同是CrawlSpider多了一个rules属性，其作用是定义”提取动作“。在rules中可以包含一个或多个Rule对象，在Rule对象中包含了LinkExtractor对象。==**

```python
# -*- coding: utf-8 -*-
import scrapy
# 导入CrawlSpider相关模块
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# 表示该爬虫程序是基于CrawlSpider类的
class CrawldemoSpider(CrawlSpider):
    name = 'crawlDemo'    #爬虫文件名称
    start_urls = ['http://www.example.com/']
    
    #连接提取器：会去起始url响应回来的页面中提取指定的url
    link = LinkExtractor(allow=r'')
    #rules元组中存放的是不同的规则解析器（封装好了某种解析规则）。如果多个Rule都满足某一个url，会选择rules中第一个Rule
    rules = (
        #规则解析器：可以将连接提取器提取到的所有连接表示的页面进行指定规则（回调函数）的解析
        Rule(link, callback='parse_item', follow=True),
    )
    # 解析方法
    def parse_item(self, response):
        #print(response.url)
        pass
```

#### 参数介绍

- LinkExtractor：连接提取器,用于提取response中符合规则的链接

  > LinkExtractor(
  >  	allow=r'Items/'，# 满足括号中“正则表达式”的值会被提取，如果为空，则全部匹配。
  > 	 deny=xxx,  # 满足正则表达式的则不会被提取。
  >  	restrict_xpaths=xxx, # 满足xpath表达式的值会被提取
  >  	restrict_css=xxx, # 满足css表达式的值会被提取
  >  	deny_domains=xxx, # 不会被提取的链接的domains。 　
  >  )

- Rule：规则解析器，根据制定规则从连接提取器输出的链接中解析网页内容

  > Rule(
  >
  > ​	LinkExtractor(allow=r'Items/'),   # 指定链接提取器
  >
  > ​	callback='parse_item',   # 指定规则解析器解析数据的规则（回调函数）
  >
  > ​	follow=True   # 是否将链接提取器继续作用到链接提取器提取出的链接网页中,默认值为true
  >
  > )

**注**：

1. CrawlSpider中不能再有以parse为名字的方法，该方法被用来实现基础的url提取等功能



### 糗事百科示例

1. 爬虫文件

   ```python
   # -*- coding: utf-8 -*-
   import scrapy
   from scrapy.linkextractors import LinkExtractor
   from scrapy.spiders import CrawlSpider, Rule
   from qiubaiBycrawl.items import QiubaibycrawlItem
   import re
   class QiubaitestSpider(CrawlSpider):
       name = 'qiubaiTest'
       #起始url
       start_urls = ['http://www.qiushibaike.com/']
   
       #定义链接提取器，且指定其提取规则
       page_link = LinkExtractor(allow=r'/8hr/page/\d+/')
       
       rules = (
           #定义规则解析器，且指定解析规则通过callback回调函数
           Rule(page_link, callback='parse_item', follow=True),
       )
   
       #自定义规则解析器的解析规则函数
       def parse_item(self, response):
           div_list = response.xpath('//div[@id="content-left"]/div')
           
           for div in div_list:
               #定义item
               item = QiubaibycrawlItem()
               #根据xpath表达式提取糗百中段子的作者
               item['author'] = div.xpath('./div/a[2]/h2/text()').extract_first().strip('\n')
               #根据xpath表达式提取糗百中段子的内容
               item['content'] = div.xpath('.//div[@class="content"]/span/text()').extract_first().strip('\n')
   
               yield item #将item提交至管道
   ```

   

2. items文件

   ```python
   # -*- coding: utf-8 -*-
   
   # Define here the models for your scraped items
   #
   # See documentation in:
   # https://doc.scrapy.org/en/latest/topics/items.html
   
   import scrapy
   
   
   class QiubaibycrawlItem(scrapy.Item):
       # define the fields for your item here like:
       # name = scrapy.Field()
       author = scrapy.Field() #作者
       content = scrapy.Field() #内容
   ```

   

3. pipeline文件

   ```python
   # -*- coding: utf-8 -*-
   
   # Define your item pipelines here
   #
   # Don't forget to add your pipeline to the ITEM_PIPELINES setting
   # See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
   
   class QiubaibycrawlPipeline(object):
       
       def __init__(self):
           self.fp = None
           
       def open_spider(self,spider):
           print('开始爬虫')
           self.fp = open('./data.txt','w')
           
       def process_item(self, item, spider):
           #将爬虫文件提交的item写入文件进行持久化存储
           self.fp.write(item['author']+':'+item['content']+'\n')
           return item
       
       def close_spider(self,spider):
           print('结束爬虫')
           self.fp.close()
   ```

   

## scrapy模拟登录

### 模拟登录的方式

- requests：

  1. 直接携带cookies请求页面
  2. 找借口发送post请求存储cookie

- selenium：

  找到对应的input标签，输入文字点击登录

- scrapy

  1. 直接携带cookie
  2. 找到发送post请求的url地址，带上信息，发送请求

### start_url的处理逻辑

scrapy.Spider部分源码如下：

```python
from scrapy.http import Request

    def start_requests(self):
        cls = self.__class__
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)")
        if method_is_overridden(cls, Spider, 'make_requests_from_url'):
            warnings.warn(
                "Spider.make_requests_from_url method is deprecated; it "
                "won't be called in future Scrapy releases. Please "
                "override Spider.start_requests method instead (see %s.%s)." % (
                    cls.__module__, cls.__name__
                ),
            )
            for url in self.start_urls:
                yield self.make_requests_from_url(url)
        else:
            for url in self.start_urls:
                yield Request(url, dont_filter=True)
                
    def make_requests_from_url(self, url):
        """ This method is deprecated. """
        warnings.warn(
            "Spider.make_requests_from_url method is deprecated: "
            "it will be removed and not be called by the default "
            "Spider.start_requests method in future Scrapy releases. "
            "Please override Spider.start_requests method instead."
        )
        return Request(url, dont_filter=True)    
```

我们定义在spider下的start_url=[]都是交给==start_requests==处理的。必要时可以重写这个方法。



### 重写start_url实现模拟登录【例】

```python
import scrapy

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/user/profile']  # 示例网址，此处需要替换成实际的信息页地址
    
    # 重写start_requests方法
    def start_requests(self):
        # 这里的cookie拿的是我的b站的cookie，“=”后面的信息我做了修改。请按实际替换成自己的cookie
        cookies = "_uuid=151A8F2AD9460689infoc; buvid3=3D303838-7355-4B505FA155825infoc; sid=12r1g; DedeUserID=7544; DedeUserID__ckMd5=26d8ad82ab; SESSDATA=a13de69%2C21379*61; bili_jct=09d7836772af9; CURRENT_FNVAL=16; rpdid=|(J~R~lmJ|l)Y)k; LIVE_BUVID=AUT8415; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1590,1505; bp_video_offset_72290544=41303; bp_t_offset_72290544=413503; CURRENT_QUALITY=64; PVID=1"
        # 格式
        cookies = {i.split('=')[0]:i.split('=')[1] for i in cookies.split(';')}
        yield scrapy.Request(
        	self.start_urls[0],
            callback = self.parse,
            cookies = cookies
        )
        
    def parse(self, response):
        # 具体的页面解析逻辑
        pass
```

### cookie在不同解析函数之间传递

- cookie在settings.py中默认是开启的，这是cookie在不同解析函数之间传递的前提

  > ```python
  > # Disable cookies (enabled by default)
  > #COOKIES_ENABLED = False
  > ```

- 在settings中添加COOKIES_DEBUG = TRUE 可以在终端显示cookie的信息。

  > [scrapy.downloadermiddlewares.==cookies==] ==DEBUG:  Sending cookies to:==
  >
  > <GET http://www.example.com>
  >
  > Cookie:  _uuid=151A8F2AD9460689infoc; buvid3=3D303838-7355-4B505FA155825infoc; ......

### 发送post请求

- 使用scrapy.Request时发送的是GET请求，发送POST请求需要使用**scrapy.FormRequest**，同时使用formdata来携带需要post的数据。

  ```python
  class ExampleSpider(scrapy.Spider):
      name = 'example'
      allowed_domains = ['example.com']
      start_urls = ['https://example.com/login']
      headers = {
          "Accept": "*/*",
          "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh,q=0.4"
      }
      
      def parse(self, response):
          # 表单需要的其他字段获取，可以通过xpath，如 
          authenticity_token = response.xpath("//input[@name='authenticity_token']/@value").extract_first()
          return scrapy.FormRequest(
          	"https://example.com/session", # 根据具体的请求信息而定
              formdata=dict(
              	login="user",
                  password="123456",
                  authenticity_token=authenticity_token
              ),
              callback=self.after_login
          )
      
      def after_login(self, response):
          # 登陆后做的事情
          pass
  ```

  

### 自动登录

```python
class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['https://example.com/login']
    
    def parse(self, response):
        yield scrapy.FormRequest.form_response(
        	response, # 自动从响应中找到form表单进行登录
            formdata={"email":"user_name","password":"password"},
            callback=self.after_login
        )
        
    def after_login(self, response):
        # 登陆后做的事情
        pass
```



## Middlewares

### 使用方法：

编写一个类，然后在settings中开启。

【例】

MyspiderDownloaderMiddleware类(创建爬虫时默认生成的)：

```python
class MyspiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
```

settings.py

```python
# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'myspider.middlewares.MyspiderDownloaderMiddleware': 543,
}
```

### 应用

#### （一）随机UA

- 添加自定义的UA，给request的headers["User-Agent"]赋值即可

1. 在settings中声明一个USER_AGENT_LIST

   ```python
   USER_AGENT_LIST = [
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
       "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
       "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"]
   ```

2. 在middlewares.py中定义RandomUserAgent类

   ```python
   import random
   
   class RandomUserAgentMiddleware:
       
       def process_request(self, request, spider):
           user_agent = random.choice(spider.settings.get["USER_AGENT_LIST"])
           request.headers['User-Agent'] = user_agent
   
   # 验证随机ua是否生效，在终端输出每次请求的ua
   class CheckUserAgentMiddleware:
       def process_response(self, request, reponse, spider):
           print(request.headers["User-Agent"])
           return response
   ```

3. 在settings中声明middleware

   ```python
   DOWNLOADER_MIDDLEWARES = {
      'myspider.middlewares.RandomUserAgentMiddleware': 543,
      'myspider.middlewares.CheckUserAgentMiddleware': 544,
   }
   ```

   

#### （二）设置代理

- 添加代理，需要在request的meta信息中添加proxy字段。代理的形式为：协议+ip+端口。

  ```python
  class ProxyMiddleware:
      def process_request(self, request, spider):
          request.meta["proxy"] = "http://1.2.3.4:8888"
  ```

- 添加检验代理有效性

（待完善）

- 加密代理

（待完善）

## settings文件的认识

- 此处以创建的myspider项目为例：

```python
# Scrapy settings for myspider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'myspider'

SPIDER_MODULES = ['myspider.spiders']
NEWSPIDER_MODULE = 'myspider.spiders'

# 过滤控制台输出日志级别
LOG_LEVEL = "DEBUG"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'myspider (+http://www.yourdomain.com)'

# 是否遵循robots.txt规则
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# 请求头的设置
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# 启用自定义的SPIDER_MIDDLEWARES
#SPIDER_MIDDLEWARES = {
#    'myspider.middlewares.MyspiderSpiderMiddleware': 543,
#}

# 启用自定义的DOWNLOADER_MIDDLEWARES
#DOWNLOADER_MIDDLEWARES = {
#    'myspider.middlewares.MyspiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# 启用自定义的pipeline
#ITEM_PIPELINES = {
#    'myspider.pipelines.MyspiderPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
```



## scrapy shell

- scrapy shell 是一个交互终端，可以在未启动spider的情况下尝试以及调试代码，也可用来测试xpath表达式

- 使用方法 scrapy shell https://www.baidu.com/

  > response.url：当前响应的url
  >
  > response.request.url：当前响应对应的请求的url
  >
  > response.headers：响应头
  >
  > response.body：响应体
  >
  > response.request.headers：当前响应的请求头
  >
  > ......



## scrapy-redis





# Scrapyd && Logparser

## Scrapyd快速入门
### 简介：

- [Github地址](https://github.com/scrapy/scrapyd)
- [官方文档](http://scrapyd.readthedocs.org/)

1. Scrapy是用来运行scrapy爬虫的一个服务
2. 特点：允许部署scrapy项目并且通过HTTP JSON的方式来控制爬虫
3. 对scrapy的理解：
   - scrapyd其实是一个服务器端的服务，真正部署爬虫的时候需要两个东西：
     - 服务器端：scrapyd
     - 客户端：scrapy-client

### 安装

#### 服务器端

```shell
pip install scrapyd
```

或

```shell
conda install scrapyd
```

#### 客户端

```shell
pip install scrapyd-client 
```

或

```shell
conda install scrapyd-client
```

### 运行

#### 试运行scrapyd查看可视化界面

命令行下输入scrapyd，正常运行后会有日志提示

>Scrapyd web console available at http://127.0.0.1:6800/

浏览器访问此默认地址即可查看可视化界面

#### 部署scrapy项目

在创建scrapy爬虫项目myspider后，修改scrapy.cfg配置文件默认如下：

> ```python
> [settings]
> default = myspider.settings # myspider为创建的scrapy项目名称
> 
> [deploy:server_name] # 为服务器指定一个名字，这里为server_name
> url = http://localhost:6800/ # 部署项目的服务器地址，此处为本地部署
> project = myspider # 工程名myspider
> # 实际上产环境下需要验证登录scrapyd服务器
> # username = ***
> # password = ***
> ```

进入爬虫根目录，即有scrapy.cfg文件的一级，运行

```shell
scrapyd-deploy <target> -p <project>  # target为配置的服务器名字，project为项目名称
```

这里对应配置文件即为：

```shell
scrapyd-deploy server_name -p myspider
```

查看部署结果：

```shell
scrapyd-deploy -L <服务器名称>
```

或者查看http://localhost:6800/页面

**注:** *部署操作会打包当前项目，如果当前项目下有setup.py文件，就会使用其中的配置，没有就会自动创建一个(后期可以根据自己的需要修改里面的信息，也可以暂时不管它) 。从返回的结果里面，我们可以看到部署的状态，项目名称，版本号和爬虫个数，以及当前的主机名称*

**到现在只是部署成功，还没有启动爬虫**

#### 使用API管理爬虫

官方推荐使用curl来管理爬虫。Windows[安装地址](https://curl.haxx.se/download.html)。

##### 查看服务器端状态

```shell
curl http://localhost:6800/daemonstatus.json
```

##### 启动爬虫：

```shell
curl http://localhost:6800/schedule.json -d project=PROJECT_NAME -d spider=SPIDER_NAME
```

下载可以进入http://localhost:6800/查看

##### 停止一个爬虫：

```shell
curl http://localhost:6800/cancel.json -d project=PROJECT_NAME -d job=JOB_ID
```

启动爬虫时会输出的信息中会包含有JOB_ID

##### 列出项目

```shell
curl http://localhost:6800/listprojects.json
```

##### 列出爬虫、版本、job信息

```shell
curl http://localhost:6800/listspiders.json?project=PROJECT_NAME
```

##### 删除爬虫项目

```shell
curl http://localhost:6800/delproject.json -d project=PROJECT_NAME -d job=JOB_ID
```



## Logparser

### 简介

- [Github](https://github.com/my8100/logparser)

- 在scrapyweb中解析scrapyd的日志
- logparser库的工作原理是每隔一段时间（默认10s）查看一下日志文件夹，然后解析，并生成stats.json文件。scrapyd在开启了端口后可以访问scrapyd的目录，因此可以在不修改scrapyd的情况下对日志解析

### 使用

#### 安装

```shell
pip install logparser
```

或者

```shell
git clone https://github.com/my8100/logparser.git
cd logparser
python setup.py install
```

#### 作为service运行

##### 通过命令启动

```shell
logparser
```

##### 查看当前状态

http://127.0.0.1:6800/logs/stats.json

##### 获取某个爬虫人物的日志分析详情

http://127.0.0.1:6800/logs/projectname/spidername/jobid.json