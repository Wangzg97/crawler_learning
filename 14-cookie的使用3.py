from urllib.request import Request, HTTPCookieProcessor, build_opener
from urllib.parse import urlencode
from fake_useragent import UserAgent
from http.cookiejar import MozillaCookieJar

# 登录
# cookie存到文件中
def save_cookie():
    login_url = "https://u.njtech.edu.cn/cas/login"
    headers = {
        "User-Agent": UserAgent().chrome
    }
    form_data = {
        "username": "1401160226",
        "password": "w1401160226"
    }
    form_data = urlencode(form_data).encode()
    request = Request(login_url, headers=headers, data=form_data)
    cookie_jar = MozillaCookieJar()
    handler = HTTPCookieProcessor(cookie_jar)
    opener = build_opener(handler)
    response = opener.open(request)
    cookie_jar.save("cookie.txt", ignore_discard=True, ignore_expires=True)


# 从文件中读取cookie
# 访问页面
def get_cookie():
    info_url = "https://i.njtech.edu.cn/index.html"
    headers = {
        "User-Agent": UserAgent().chrome
    }
    request = Request(info_url, headers=headers)
    cookie_jar = MozillaCookieJar()
    cookie_jar.load("cookie.txt", ignore_discard=True, ignore_expires=True)
    handler = MozillaCookieJar(cookie_jar)
    opener = build_opener(handler)
    response = opener.open(request)
    print(response.read().decode())


if __name__ == '__main__':
    save_cookie()
    get_cookie()
