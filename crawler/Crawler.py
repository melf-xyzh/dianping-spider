# -*- coding: utf-8 -*-
"""
@Time       :2021/11/14 8:50
@Author     :MELF晓宇
@Email      :xyzh.melf@petalmail.com
@ProjectName:dianping-spider
@FileName   :Crawler.py
@Blog       :https://blog.csdn.net/qq_29537269
@Guide      :https://guide.melf.space
@Information:
   
"""
import time

import urllib3
from bs4 import BeautifulSoup

from utils.bs4_filter import Bs4Filter
from utils.mongo import MongoDB
from utils.user_agent import create_user_agent, choice_cookie


class Crawler:
    @staticmethod
    def get_shop_list_page_url(url="https://www.dianping.com/xian/ch10"):
        print("正在发起请求:{}".format(url))
        http = urllib3.PoolManager(timeout=5)
        user_agent = create_user_agent()
        cookie = choice_cookie()

        # 创建一个请求
        r = http.request(
            method='GET',
            url=url,
            headers={
                'User-Agent': user_agent,
                'Cookie': cookie,
            }
        )
        print("请求成功")
        # 获取HTML源码
        html = r.data.decode()
        # print(html)

        if r.status != 200 and r.status != "200":
            raise Exception("请求失败，请检查网络连接和Cookie")

        # 使用BeautifulSoup煲汤
        soup = BeautifulSoup(html, "html.parser")

        # 获取本页面所有分类标签
        a_l = soup.find_all(Bs4Filter.shop_category_tags_filter)
        # print(a_l)
        category_tags = []
        for a in a_l:
            # 创建字典保存每一对标签
            tag_dict = {
                'name': a.contents[0].getText(),
                'href': a['href']
            }
            category_tags.append(tag_dict)

        return category_tags

    @staticmethod
    def get_shop_list_page_base_url(url="https://www.dianping.com/xian/"):
        print("正在发起请求")
        http = urllib3.PoolManager(timeout=5)
        user_agent = create_user_agent()
        cookie = choice_cookie()

        # 创建一个请求
        r = http.request(
            method='GET',
            url=url,
            headers={
                'User-Agent': user_agent,
                'Cookie': cookie,
            }
        )
        print("请求成功")
        # 获取HTML源码
        html = r.data.decode()
        # print(html)

        if r.status != 200 and r.status != "200":
            raise Exception("请求失败，请检查网络连接和Cookie")

        # 使用BeautifulSoup煲汤
        soup = BeautifulSoup(html, "html.parser")
        print(soup)

        # # 获取本页面所有分类标签
        a_l = soup.find_all(Bs4Filter.shop_index_title_filter)
        print(a_l)
        category_tags = []
        for a in a_l:
            # 创建字典保存每一对标签
            tag_dict = {
                'name': a.contents[0].getText(),
                'href': a['href']
            }
            category_tags.append(tag_dict)

        return category_tags


if __name__ == '__main__':
    # 获取Mongo实例
    mongo = MongoDB()

    # # 查询初始城市分类标签
    # category_tags = Crawler.get_shop_list_page_url()
    # print(category_tags)
    #
    # # 查询子项城市分类标签
    # for category_tag in category_tags:
    #     tags = Crawler.get_shop_list_page_url(category_tag["href"])
    #     time.sleep(3)
    #     mongo.data_save("商铺分类标签", tags)

    category_tags = Crawler.get_shop_list_page_base_url()
    mongo.data_save("商铺分类标签", category_tags)

    # 查询子项城市分类标签
    for category_tag in category_tags:
        tags = Crawler.get_shop_list_page_url(category_tag["href"])
        time.sleep(3)
        mongo.data_save("商铺分类标签", tags)
