# -*- coding: utf-8 -*-

from typing import List
import numpy as np
import pandas as pd
import datetime
from preprocess import Preprocess


chara2column = {
    "temperature": ["ワーク外側温度", "ワーク内側温度"],
    "carbide": ["炭化物面積率1", "炭化物面積率2"],
    "frequency": "IHヒータ周波数",
    "power": "IHヒータ出力電力値",
    'voltageAC': "IHヒータ電圧値",
    'voltageDC': "IHヒータ直流電圧値",
    'MV': '電圧出力'
}


def singlecurve(path, graph_index, character="temperature"):
    
    df, start_end_index = Preprocess(path).getdata()

    # 加熱時間(heatduration)はsinglecurveを作成できないので，温度で代用
    if character == 'heatduration':
        character = 'temperature'
        
    column = chara2column[character]
    if type(column) is str:
        column = [column]


    # if character == "temperature":
    #     chara1 = "ワーク外側温度"
    #     chara2 = "ワーク内側温度"
    # elif character == "carbide":
    #     chara1 = "炭化物面積率1"
    #     chara2 = "炭化物面積率2"
    # else:
    #     chara1 = chara2 = chara2column[character]
 
    i = graph_index

    charalist = []

    for col in column:
        charalist.append(df[col].values[start_end_index[i][0]:start_end_index[i][1] + 1].tolist())
    mv = df["電圧出力"].values[start_end_index[i][0]:start_end_index[i][1] + 1].tolist()

    # 加熱開始時間との差を取り，経過時間を計算
    # 秒に変化し，最後にリスト化
    time = df['日時'][start_end_index[i][0]:start_end_index[i][1] + 1] - df['日時'][start_end_index[i][0]]
    time = time.dt.total_seconds()
    time = time.tolist()

    return time, mv, charalist


def get_characteristic_data(path, character, startsec=0, endsec=30, refresh=False):
    """
    character: carbide → 炭化物面積率の最終値
               temperature → ワーク温度の"最大値"
               frequency → 開始，終了時周波数
               power → 開始，終了時電力
               tempdiff → ワーク外側最高温度 - ワーク内側最高温度
               heatduration → 加熱時間
    """

    df, start_end_index = Preprocess(path).getdata(refresh)

    charalist = []

    # 各ヒートでの特性値をリストに抽出
    # 配列2つをcharalistという配列に入れる
    if character == "carbide":
        arr = df.loc[:,["日時", "炭化物面積率1", "炭化物面積率2"]].values
        datetime = [arr[x[1],0] for x in iter(start_end_index)]
        charalist.append([arr[x[1],1] for x in iter(start_end_index)])
        charalist.append([arr[x[1],2] for x in iter(start_end_index)])

    elif character == "temperature" or character == "tempdiff":
        arr = df.loc[:,["日時", "ワーク外側温度", "ワーク内側温度"]].values
        datetime = [arr[x[1],0] for x in iter(start_end_index)]
        charalist.append([arr[x[0]:x[1]+1, 1].max() for x in iter(start_end_index)])
        charalist.append([arr[x[0]:x[1]+1, 2].max() for x in iter(start_end_index)])

    elif character == "heatduration":
        arr = df.loc[:,"日時"].values
        datetime = [arr[x[1]] for x in iter(start_end_index)]
        heatduration = [(arr[x[1]]-arr[x[0]])/np.timedelta64(1, 's') for x in iter(start_end_index)]
        # time = df['日時'][start_end_index[i][0]:start_end_index[i][1] + 1] - df['日時'][start_end_index[i][0]]
        # heatduration = heatduration.dt.total_seconds()

        charalist.append(heatduration)

    else:
        column = chara2column[character]

        arr = df.loc[:,["日時", column]].values
        datetime = [arr[x[1],0] for x in iter(start_end_index)]

        #temperature や carbideとの整合性を保つために
        # 配列1つが配列charlistの中に入っている状態にしたい
        charalist.append([])
        for i in iter(start_end_index):
            for j in range(*i):
                time = (arr[j, 0] - arr[i[0], 0]).total_seconds()
                if time == startsec:
                    startidx = j
                if time == endsec:
                    endidx = j
                    charalist[0].append(arr[startidx:endidx+1, 1].sum()/(endidx - startidx + 1))
                    break
        
    return [datetime, *charalist]



if __name__ == "__main__":
    # path = "Z:/01_研究テーマ/14_三重IH改善/08_生産チャート/202106_GRW5102B0"
    # singlecurve(path, 2)
    list = "aaa"
    print(type(list))



