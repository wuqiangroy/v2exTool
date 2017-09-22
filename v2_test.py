#!usr/bin/env python
# _*_ coding:utf-8 _*_


import v2extool
v2extool.use_proxy("61.160.208.222:8080")
v2extool.login("wuqiangroy", "123321")
v2extool.balance()
v2extool.check_in()
# v2extool.article_info(123)
v2extool.node_content("apple")
v2extool.user_info(user_id=123)
