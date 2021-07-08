# -*- coding: utf-8 -*-

import glob
import os
import numpy as np
import pandas as pd

class AmbTemp:

    def __init__(self, filepath, maker):
        """
        makerはロガーのメーカー
        """
        self.maker = maker
        self.filepath = filepath

    def load_file(self):
        """
        周辺温度データ
        """

        if self.maker == 'chino':
             # 必要な列だけを読み込み，列名をつける． 0, 1 列が日付と時間
            self.df = pd.read_csv(self.filepath, usecols=(0, 1, 2, 3), skiprows=1)
            self.df.columns = ["date", "time", "in", "out"]

        elif self.maker == 'graphtec':
            # graphtec用
            # 数値データの先頭に "+  "とついており，そのままではfloatに変換できない
            self.df = pd.read_csv(self.filepath, usecols=(1, 2, 4, 5), skiprows=35)
            self.df.columns = ["date", "time", "out", "in"]
            self.df["in"] = self.df["in"].str[3:]
            self.df["out"] = self.df["out"].str[3:]
            self.df = self.df.astype({"in":float, "out":float})

        # 日付と時間が別れているので結合しdatetimeに変換
        self.df["日時"] = self.df["date"].str.cat(self.df["time"], sep=" ")
        self.df["日時"] = pd.to_datetime(self.df["日時"])

        # 日付と時間だけの列を削除
        self.df = self.df.drop(["date", "time"], axis=1)


    def getdata(self):
        """
        """
        self.load_file()
        
        return self.df

    def kuwana_weather():
        """
        使っていない
        自動で取得できるとよいが・・
        """
        df = pd.read_csv("kuwana_weather.csv", skiprows=5, usecols=(0, 1))
        df.columns = ["日時", "気温"]
        df["日時"] = pd.to_datetime(df["日時"])
        # df = df.set_index("日時")
        return df


if __name__ == "__main__":
    path = "Z:/01_研究テーマ/14_三重IH改善/08_生産チャート/202106_GRW5102B0/amb/amb.csv"
    df = AmbTemp(path, 'chino').getdata()

    print(df)

