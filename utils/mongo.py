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
        # 获取数据库连接
        db, client = self.get_mongo_client()
        # 选中集合
        collection = db[set_name]
        print("------------------集合名称：{}--------------------".format(set_name))

        # # 为商铺分类标签创建唯一索引
        # if set_name == "商铺分类标签":
        #     collection.create_index("href", unique=True)

        if isinstance(data_dict, dict):
            try:
                # 向集合写入数据
                collection.insert(data_dict)
                # 关闭数据库连接
                client.close()
                print("写入:{}成功".format(data_dict))
            except:
                print("写入异常")

        elif isinstance(data_dict, list):
            try:
                # 向集合写入数据
                collection.insert_many(data_dict)
                # 关闭数据库连接
                client.close()
                print("写入:{}成功".format(data_dict))
            except:
                print("写入异常")


if __name__ == '__main__':
    mongo = MongoDB()
    mongo.data_save("商铺分类标签", {
        'name': "测试",
        'href': "测试",
    })
