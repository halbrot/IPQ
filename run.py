#!/usr/bin/env python
# coding: utf-8

import sys
import os
import time

# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "calc"))
import divide2single_data as d2sd

from flask import Flask, render_template, Response,request,redirect,url_for, jsonify


# flask incetance
app = Flask(__name__)

# index page, input code
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getdata', methods=['GET'])
def getdata():

    # b = float(request.args.get('b'))

    path="Z:/01_研究テーマ/14_三重IH改善/07_冷却水温度測定/202106_GRT7101C0/"
    df = d2sd.routine(path, "temperature")

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

    id = int(request.args.get('id'))

    path="Z:/01_研究テーマ/14_三重IH改善/07_冷却水温度測定/202106_GRT7101C0/"
    chara1list, chara2list, mv , time = d2sd.singlecurve(id, character="temperature")


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

