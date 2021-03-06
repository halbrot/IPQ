#!/usr/bin/env python
# coding: utf-8

import sys
import os
import time

# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "calc"))
import edit_for_graph as efg
from ambtemp import AmbTemp

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
    character = str(request.args.get('character'))
    startsec = int(request.args.get('startsec'))
    endsec = int(request.args.get('endsec'))
    refresh = int(request.args.get('refresh'))

    if refresh==1:
        refresh=True
    else:
        refresh=False

    charalist = efg.get_characteristic_data(path, character, startsec, endsec, refresh)

    # 日時をstring のリストに変換
    datetime_string = [str(date) for date in charalist[0]]

    # マウスオーバーで表示するためのID
    id = list(range(len(charalist[0])))

    response={}
    response['datetime'] = datetime_string
    for i in range(len(charalist)-1):
        response['data' + str(i)] = charalist[i+1]
    response['id'] = id

    # response = {'datetime':datetime_string,
    #             'data1': df["特性値1"].values.tolist(),
    #             'data2': df["特性値2"].values.tolist(),
    #             'id' : id}

    response = jsonify(response)

    # CORS を回避 qiitaのストック記事参照
    response.headers["Access-Control-Allow-Origin"]="*"

    return response

@app.route('/singleplot', methods=['GET'])
def singleplot():

    path = str(request.args.get('path'))
    character = str(request.args.get('character'))
    id = int(request.args.get('id'))

    # path="Z:/01_研究テーマ/14_三重IH改善/07_冷却水温度測定/202106_GRT7101C0/"
    time, mv, charalist = efg.singlecurve(path, id, character=character)

    # response = {'time': time,
    #             'data1': chara1list,
    #             'data2': chara2list,
    #             'mv' : mv}

    response={}
    response['datetime'] = time
    for i in range(len(charalist)):
        response['data' + str(i)] = charalist[i]
    response['mv'] = mv

    response = jsonify(response)

    # CORS を回避 qiitaのストック記事参照
    response.headers["Access-Control-Allow-Origin"]="*"

    return response

@app.route('/ambtemp', methods=['GET'])
def ambtemp():

    path = str(request.args.get('path'))
    filename = str(request.args.get('filename'))

    df = AmbTemp(path + 'amb/' + filename).getdata()

    # 日時をstring のリストに変換
    datetime_string = []
    for date in df["日時"].values:
        datetime_string.append(str(date))

    response = {
        'time': datetime_string,
        'in': df['in'].values.tolist(),
        'out': df['out'].values.tolist()
    }

    response = jsonify(response)

    # CORS を回避 qiitaのストック記事参照
    response.headers["Access-Control-Allow-Origin"]="*"

    return response

@app.route('/ambcheck', methods=['GET'])
def ambcheck():

    path = str(request.args.get('path'))
    import os, glob

    files = []

    if os.path.exists(path + 'amb'):
        fullpathfiles = glob.glob(path + 'amb/*.csv')
        for fullpathfile in fullpathfiles:
            files.append(os.path.split(fullpathfile)[1])
    else:
        files = None

    response = {
        'file': files
    }

    response = jsonify(response)

    # CORS を回避 qiitaのストック記事参照
    response.headers["Access-Control-Allow-Origin"]="*"

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    app.run()
    # getdata()

