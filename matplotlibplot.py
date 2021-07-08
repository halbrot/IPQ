import matplotlib.pyplot as plt
from preprocess import Preprocess
import edit_for_graph as efg
import datetime

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

def curves(path, graph_index):

    df, start_end_index = Preprocess(path).getdata()

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

    df = efg.get_characteristic_data(character)

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


def all_hist(path, character="carbide"):
    df, start_end_index = Preprocess(path).getdata()
    df = efg.get_characteristic_data(character)  # プロット期間を指定するために必要
    fig, ax = create_ax(1, 1, tatemm=50, yokomm=300)
    annotate_index = range(0, len(start_end_index) + 1, 100)
    histplot_datetime(df["日時"].iloc[0], df["日時"].iloc[-1], character, ax, **{"annotation_index": annotate_index})

    plt.tight_layout()
    plt.show()
