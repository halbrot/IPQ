# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import datetime
from preprocess import Preprocess
from numba import jit


chara2column = {
      "frequency": "IHヒータ周波数",
      "power": "IHヒータ出力電力値",
      'voltageAC': "IHヒータ電圧値",
      'voltageDC': "IHヒータ直流電圧値",
      'MV': '電圧出力'
}


def singlecurve(path, graph_index, character="temperature"):
    
    df, start_end_index = Preprocess(path).getdata()

    if character == "temperature":
        chara1 = "ワーク外側温度"
        chara2 = "ワーク内側温度"
    elif character == "carbide":
        chara1 = "炭化物面積率1"
        chara2 = "炭化物面積率2"
    else:
        chara1 = chara2 = chara2column(character)
 

    i = graph_index

    chara1list = df[chara1].values[start_end_index[i][0]:start_end_index[i][1] + 1].tolist()
    chara2list = df[chara2].values[start_end_index[i][0]:start_end_index[i][1] + 1].tolist()
    mv = df["電圧出力"].values[start_end_index[i][0]:start_end_index[i][1] + 1].tolist()

    # 加熱開始時間との差を取り，経過時間を計算
    # 秒に変化し，最後にリスト化
    time = df['日時'][start_end_index[i][0]:start_end_index[i][1] + 1] - df['日時'][start_end_index[i][0]]
    time = time.dt.total_seconds()
    time = time.tolist()

    return chara1list, chara2list, mv, time


def get_characteristic_data(path, character, refresh=False):
    """
    character: carbide → 炭化物面積率の最終値
               temperature → ワーク温度の"最大値"
               frequency → 開始，終了時周波数
               power → 開始，終了時電力
               tempdiff → ワーク外側最高温度 - ワーク内側最高温度
    """

    df, start_end_index = Preprocess(path).getdata(refresh)

    datanum = len(start_end_index)
    datetime = []
    chara1list = []
    chara2list = []

    from datetime import datetime as dt
    start = dt.now()
    # it = iter(start_end_index)
    

    # 各ヒートでの特性値をリストに抽出
    if character == "carbide":
        datetime = [df["日時"][x[1]] for x in iter(start_end_index)]
        chara1list = [df["炭化物面積率1"][x[1]] for x in iter(start_end_index)]
        chara2list = [df["炭化物面積率2"][x[1]] for x in iter(start_end_index)]

    elif character == "temperature" or character == "tempdiff":
        arr = df.loc[:,["日時", "ワーク外側温度", "ワーク内側温度"]].values
        datetime = [arr[x[1],0] for x in iter(start_end_index)]
        chara1list = [arr[x[0]:x[1]+1, 1].max() for x in iter(start_end_index)]
        chara2list = [arr[x[0]:x[1]+1, 2].max() for x in iter(start_end_index)]

    else:
        column = chara2column(character)

        arr = df.loc[:,["日時", column]].values
        datetime = [arr[x[1],0] for x in iter(start_end_index)]
        chara1list = [arr[x[0]+30:x[0]+250, 1].sum()/220 for x in iter(start_end_index)]
        chara2list = [arr[x[0]+30:x[0]+250, 1].sum()/220 for x in iter(start_end_index)]

    print(dt.now()-start)

    # 異常値除去しやすいようにDataFrameにまとめる
    df2 = pd.DataFrame({"日時": datetime,
                        "特性値1": chara1list,
                        "特性値2": chara2list})


    # tempdiffは1系列のデータしか必要ないが，この後のif文を少なくするために特性値1, 2両方に 同じデータを入れている．
    # 両方ともプロットされるが，完全に重なるので見た目上問題ない．
    if character == "tempdiff":
        df2["特性値1"] = df2["特性値1"] - df2["特性値2"]
        df2["特性値2"] = df2["特性値1"]

    return df2



if __name__ == "__main__":
    # path = "Z:/01_研究テーマ/14_三重IH改善/08_生産チャート/202106_GRW5102B0"
    # singlecurve(path, 2)
    list = [[0,1],[2,3]]
    arr = np.array(list)
    for i in iter(list):
        print(i[0])



