from urllib.request import Request, urlopen
from fake_useragent import UserAgent

url_base = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={}"
i = 0
while True:
    headers = {
        "User-Agent": UserAgent().chrome
    }
    request = Request(url_base.format(i * 20), headers=headers)
    response = urlopen(request)
    info = response.read().decode()
    if info == "" or info == None:
        break
    if i == 5:
        break
    print(info)
    i += 1
