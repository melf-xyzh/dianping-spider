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
   爬虫
"""
import random
import time
from datetime import datetime

import urllib3
from bs4 import BeautifulSoup

from utils.bs4_filter import Bs4Filter
from utils.mongo import MongoDB
from utils.user_agent import create_user_agent, choice_cookie


class Crawler:
    def __init__(self, city="xian"):
        self.http = urllib3.PoolManager(timeout=5)
        self.user_agent = create_user_agent()
        self.cookie = choice_cookie()
        self.city = city
        self.mongodb = MongoDB()

    def get_html(self, url):
        """
        获取网址的html代码
        :param url: url
        :return:
        """
        self.cookie = choice_cookie()
        self.user_agent = create_user_agent()

        print("正在请求：{}".format(url))
        # 创建一个请求
        r = self.http.request(
            method='GET',
            url=url,
            headers={
                'User-Agent': self.user_agent,
                'Cookie': self.cookie,
            }
        )
        print("请求成功")
        # 获取HTML源码
        html = r.data.decode()

        if r.status != 200 and r.status != "200":
            raise Exception("请求失败，请检查网络连接和Cookie")
        return html

    def get_soup(self, url):
        """
        获取煲汤之后的html代码
        :param url: url
        :return:
        """
        html = self.get_html(url)
        # 使用BeautifulSoup煲汤
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def get_category_tags_in_index(self):
        """
        获取大众点评主页的分类标签地址
        :return:
        """
        # 拼接请求url
        url = "https://www.dianping.com/" + self.city + "/"
        # 获取煲汤后的res
        soup = self.get_soup(url)
        # 获取网站标题
        title = soup.title.text
        # 获取本页面所有分类标签
        a_l = soup.find_all(Bs4Filter.shop_index_title_filter)
        # 建立list存取分类标签
        category_tags = []
        # 标签分类标签
        for a in a_l:
            href = a['href']
            if self.city in href:
                # 创建字典保存每一对标签
                tag_dict = {
                    'title': title,
                    'name': a.contents[0].getText(),
                    'href': a['href'],
                    'create': datetime.now(),
                    'is_finish': False,
                }
                # print(tag_dict)
                category_tags.append(tag_dict)
                # 将商铺标签插入数据库
                self.mongodb.add_category_tags(tag_dict)
        return category_tags

    def get_category_tags_in_second_index(self, url):
        """
        获取大众点评二级页面的分类标签地址
        :param url:
        :return:
        """
        # 获取煲汤后的res
        soup = self.get_soup(url)
        # 获取网站标题
        title = soup.title.text
        if title == "验证中心":
            # raise Exception("已触发美团的反爬机制，请更换Cookie")
            print("已触发美团的反爬机制，请更换Cookie")
            return None

            # 获取本页面所有分类标签
        a_l = soup.find_all(Bs4Filter.shop_index_title_filter)
        # 建立list存取分类标签
        category_tags = []
        # 遍历分类标签
        for a in a_l:
            href = a['href']
            if self.city in href and "/ch" in href:
                # 创建字典保存每一对标签
                tag_dict = {
                    'title': title,
                    'name': a.contents[0].getText(),
                    'href': a['href'],
                    'create': datetime.now(),
                    'is_finish': False,
                }
                print(tag_dict)
                category_tags.append(tag_dict)
                # 将商铺标签插入数据库
                self.mongodb.add_category_tags(tag_dict)
        # 标记该页面已经成功请求
        self.mongodb.finish_category_tag(url)
        return category_tags

    def get_shop_id_list(self, url, pages=50):
        """
        获取商铺列表
        :param url:
        :param pages:
        :return:
        """
        shop_list_sum = []
        # 翻页查询
        for page in range(1, pages + 1):
            # 拼接url
            url_i = url + "/p" + str(page)
            # 获取煲汤后的shop
            soup = self.get_soup(url_i)
            # 获取网站标题
            title = soup.title.text
            # 获取本页面所有分类标签
            a_l = soup.find_all(Bs4Filter.shop_id_filter)

            # 商铺列表
            shop_list = []
            # 遍历筛选后的a标签
            for a in a_l:
                href = a['href']
                name = a['title'],
                if isinstance(name, tuple):
                    name = name[0]

                # print(len(name))
                if 'shop' in href and name != "" and name != " ":
                    # 创建字典保存每一对标签
                    shop_dict = {
                        'base_url': url,
                        'url': url_i,
                        'title': title,
                        'shop_id': a['data-shopid'],
                        'href': href,
                        'name': name,
                        'create': datetime.now(),
                        'is_finish': False,
                    }
                    shop_list.append(shop_dict)

                    shop_list_sum.append(shop_dict)
            self.mongodb.add_shop(shop_list)
        self.mongodb.finish_category_tag(url)
        return shop_list_sum


if __name__ == '__main__':
    crawler1 = Crawler()
    category_tags = crawler1.get_category_tags_in_index()
    for category_tag in category_tags:
        if crawler1.mongodb.is_finish_category_tag(category_tag['href']):
            print("已访问：{}".format(category_tag['href']))
        else:
            try:
                crawler1.get_category_tags_in_second_index(category_tag['href'])
                time.sleep(random.randint(3, 10))
            except:
                print("跳过访问")
