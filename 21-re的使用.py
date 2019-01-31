import re

str1 = "I Study Python3.6 Everyday"
print("------match------")
# 匹配第一个字符
m1 = re.match(r'I', str1)  # 指定字符
m2 = re.match(r'\w', str1)  # 数字字母下划线
m3 = re.match(r'.', str1)  # 任意一个字符
m4 = re.match(r'\D', str1)
m5 = re.match(r'i', str1, re.I)  # 不区分大小写
m6 = re.match(r'\S', str1)  # 非空白字符  \s 空格
# m = re.match(r'Study', str1)  匹配不到，因为re从左开始匹配
# print(m6.group())

print("------search------")
s1 = re.search(r'Study', str1)
s2 = re.search(r'S\w+', str1)
s3 = re.search(r'P\w+.\d', str1)  # \d 数字
# print(s3.group())

print("------findall------")
f1 = re.findall(r'y', str1)
print(f1)

print("-----------------test------------------")
str2 = '<div><a href="https://www.baidu.com">百度baidu</a></div>'
t1 = re.findall(r'<a href="https://www.baidu.com">(.+)</a>', str2)
t2 = re.findall(r'<a href="(.+)">', str2)
print(t1)

print("-----------------sub------------------")
sub1 = re.sub(r'<div>(.+)</div>', r'<span>\1</span>', str2)
print(sub1)



