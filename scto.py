import json
import requests
import os

# 请求头
headers = {
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.34(0x18002230) NetType/WIFI Language/zh_CN",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept-Language": "en-us,en",
    "Accept": "application/json, text/javascript, */*; q=0.01"
}


def login(email, pass_word):
    loginUrl = "https://www.sctocloud.com/auth/login"
    session = requests.session()

    data = {
        "email": email,
        "passwd": pass_word,
        "remember_me": "on"
    }
    response = session.post(url=loginUrl, json=data)
    res = json.loads(response.text)
    if res["ret"] == 1:
        print(res["msg"])

        header_str = response.headers["Set-Cookie"]

        return header_str
    else:
        print("登录失败，结果-->", res)
        return None


def check(headers_str):
    check_url = "https://www.sctocloud.com/user/checkin"
    session = requests.session()

    headers["cookie"] = headers_str
    response = session.post(url=check_url, headers=headers)
    res = json.loads(response.text)
    print(res)


def analysis(s: str):
    s = s.replace(",", ";").replace(" ", "").split(";")
    b = {}
    for i in s:
        try:
            tmp = i.split("=")
            b[tmp[0]] = tmp[1]
        except:
            pass
    return f"uid={b['uid']}; " \
           f"email={b['email']}; " \
           f"expire_in={b['expire_in']}; " \
           f"ip={b['ip']}; " \
           f"key={b['key']};"


if __name__ == "__main__":
    user_list = os.environ.get('USER', '').split('\n')

    email = user_list[0]
    password = user_list[1]

    cookies_str = login(email, password)
    header_str = analysis(cookies_str)
    print(header_str)
    check(header_str)