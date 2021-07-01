# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 14:30:30 2020

@author: ntn080465
"""
import glob
import os
import numpy as np
import pandas as pd

workdir = "Z:/05_テーマ外仕事/202011_三重IH改善/06_周辺温度測定/202106_GRW5102B0/"
concatfile = workdir + "concat.csv"

def concat_csv():
    """
    すでにconcat.csv が存在する場合は削除して再作成
    """
    if os.path.exists(concatfile):
        os.remove(concatfile)

    files = glob.glob(workdir + "*.csv")
    
    i = 0
    for file in files:
        new_array = pd.read_csv(file, sep=',', skiprows=47)
        if i == 0:
            concat_array = new_array.copy()
        else:
            concat_array = pd.concat([concat_array, new_array])
        i = i + 1
        print(file)

    concat_array.reset_index(drop=True, inplace=True)
    concat_array.to_csv(concatfile)


def change_column_name():
    """
    2020/12/07時点 三重IHのロギングの設定

    """
    df = pd.read_csv(concatfile, index_col=0)
    
    if df.shape[1]!=21:
        return
    
    df.columns = ["日時", "ms", "ワーク外側温度", "ワーク内側温度", "IHヒータ電圧値", "IHヒータ周波数",
                  "IHヒータ出力電力値", "IHヒータ直流電圧値", "Channel1", "電圧出力", "材温熱電対1",
                  "材温熱電対2", "材温熱電対3", "Channel8", "材温熱電対4", "材温熱電対5", "炭化物面積率1",
                  "炭化物面積率2", "IHﾘﾌﾀｰｻｰﾎﾞ負荷率", "回転", "回転"]
    df.to_csv(concatfile)


def drop_unused_columns():
    """
    量産時に使わない項目（例えば熱電対）を削除

    """
    df = pd.read_csv(concatfile, index_col=0)
    
    if df.shape[1]!=21:
        return
    
    drop_column_names = ["材温熱電対1", "材温熱電対2", "材温熱電対3", "Channel8", "材温熱電対4","材温熱電対5" ]
    for column in drop_column_names:
        df = df.drop(column, axis=1)
        
    df.to_csv(concatfile)

def divided2single():
    """
    concat.csv は複数回の加熱が適当なインターバルをはさんで繰り返されるデータなので，
    個々の加熱データにわける必要がある．
    加熱開始インデックスと加熱終了インデックスの2要素からなる配列の2次元配列を返す．
    一度計算したらstartend.npy に保存して，次からは再利用する．
    再計算したい場合は引数にTrueを指定する．
    """

    if os.path.exists(workdir + "startend.npy"):
        os.remove(workdir + "startend.npy")

    start_end_index = []
 
    df = pd.read_csv(concatfile, index_col=0)
    frequency = df["IHヒータ周波数"]
    # 加熱していないときの周波数は1となっている．
    # 念のために 5を超える場合は加熱中，5未満では非加熱中とした．
    is_heat = False
    for i in range(frequency.size):
        if not is_heat:
            if frequency[i] > 5:
                start_index = i
                is_heat = True
        if is_heat:
            if frequency[i] <= 5:
                end_index = i
                is_heat = False
                start_end_index.append([start_index, end_index - 1])
    arr = np.array(start_end_index)
    np.save(workdir + "startend", arr)

def set_workdir(path):
    global workdir, concatfile
    workdir = path
    concatfile = workdir + "concat.csv"

def initprocess(path):
    """
    Excelファイルからconcat.csvを作成し，
    start_end_index を作成．
    すでにconcat.csv, startend.npyがある場合は再生成
    """
    set_workdir(path)
    concat_csv()
    change_column_name()
    drop_unused_columns()
    divided2single()


if __name__ == "__main__":
    concat_csv()
    change_column_name()
    drop_unused_columns()
