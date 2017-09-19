import re
import requests


class v2extool:

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
        "referer": "https://www.v2ex.com/signin" 
    }
    session = requests.session()

    def login(self, username, password):
        login_url = "https://www.v2ex.com/signin"
        data = {"username": username, "password": password}
        res = self.session.post(url=login_url, data=data)
        print(res.text.encode().decode())
    
    @property
    def check_in(self):
        check_in_url = "https://www.v2ex.com/mission/daily"
        res = self.session.get(check_in_url)
        if "每日登录奖励已领取" in res.text.encode().decode():
            print("error: you have been already checked in")
            return False
        resp = self.session.get('http://v2ex.com' + re.search(r'/mission/daily/redeem\?once=\d+', res.text).group())
        if resp.ok:
            print("success: you just checked in success!")
            return True
    


if __name__ == "__main__":
    v = v2extool()
    v.login(username="wuqiangroy", password="123321")

