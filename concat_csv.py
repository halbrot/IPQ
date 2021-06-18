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
    if os.path.exists(concatfile):
        return
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
    
    drop_column_names = ["ms", "材温熱電対1", "材温熱電対2", "材温熱電対3", "Channel8", "材温熱電対4","材温熱電対5" ]
    for column in drop_column_names:
        df = df.drop(column, axis=1)
        
    df.to_csv(concatfile)

def set_workdir(path):
    global workdir, concatfile
    workdir = path
    concatfile = workdir + "concat.csv"

def usualprocess(path):
    """
    concatfile があるとconcat_csvは実行しない
    使わない項目を落として 列数が21 になっていたら，change_column_name と drop_unused_columns を実行しない．
    """
    set_workdir(path)
    concat_csv()
    change_column_name()
    drop_unused_columns()

if __name__ == "__main__":
    concat_csv()
    change_column_name()
    drop_unused_columns()
