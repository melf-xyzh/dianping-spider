# -*- coding: utf-8 -*-
"""
@Time       :2021/11/14 8:54
@Author     :MELF晓宇
@Email      :xyzh.melf@petalmail.com
@ProjectName:dianping-spider
@FileName   :user_agent.py
@Blog       :https://blog.csdn.net/qq_29537269
@Guide      :https://guide.melf.space
@Information:
   
"""
import random

from fake_useragent import UserAgent

from constants import COOKIE_LIST


def create_user_agent():
    """
    随机生成User-Agent
    :return: 随机生成的User-Agent
    """
    ua = UserAgent().random
    return ua


def choice_cookie():
    """
    随机选择一个cookie
    :return:
    """
    cookie = random.choice(COOKIE_LIST)
    return cookie
