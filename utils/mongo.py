# -*- coding: utf-8 -*-
"""
@Time       :2021/11/14 9:49
@Author     :MELF晓宇
@Email      :xyzh.melf@petalmail.com
@ProjectName:dianping-spider
@FileName   :mongo.py
@Blog       :https://blog.csdn.net/qq_29537269
@Guide      :https://guide.melf.space
@Information:
   
"""
from pymongo import MongoClient
from constants import MONGODB_HOST, MONGODB_POST, MONGODB_USER, MONGODB_PASSWORD, MONGODB_NAME


class MongoDB:
    def __init__(self):
        """
        初始化MongoDB类
        """
        self.host = MONGODB_HOST
        self.port = MONGODB_POST
        self.user = MONGODB_USER
        self.password = MONGODB_PASSWORD
        self.db_name = MONGODB_NAME
        self.db, self.client = self.get_mongo_client()

    def get_mongo_client(self):
        """
        获取数据库连接
        :return:数据库对象，数据库连接对象
        """
        try:
            # 连接MongoDB数据库,账号密码认证
            client = MongoClient(self.host, self.port)
            # 先连接系统默认数据库admin
            db = client.admin
            # 让admin数据库去认证密码登录，好吧，既然成功了，
            db.authenticate(self.user, self.password)
            # 再连接自己的数据库
            my_database = client[self.db_name]
            return my_database, client
        except:
            raise Exception("MongoDB连接异常")

    def data_save(self, set_name, data_dict):
        """
        将数据存入数据库
        :param data_dict: 要存入的数据（字典）
        :param set_name:集合名称（要存入的集合-表名）
        :return:
        """
        print("接收到数据：{}".format(data_dict))
        # 选中集合
        collection = self.db[set_name]
        print("------------------集合名称：{}--------------------".format(set_name))

        # # 为商铺分类标签创建唯一索引
        # if set_name == "商铺分类标签":
        #     collection.create_index("href", unique=True)

        if isinstance(data_dict, dict):
            try:
                # 向集合写入数据
                collection.insert(data_dict)
                # 关闭数据库连接
                self.client.close()
                print("写入:{}成功".format(data_dict))
            except:
                print("写入异常")

        elif isinstance(data_dict, list):
            try:
                # 向集合写入数据
                collection.insert_many(data_dict)
                # 关闭数据库连接
                self.client.close()
                print("写入:{}成功".format(data_dict))
            except:
                print("写入异常")

    def add_category_tags(self, category_tags):
        """
        插入商铺分类标签
        :param category_tags:
        :return:
        """
        # print("插入数据")
        if isinstance(category_tags, list):
            for category_tag in category_tags:
                if self.exist_category_tag(category_tag['href']):
                    print("{} 已存在，不再添加".format(category_tag['href']))
                else:
                    self.data_save("商铺分类标签", category_tag)
        elif isinstance(category_tags, dict):
            if self.exist_category_tag(category_tags['href']):
                print("{} 已存在，不再添加".format(category_tags['href']))
            else:
                self.data_save("商铺分类标签", category_tags)
        else:
            raise Exception("插入数据格式错误")

    def exist_category_tag(self, url):
        """
        判断商铺分类标签是否存在
        :param url: 该标签对应得url
        :return:
        """
        tag_count = self.db['商铺分类标签'].count_documents({'href': url})
        if tag_count == 0:
            return False
        else:
            return True

    def is_finish_category_tag(self, url):
        """
        判断商铺分类标签是否被访问
        :param url:
        :return:
        """
        query = {"href": url}
        doc = self.db['商铺分类标签'].find_one(query)
        if doc['is_finish']:
            return True
        else:
            return False

    def finish_category_tag(self, url):
        """
        访问商铺分类标签
        :param url:
        :return:
        """
        query = {"href": url}
        new_values = {"$set": {"is_finish": True}}
        self.db['商铺分类标签'].update(query, new_values)

    def get_category_tag_is_not_finish(self):
        """
        获取一个未访问的商铺分类标签页
        :return:
        """
        query = {"is_finish": True}
        col = self.db["商铺分类标签"].find_one(query)
        return col

    def get_category_tags_is_not_finish(self):
        """
        获取未访问的商铺分类标签页
        :return:
        """
        query = {"is_finish": True}
        cols = self.db["商铺分类标签"].find(query)
        return cols

    def add_shop(self, shop_dicts):
        if isinstance(shop_dicts, list):
            for shop_dict in shop_dicts:
                if self.exist_shop(shop_dict['shop_id']):
                    print("{} 已存在")
                else:
                    self.data_save("商铺列表", shop_dict)
        elif isinstance(shop_dicts, dict):
            if self.exist_shop(shop_dicts['shop_id']):
                print("{} 已存在")
            else:
                self.data_save("商铺列表", shop_dicts)
        else:
            print("类型错误")

    def exist_shop(self, shop_id):
        tag_count = self.db['商铺列表'].count_documents({'shop_id': shop_id})
        if tag_count == 0:
            return False
        else:
            return True


if __name__ == '__main__':
    mongo = MongoDB()
    # mongo.data_save("商铺分类标签", {
    #     'name': "测试",
    #     'href': "测试",
    # })
    col = mongo.get_category_tag_is_not_finish()
    print(col)
