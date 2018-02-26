###  drawchart.py
###  描画モジュール

import matplotlib.pyplot as plt
import matplotlib.finance as mpf

### チャート描画
fig = plt.figure()
ax = plt.subplot()

#   ローソク足描画
def ohlc(Open,High,Low,Close):
    mpf.candlestick2_ohlc(ax,Open,High,Low,Close,width=0.8,colorup='#008800',colordown='#ff0000',alpha=0.75)


##  テクニカル指標描画
#   単純移動平均線
def sma(smaData,Color):
    ax.plot(smaData,color=Color)

##  ボリンジャーバンド
def Boll(center,upper,lower):
    ax.plot(center,color='#ff1493')
    ax.plot(upper,color='#ff1493')
    ax.plot(lower,color='#ff1493')


##  グラフタイトル
def title(Title):
    plt.title(Title)

##  グリッド表示
def grid():
    ax.grid()

##  x軸調整
def autofmtX():
    fig.autofmt_xdate()

##  単純プロット(test)
def plot(data,form,Color):
    ax.plot(data,form,color=Color)
    #print("plot")

    

def show():
    plt.show()

