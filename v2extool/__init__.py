#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from .main_func import V2exTool

v2extool = V2exTool()


def login(username, password):
    return v2extool.login(username, password)


def balance():
    return v2extool.balance


def check_in():
    return v2extool.check_in


def user_info(username=None, user_id=None):
    return v2extool.user_info(username, user_id)


def node_content(node_name="tech"):
    return v2extool.node_content(node_name)


def use_proxy(ip=None, port=None):
    return v2extool.use_proxy(ip, port)


# def article_info(article_id):
#     return v2extool.article_info(article_id)
