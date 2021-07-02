# -*- coding: utf-8 -*-
"""
ver.1.05
・divide2single_data.py から concat.csvを呼び出すように変更
・yrange もkwardsに含めた．

ver.1.04
2021/6/4
・桑名の気温をプロットする機能を拡張し，雰囲気温度等をプロットする標準的な仕様にした．
　辞書型変数 ambient に データフレーム と プロットする列名，yrange を格納して
  histplot_datetime にわたす．
・ histplot_datetime 内でプロット前にプロットする範囲のデータだけを抽出するように変更
　これにより適切な上下限でプロットされるようになった．
要変更
・ days_history で 2日以上をプロットする場合に上下限を自動的に決定し統一する機能


ver.1.03
2021/05/13
下記関数に集約
・ singlecurve(graph_index, character="temperature")
・ curves (メンテナンスしていない)
・ days_history(year, month, firstday, days = 1, character = "carbide", annotation = False, weather = False)
・ all_hist(character = "carbide")

divided2singleの結果を保存して再利用するように変更

ver.1.02
2021/05/12
一日毎の炭化物面積率推移表示を追加

2021/04/12
sigletempを追加
目標温度の横軸を自動決定
MVのシフトを削除

@author: ntn080465
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import preprocess
import os



workdir = "Z:/01_研究テーマ/14_三重IH改善/07_冷却水温度測定/202106_GRT7101C0/"
concatfile = workdir + "concat.csv"

def read_startend():
    global start_end_index
    start_end_index = np.load(workdir + "startend.npy").tolist()


def create_ax(tate=1, yoko=1, tatemm=127, yokomm=170):
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['xtick.major.width'] = 1.0
    plt.rcParams['ytick.major.width'] = 1.0
    plt.rcParams['font.size'] = 8
    plt.rcParams['axes.linewidth'] = 1.0
    # 30*5
    mm2inch = 1 / 25.4
    fig, ax = plt.subplots(tate, yoko, figsize=(yokomm * mm2inch * yoko, tatemm * mm2inch * tate), dpi=100)
    return fig, ax


def singlecurve(path, graph_index, character="temperature"):
    
    df, start_end_index = preprocess.getdata(path)

    if character == "temperature":
        chara1 = "ワーク外側温度"
        chara2 = "ワーク内側温度"
    elif character == "carbide":
        chara1 = "炭化物面積率1"
        chara2 = "炭化物面積率2"

    # numpyarrayに変換
    # series のままだとMatplotlib でplot した時に X軸の値にインデックス値を使われてしまう．
    i = graph_index
    #サンプリングレートを検出 (1 s 以下にのみ対応)
    samplingrate = (df["ms"][start_end_index[i][0]+1]-df["ms"][start_end_index[i][0]])/1000
    if samplingrate == 0:
        samplingrate = 1

    chara1list = df[chara1].values[start_end_index[i][0]:start_end_index[i][1] + 1].tolist()
    chara2list = df[chara2].values[start_end_index[i][0]:start_end_index[i][1] + 1].tolist()
    mv = df["電圧出力"].values[start_end_index[i][0]:start_end_index[i][1] + 1].tolist()
    time = np.arange(0, len(chara1list)*samplingrate, samplingrate).tolist()

    return chara1list, chara2list, mv, time


def curves(path, graph_index):

    df, start_end_index = preprocess.getdata(path)

    # numpyarrayに変換
    # series のままだとMatplotlib でplot した時に X軸の値にインデックス値を使われてしまう．
    outer_temperature = df["ワーク外側温度"].values
    inner_temperature = df["ワーク内側温度"].values
    MV = df["電圧出力"].values

    # グラフを書くための準備
    fig, ax = create_ax(1, 3)

    duration = 0
    for i in graph_index:
        label = str(i) + "   " + df["日時"][start_end_index[i][0]]
        ax[0].plot(outer_temperature[start_end_index[i][0]:start_end_index[i][1] + 1], label=label)
        ax[1].plot(inner_temperature[start_end_index[i][0]:start_end_index[i][1] + 1], label=label)
        ax[2].plot(MV[start_end_index[i][0]:start_end_index[i][1] + 1], label=label)
        duration_c = start_end_index[i][1] - start_end_index[i][0]
        duration = max(duration, duration_c)
        # print(str(i)+" " +df["日時"][start_end_index[i][0]])

    # グラフの体裁
    for i in range(3):
        if i != 2:
            ax[i].plot((1, duration), (880, 880), color='black', linewidth=1.0)
            ax[i].legend(loc='lower right')
        ax[i].tick_params(axis='both', direction='in')
    ax[2].legend(loc='upper right')
    ax[0].set_ylim([750, 920])
    ax[1].set_ylim([750, 920])
    ax[0].set_title("Outer Temperature")
    ax[1].set_title("Inner Temperature")
    ax[2].set_title("MV")

    plt.show()


def get_characteristic_data(path, character, refresh=False):
    """
    character: carbide → 炭化物面積率の最終値
               temperature → ワーク温度の"最大値"
               frequency → 開始，終了時周波数
               power → 開始，終了時電力
               tempdiff → ワーク外側最高温度 - ワーク内側最高温度
    """

    df, start_end_index = preprocess.getdata(path, refresh)

    # 日時をdatetime型に変換
    df["日時"] = pd.to_datetime(df["日時"])
    datetime = []
    chara1list = []
    chara2list = []

    # 各ヒートでの特性値をリストに抽出
    if character == "carbide":
        for i in range(len(start_end_index)):
            datetime.append(df["日時"][start_end_index[i][1]])
            chara1list.append(df["炭化物面積率1"][start_end_index[i][1]])
            chara2list.append(df["炭化物面積率2"][start_end_index[i][1]])
    elif character == "temperature" or character == "tempdiff":
        for i in range(len(start_end_index)):
            datetime.append(df["日時"][start_end_index[i][1]])
            chara1list.append(df["ワーク外側温度"].iloc[start_end_index[i][0]:start_end_index[i][1] + 1].max())
            chara2list.append(df["ワーク内側温度"].iloc[start_end_index[i][0]:start_end_index[i][1] + 1].max())
    elif character == "frequency":
        for i in range(len(start_end_index)):
            datetime.append(df["日時"][start_end_index[i][1]])
            chara1list.append(df["IHヒータ周波数"][start_end_index[i][0] + 3])
            chara2list.append(df["IHヒータ周波数"][start_end_index[i][1] - 3])
    elif character == "power":
        for i in range(len(start_end_index)):
            datetime.append(df["日時"][start_end_index[i][1]])
            chara1list.append(df["IHヒータ出力電力値"][start_end_index[i][0] + 3])
            chara2list.append(df["IHヒータ出力電力値"][start_end_index[i][1] - 3])

  
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


def histplot_datetime(startdatetime, enddatetime, character, ax, **kwargs):
    """
    下記データを抽出してDataFrameで返す
    character: carbide → 炭化物面積率の最終値
               temperature → ワーク温度の最"大"値
               tempdiff → ワーク外側最高温度 - ワーク内側最高温度
    """

    # 辞書のkeyに含まれていない場合，None を返す
    def check_key(key):
        if key in kwargs:
            return kwargs[key]
        else:
            return None

    # 辞書の各値を取り出す，key が含まれていない場合は，Noneとなる．
    yrange = check_key("yrange")
    annotation_index = check_key("annotation_index")
    df_amb = check_key("df_amb")
    yrange_amb = check_key("yrange_amb")
    col_names = check_key("col_names")

    read_startend()
    df = get_characteristic_data(character)

    # DataFrameからプロットに使う範囲のデータだけを抽出する
    # こうすると，適切な上下限範囲でプロットされる
    df2 = df[(df["日時"] >= startdatetime) & (df["日時"] <= enddatetime)]

    label = ("outer", "inner")

    # 散布図のプロット
    ax.scatter(df2["日時"], df2["特性値1"], s=6, label=label[0])
    ax.scatter(df2["日時"], df2["特性値2"], s=6, label=label[1])

    # ax.legend()

    # xの表示範囲を設定
    ax.set_xlim(startdatetime, enddatetime)

    # yrangeが指定されている場合はYの表示範囲を設定
    # 多段プロットをする場合は基本的には必須
    if yrange is not None:
        ax.set_ylim(*yrange)

    ###########################################################################################
    # 注釈
    if annotation_index is not None:
        # 矢印のプロパティを設定
        annotation_index = kwargs["annotation_index"]
        arrow_dict = dict(arrowstyle="->", color="black")

        # annotation_indexに all が指定されている場合はすべて
        if annotation_index == "all":
            annotation_index = range(len(start_end_index))

        # ポイントに注釈を入れる
        for i in annotation_index:
            ax.annotate(str(i), xy=(df["日時"][i], df["特性値1"][i]), xytext=(df["日時"][i], df["特性値1"][i] + 0.1),
                        arrowprops=arrow_dict, size=6)
            ax.annotate(str(i), xy=(df["日時"][i], df["特性値2"][i]), xytext=(df["日時"][i], df["特性値2"][i] + 0.1),
                        arrowprops=arrow_dict, size=6)

    ###############################################################################################
    # 第2軸での雰囲気温度等のプロット
    # None もしくは 辞書に含まれていなかったら 実行しない
    # 辞書に含まれていない場合は df_amb が None になる
    if df_amb is not None:

        #  # DataFrameからプロットに使う範囲のデータだけを抽出する
        df_amb = df_amb[(df_amb["日時"] >= startdatetime) & (df_amb["日時"] <= enddatetime)]

        # 第2軸の生成
        ax2 = ax.twinx()

        # if not isinstance(col_names, tuple) or not isinstance(col_names, list):
        #     col_names = [col_names]

        color = ["lightblue", "pink"]
        i=0
        for col_name in col_names:
            ax2.plot(df_amb["日時"], df_amb[col_name], color=color[i], linewidth=1., alpha=0.8)
            i += 1

        # yrange_ambが指定されている場合はYの表示範囲を設定
        if yrange_amb is not None:
            ax2.set_ylim(*yrange_amb)

        ax2.invert_yaxis()


def days_history(year, month, firstday, days=1, character="carbide", **kwargs):
    """
    histplot_datetimeのラッパー
    一日を単位として指定日からの日数分をプロット
    雰囲気温度等を第2軸でプロットする場合には以下の辞書オブジェクトを引数に渡す
    "df_amb":対象のデータフレーム, "col_name":プロットする列名
    データラベルが必要な場合は下記の辞書オブジェクトを追加
    "annotation_index": インデックスのリスト，すべて表示する場合は"all"を渡す．ただし，描画にすごく時間かかる．
    """

    fig, ax = create_ax(days, 1, tatemm=50, yokomm=300)

    startdatetime = datetime.datetime(year, month, firstday, 0, 0, 0)
    enddatetime = datetime.datetime(year, month, firstday, 23, 59, 59)

    for i in range(days):
        if days == 1:
            ax = [ax]
        histplot_datetime(startdatetime + datetime.timedelta(days=i), enddatetime + datetime.timedelta(days=i),
                          character, ax[i], **kwargs)

    plt.tight_layout()
    plt.show()


def all_hist(character="carbide"):
    read_startend()
    df = get_characteristic_data(character)  # プロット期間を指定するために必要
    fig, ax = create_ax(1, 1, tatemm=50, yokomm=300)
    annotate_index = range(0, len(start_end_index) + 1, 100)
    histplot_datetime(df["日時"].iloc[0], df["日時"].iloc[-1], character, ax, **{"annotation_index": annotate_index})

    plt.tight_layout()
    plt.show()


def kuwana_weather():
    df = pd.read_csv("kuwana_weather.csv", skiprows=5, usecols=(0, 1))
    df.columns = ["日時", "気温"]
    df["日時"] = pd.to_datetime(df["日時"])
    # df = df.set_index("日時")
    return df


def amb_temps():
    """
    周辺温度データ
    """

    # 必要な列だけを読み込み，列名をつける． 0, 1 列が日付と時間
    # Chino用
    # df = pd.read_csv(workdir + '/amb/コイル冷却水.csv', usecols=(0, 1, 2, 3), skiprows=1)
    # df.columns = ["date", "time", "in", "out"]
    # df["diff"] = df["out"] - df["in"]

    # graphtec用
    df = pd.read_csv(workdir + '/amb/電源冷却水.csv', usecols=(1, 2, 4, 5), skiprows=35)
    df.columns = ["date", "time", "out", "in"]
    df["in"] = df["in"].str[3:]
    df["out"] = df["out"].str[3:]
    df = df.astype({"in":float, "out":float})

    # 日付と時間が別れているので結合しdatetimeに変換
    df["日時"] = df["date"].str.cat(df["time"], sep=" ")
    df["日時"] = pd.to_datetime(df["日時"])

    # 日付と時間だけの列を削除
    df = df.drop(["date", "time"], axis=1)

    # 日時の列を行名に使用
    # df = df.set_index("日時")
    return df


if __name__ == "__main__":
    # singlecurve(12, "temperature", save=True)
    path = "Z:/01_研究テーマ/14_三重IH改善/07_冷却水温度測定/202106_GRT7101C0/"
    df, start_end_index = preprocess.getdata(path)
    print(df["ms"].iloc[1]-df["ms"].iloc[0])
    # routine(path)

