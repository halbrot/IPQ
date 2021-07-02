# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 14:30:30 2020

@author: ntn080465
"""
import glob
import os
import numpy as np
import pandas as pd


class preprocess:

    def __init__(self, path):
        if path[-1] != '/':
            path += '/'
        self.workdir = path
        self.concatfile = path + 'concat.pkl'

    def concat_csv(self):
        """
        すでにconcat.csv が存在する場合は削除して再作成
        """
        if os.path.exists(self.concatfile):
            os.remove(self.concatfile)

        files = glob.glob(self.workdir + "*.csv")
        
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
        self.df = concat_array


    def change_column_name(self):
        """
        2020/12/07時点 三重IHのロギングの設定

        """
        if self.df.shape[1]!=21:
            return
        
        self.df.columns = ["日時", "ms", "ワーク外側温度", "ワーク内側温度", "IHヒータ電圧値", "IHヒータ周波数",
                    "IHヒータ出力電力値", "IHヒータ直流電圧値", "Channel1", "電圧出力", "材温熱電対1",
                    "材温熱電対2", "材温熱電対3", "Channel8", "材温熱電対4", "材温熱電対5", "炭化物面積率1",
                    "炭化物面積率2", "IHﾘﾌﾀｰｻｰﾎﾞ負荷率", "回転", "回転"]


    def drop_unused_columns(self):
        """
        量産時に使わない項目（例えば熱電対）を削除
        """
        
        if self.df.shape[1]!=21:
            return
        
        drop_column_names = ["材温熱電対1", "材温熱電対2", "材温熱電対3", "Channel8", "材温熱電対4","材温熱電対5" ]
        self.df.drop(columns=drop_column_names, inplace=True)

    def save_df(self):
        self.df.to_pickle(self.concatfile)

    def load_df(self):
        self.df = pd.read_pickle(self.concatfile)


    def divided2single(self):
        """
        concat.csv は複数回の加熱が適当なインターバルをはさんで繰り返されるデータなので，
        個々の加熱データにわける必要がある．
        加熱開始インデックスと加熱終了インデックスの2要素からなる配列の2次元配列を返す．
        一度計算したらstartend.npy に保存して，次からは再利用する．
        再計算したい場合は引数にTrueを指定する．
        """

        if os.path.exists(self.workdir + "startend.npy"):
            os.remove(self.workdir + "startend.npy")

        start_end_index = []
    
        frequency = self.df["IHヒータ周波数"]
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
        np.save(self.workdir + "startend", arr)

    def getdata(self, remake=False):
        """
        df と start_end_indexを返す
        refreshがFalseでconcat.csvがすでにある場合はそれを読み込んで返し，
        ない場合は生成する．
        refreshがTrueの場合はconcat.csvを削除して再生成する．
        """

        # concat.pklが存在しない場合，remakeフラグを立てる
        if not remake:
            if not os.path.exists(self.concatfile):
                remake = True

        if remake:
            self.concat_csv()
            self.change_column_name()
            self.drop_unused_columns()
            self.save_df()
            self.divided2single()
        
        self.load_df()
        start_end_index = np.load(self.workdir + "startend.npy").tolist()

        return self.df, start_end_index


if __name__ == "__main__":
    path = 'Z:/05_テーマ外仕事/202011_三重IH改善/06_周辺温度測定/202106_GRW5102B0/'
    df, start_end_index = preprocess(path).getdata
    print(start_end_index)
