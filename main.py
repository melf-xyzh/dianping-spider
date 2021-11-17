# -*- coding: utf-8 -*-
"""
@Time       :2021/11/12 20:54
@Author     :MELF晓宇
@Email      :xyzh.melf@petalmail.com
@ProjectName:dianping-spider
@FileName   :main.py
@Blog       :https://blog.csdn.net/qq_29537269
@Guide      :https://guide.melf.space
@Information:
   程序入口
"""
# import urllib3
# from bs4 import BeautifulSoup
#
# ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
# cookie = "navCtgScroll=0; showNav=javascript:; fspop=test; cy=17; cye=xian; _lxsdk_cuid=17d14014cf3c8-05b3f0dcfb9ea3-561a1053-144000-17d14014cf3c8; _lxsdk=17d14014cf3c8-05b3f0dcfb9ea3-561a1053-144000-17d14014cf3c8; _hc.v=b49fb345-eaa7-63e9-fa9a-86f436a19bad.1636718169; s_ViewType=10; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_3607629787; ctu=f2c64a6b07df219587a01b189fb33ec3181c52f924e32ce53a35009c737dbaac; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1636760128; Hm_lpvt_dbeeb675516927da776beeb1d9802bd4=1636762038; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1636718170,1636718840,1636758897,1636848397; dper=b49b8839253d77b1ee7197a64a8254e037d3140fe01c2fe7af6adcc899f937a47e533dc3610dbcdb578f74d55c60c0c5a106ed4246963918665c822e10500a5b278763e87cc0c275779f16484fc429487752e4e2324000e4a9241497b6b437d6; uamo=18909190607; dplet=49571cf2cb6b5313f0e499395e4015b8; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1636853119; _lxsdk_s=17d1c0c73f6-147-0fd-298%7C%7C20"
#
#
# def test():
#     http = urllib3.PoolManager()
#     r = http.request(
#         method='GET',
#         url='http://www.dianping.com/xian/ch10',
#         headers={
#             'User-Agent': ua,
#             'Cookie': cookie
#         }
#     )
#     html = r.data.decode()
#
#     # 使用BeautifulSoup煲汤
#     soup = BeautifulSoup(html, "html.parser")
#     # print(soup.body.contents)
#     print(r.status)
#
#     soup.find_all(name=True)
#
#     a_l = soup.find_all()
#     for a in a_l:
#         print(a)
#         print(a['href'])
#         print(a.contents[0].getText())
#
#
# if __name__ == '__main__':
#     test()
from crawler.Crawler import Crawler

crawler1 = Crawler()

for i in range(100):
    col = crawler1.mongodb.get_category_tag_is_not_finish()
    url = col['href']
    print(url)
    crawler1.get_shop_id_list(url=url)
