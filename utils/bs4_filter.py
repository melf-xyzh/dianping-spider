# -*- coding: utf-8 -*-
"""
@Time       :2021/11/14 9:05
@Author     :MELF晓宇
@Email      :xyzh.melf@petalmail.com
@ProjectName:dianping-spider
@FileName   :bs4_filter.py
@Blog       :https://blog.csdn.net/qq_29537269
@Guide      :https://guide.melf.space
@Information:
    BeautifulSoup过滤器
"""


class Bs4Filter:
    @staticmethod
    def shop_category_tags_filter(tag):
        """
        bs4过滤器(商铺分类标签过滤器)
        :param tag:
        :return: 返回
        """
        return tag.has_attr('data-cat-id')

    @staticmethod
    def shop_index_title_filter(tag):
        """
        bs4过滤器(一级分类过滤器)
        :param tag:
        :return:
        """
        return tag.has_attr('data-click-name') and tag.has_attr('href')

    @staticmethod
    def shop_id_filter(tag):
        """
        bs4过滤器(shopID过滤器)
        :param tag:
        :return:
        """
        return tag.has_attr('data-shopid') and tag.has_attr('href') and tag.has_attr('title')
