#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   visualization.py
@Time    :   2020/08/20 10:41:56
@Author  :   MOY 
@Version :   3.7.3
@Contact :   283120991@qq.com
@License :   (C)Copyright 2018-2020, Liugroup-NLPR-CASIA
@Desc    :   使用flask将保存的数据进行可视化展示
'''
# here put the import lib
import json
import pymongo

from flask import Flask, render_template, Response
from flask_bootstrap import Bootstrap

from spiders.mafengwo import Mafengwo
from db.mongo_pool import mongo


class scenic_spots_api(object):
    def __init__(self):
        self.app = Flask(__name__)
        self.bootstrap = Bootstrap(self.app)

        @self.app.route('/')
        def view():
            data = {
                "a": "aaa",
                "list": [1, 2, 3, 4, 5],
                "dict": {
                    "x": 44,
                    "y": 55
                }
            }
            name = "44"
            return render_template('view.html', name=name, **data)

        @self.app.route('/user/<name>')
        def user(name=None):
            return render_template('user.html', name=name)

        @self.app.route('/echarts/<city>')
        def chart(city):
            if city is None:
                return "请输入查询城市"

            count = mongo.find_by_condition(condition={'city': city}, limit=15)
            if len(count) <= 0:

                obj = Mafengwo(city)
                obj.run()

            return Response(json.dumps(info_list))

    def run(self):
        self.app.run()

    @classmethod
    def start(cls):
        obj = cls()
        obj.run()


if __name__ == "__main__":
    scenic_spots_api.start()