import re
import requests
from config import headers, main_url, login_url, check_in_url, user_info_url


class v2extool:
    """main func"""

    session = requests.session()

    def login(self, username, password):
        data = {"username": username, "password": password}
        res = self.session.post(url=login_url, data=data)
        print(res.text.encode().decode())
    
    @property
    def check_in(self):
        res = self.session.get(check_in_url)
        if "每日登录奖励已领取" in res.text:
            print("error: you have been already checked in")
            return False
        resp = self.session.get(main_url + re.search(r'/mission/daily/redeem\?once=\d+', res.text).group())
        if resp.ok:
            print("success: you just checked in success!")
            return True
    
    def user_info(self, username=None, user_id=None):
        if not (username or user_id):
            raise TypeError("You must type one params: usernae or user_id")
        user_url = user_info_url + "?username={}&id={}".format(username, user_id)
        res = requests.get(user_url)
        print(res.json())
        return True

if __name__ == "__main__":
    v = v2extool()
    v.login(username="wuqiangroy", password="123321")
    # v.check_in
    # v.user_info("wuqiangroy")

