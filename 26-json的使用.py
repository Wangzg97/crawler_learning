import json

str = '{"name": "盗梦空间" }'
print(type(str))

obj = json.loads(str)  # 转换成json对象
print(type(obj), ":", obj)

str2 = json.dumps(obj, ensure_ascii=False)  # 把json对象转换成字符串
print(type(str2), ":", str2)

json.dump(obj, open("movie.txt", "w", encoding="utf-8"), ensure_ascii=False)  # 把对象写入到文件中

str3 = json.load(open("movie.txt", encoding='utf-8'))  # 读取文件
print(str3)
