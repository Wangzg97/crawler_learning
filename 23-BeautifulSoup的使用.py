from bs4 import BeautifulSoup
from bs4.element import Comment

str = '''
<title id="title">测试</title>
<div class='info' float='left'>Welcome</div>
<div class='info' float='right'>
    <span>Good Good Study</span>
    <a href='www.baidu.com'></a>
    <strong><!--此处是注释--></strong>
</div>
'''

print("----------------解析html---------------")
soup = BeautifulSoup(str, 'lxml')
print(soup.title)
print(soup.div)
print(type(soup.div.string))
print(soup.div.string)
print(soup.div.attrs)
print(soup.div['class'])
print(soup.span.string)
print(soup.span.text)
print(soup.a['href'])
print(soup.strong.string)
print(soup.strong.text + "**")

if type(soup.strong.string) == Comment:
    print(type(soup.strong.string))
    print(soup.strong.string)
    print(soup.strong.prettify())
else:
    print(soup.strong.text)

print("----------------find_all---------------")
print(soup.find_all('title'))
print(soup.find_all(id='title'))
print(soup.find_all("div"))
print(soup.find_all(class_='info'))
print(soup.find_all(attrs={"float": "left"}))

print("----------------css选择器---------------")
print(soup.select("title"))
print(soup.select("#title"))
print(soup.select(".info"))
print(soup.select("div span"))
print(soup.select("div > span"))  # 注意要有空格
print(soup.select("div")[1].select("span"))
print(soup.select("title")[0].text)
