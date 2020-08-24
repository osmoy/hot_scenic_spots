import requests
import re
import random
import csv
import sys
import os
from bs4 import BeautifulSoup
from lxml import etree
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from spiders.settings import USER_AGENT
from db.mongo_pool import mongo


class Mafengwo(object):
    def __init__(self, city=''):
        self.city = city if len(city) > 0 else '杭州'
        self.headers = {'User-Agent': random.choice(USER_AGENT)}
        self.urls = [
            'http://www.mafengwo.cn/search/q.php?q={}&t=pois&p={}'.format(
                self.city, i) for i in range(1, 11)
        ]

    def get_html(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def parse_html(self, html):
        selector = etree.HTML(html)
        all_li = selector.xpath(
            '//*[@id="_j_search_result_left"]/div/div/ul/li')

        for li in all_li:
            item = {}
            title = li.xpath('./div/div[2]/h3/a/text()')[0]
            comment = li.xpath('./div/div[2]/ul/li[2]/a/text()')[0]
            travels = li.xpath('./div/div[2]/ul/li[3]/a/text()')[0]

            if (title.find('（') != -1):
                # 景点 - 杭州西湖风景名胜区（West Lake）
                res = re.findall('(.+) - (.+)（(.+)）', title)
                item['category'] = res[0][0]
                item['name'] = res[0][1]
                item['english_name'] = res[0][2]
            else:
                # 美食 - 咬不得高祖生煎(高银街店)
                res = re.findall('(.+) - (.+)', title)[0]
                item['category'] = res[0]
                item['name'] = res[1]

            item['location'] = li.xpath('./div/div[2]/ul/li[1]/a/text()')[0]            
            item['comments'] = int(re.findall('\((\d+)\)', comment)[0])            
            item['travels'] = int(re.findall('\((\d+)\)', travels)[0])
            item['get_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['city'] = self.city
            yield item

    def save_to_csv(self, data, index):
        with open('hot_scenic_spots.csv','a',encoding='utf-8-sig',newline='') as f:
            fieldnames = [
                'name', 'english_name', 'category', 'location', 'comments', 'travels', 'get_time', 'city'
            ]
            f_csv = csv.DictWriter(f, fieldnames=fieldnames, dialect='excel')
            if (index == 0):
                f_csv.writeheader()
            f_csv.writerows(data)

    def save_to_mongo(self, data):
        for item in data:
            # 用名字作为唯一主键
            item['_id'] = item['name']
            mongo.insert_one(item)

    def run(self):
        # i = 0
        # for url in self.urls:
        #     html = self.get_html(url)
        #     data = self.parse_html(html)
        #     self.save_to_csv(data, i)
        #     i = i + 1

        for url in self.urls:
            html = self.get_html(url)
            data = self.parse_html(html)
            self.save_to_mongo(data)
        print('保存成功')


if __name__ == "__main__":
    obj = Mafengwo()
    obj.run()