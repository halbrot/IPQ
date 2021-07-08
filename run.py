#!/usr/bin/env python
# coding: utf-8

import sys
import os
import time

# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "calc"))
import edit_for_graph as efg

from flask import Flask, render_template, Response,request,redirect,url_for, jsonify


# flask incetance
app = Flask(__name__)

# index page, input code
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getdata', methods=['GET'])
def getdata():


    path = str(request.args.get('path'))
    refresh = int(request.args.get('refresh'))

    if refresh==1:
        refresh=True
    else:
        refresh=False

    df = efg.get_characteristic_data(path, "temperature", refresh)

    # 日時をstring のリストに変換
    datetime_string = []
    for date in df["日時"].values:
        datetime_string.append(str(date))

    # マウスオーバーで表示するためのID
    id = list(range(df.shape[0]))
    
    response = {'datetime':datetime_string,
                'data1': df["特性値1"].values.tolist(),
                'data2': df["特性値2"].values.tolist(),
                'id' : id}

    response = jsonify(response)

    # CORS を回避 qiitaのストック記事参照
    response.headers["Access-Control-Allow-Origin"]="*"

    return response

@app.route('/singleplot', methods=['GET'])
def singleplot():

    path = str(request.args.get('path'))
    id = int(request.args.get('id'))

    # path="Z:/01_研究テーマ/14_三重IH改善/07_冷却水温度測定/202106_GRT7101C0/"
    chara1list, chara2list, mv , time = efg.singlecurve(path, id, character="temperature")
    print(time[0:5])

    response = {'time': time,
                'data1': chara1list,
                'data2': chara2list,
                'mv' : mv}

    response = jsonify(response)

    # CORS を回避 qiitaのストック記事参照
    response.headers["Access-Control-Allow-Origin"]="*"

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    app.run()
    # getdata()

