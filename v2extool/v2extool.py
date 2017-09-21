
import re
import json
import requests
from bs4 import BeautifulSoup
from v2extool.error import *
from v2extool.config import headers, main_url, login_url, check_in_url, user_info_url, balance_url


def access_deny(proxy=""):
    """It's a decorator to detect if ip blocked by v2ex"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            res = requests.get(main_url, proxies=proxy, timeout=10)
            if "Access Denied" in res.text:
                print(access_denied)
                return False
            return func(*args, **kwargs)
        return wrapper
    return decorator


class v2extool:
    """main func"""

    session = requests.session()
    proxy = {"https": "http://61.160.208.222:8080"}
    # proxy = ""

    def login(self, username, password):

        html = self.session.get(login_url, proxies=self.proxy, timeout=10).text
        if "Access Denied" in html:
            print(access_denied)
            return False
        soup = BeautifulSoup(html, "html.parser")
        param = soup.find_all("input")
        data = {
            param[1]["name"]: username,
            param[2]["name"]: password,
            param[3]["name"]: param[3]["value"],
            param[5]["name"]: param[5]["value"]
        }
        res = self.session.post(url=login_url, params=data, headers=headers, proxies=self.proxy, timeout=10)
        if "登录有点问题，请重试一次" in res.text:
            print(login_failed)
            return False
        else:
            print(login_success)
            return True

    @property
    def check_in(self):
        res = self.session.get(check_in_url, proxies=self.proxy, timeout=10)

        if "你要查看的页面需要先登录" in res.text:
            print(login_required)
            return False

        if "每日登录奖励已领取" in res.text:
            print(checked_in)
            return False
        daily_redeem = main_url + re.search(r'/mission/daily/redeem\?once=\d+', res.text).group()
        resp = self.session.get(daily_redeem, proxies=self.proxy, timeout=10)
        if resp.ok:
            print(check_in_success)
            return True
        else:
            print(check_in_failed)
            return False

    def user_info(self, username=None, user_id=None):
        if not (username or user_id):
            raise TypeError("You must type one params: username or user_id")
        user_url = user_info_url + "?username={}&id={}".format(username, user_id)
        res = requests.get(user_url, proxies=self.proxy, timeout=10)
        print(res.json())
        return True

    def node_content(self, node_name="tech"):

        if not isinstance(node_name, str):
            raise ValueError("node name must be strings")

        content = []
        if node_name in ["tech", "creative", "play", "apple", "jobs", "deals", "city", "qna", "hot", "all", "r2",
                         "nodes", "members"]:
            res = self.session.get(main_url + "/?tab={}".format(node_name), proxies=self.proxy, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            items = soup.find_all(attrs={"class": "cell item"})
            for item in items:
                data = item.find("span")
                content.append({
                    "node_name": node_name,
                    "article_id": re.search(r"\d+", str(data)).group(),
                    "article_name": data.text,
                    "reply_num": re.search(r"reply\d+", str(data)).group()[5:],
                    "author": item.find("strong").text
                })
            print(content)
            return content
        else:
            res = self.session.get(main_url + "/go/{}".format(node_name), proxies=self.proxy, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            items = soup.find_all(attrs={"class": re.compile(r'^cell from')})
            for item in items:
                data = item.find(attrs={"class": "item_title"})
                content.append({
                    "node_name": node_name,
                    "article_id": re.search(r"\d+", str(data)).group(),
                    "article_name": data.text,
                    "reply_num": re.search(r"reply\d+", str(data)).group()[5:],
                    "author": item.find("strong").text
                })
            print(content)
            return content

    def article_info(self, article_id):

        try:
            int(article_id)
        except ValueError as e:
            raise ValueError("article_id must be an int or all numeric strings")
        article_detail = {}
        reply_content = []
        res = self.session.get(main_url + "/t/{}".format(str(article_id)), proxies=self.proxy, timeout=10)
        if "主题未找到" in res.text:
            print(topic_not_found)
            return False
        soup = BeautifulSoup(res.text, "html.parser")
        data = soup.find(attrs={"class": "gray"}).text.split("·")
        content = soup.find(attrs={"class": "markdown_body"}).text
        author = data[0]
        publish_time = data[1]
        views = data[2]
        title = soup.find("h1").text
        article_detail.update({
            "article_id": article_id,
            "url": main_url + "/t/{}".format(str(article_id)),
            "title": title,
            "author": author,
            "publish_time": publish_time,
            "content": content,
            "views": views,
            "reply": reply_content
        })
        items = soup.find_all(attrs={"class": "cell"})
        print(items)
        for index in range(3, len(items)):
            reply_content.append({
                "reply_content": items[index].find(attrs={"class": "reply_content"}).text,
                "reply_author": items[index].find("strong").text,
                "create_time": items[index].find(attrs={"class": "ago"}).text,
                "rank": items[index].find(attrs={"class": "no"}).text
            })
        article_detail.update({"reply_content": reply_content})
        print(json.dumps(article_detail))

    @property
    def balance(self):
        """show your balance"""
        res = self.session.get(balance_url, proxies=self.proxy, timeout=10)
        if "你要查看的页面需要先登录" in res.text:
            print(login_required)
            return False
        balance = []
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.find_all(attrs={"class": "d"})
        total = items[3].text
        balance.append({"total_balance": total})
        for i in range(0, len(items), 5):
            balance.append({"time": items[i].text[:-7], "info": items[i+4].text})
        print(balance)
        return balance


if __name__ == "__main__":
    v = v2extool()
    v.login(username="wuqiangroy", password="123321")
    # v.check_in
    # v.user_info("wuqiangroy")
    # v.node_content("share")
    # v.article_info(391903444)
    v.balance()

