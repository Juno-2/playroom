###  drawchart.py
###  描画モジュール

import matplotlib.pyplot as plt
import matplotlib.finance as mpf

### チャート描画
fig = plt.figure()
ax = plt.subplot()

##  ローソク足描画
def Ohlc(Open,High,Low,Close):
    mpf.candlestick2_ohlc(ax,Open,High,Low,Close,width=0.8,colorup='#008800',colordown='#ff0000',alpha=0.75)

##  テクニカル指標描画
##  単純移動平均線
def Sma(SmaData,Color):
    ax.plot(SmaData,color=Color)

##  ボリンジャーバンド
def Boll(Center,Upper,Lower):
    ax.plot(Center,color='#ff1493')
    ax.plot(Upper,color='#ff1493')
    ax.plot(Lower,color='#ff1493')

##  グラフタイトル
def Title(Title):
    plt.title(Title)

##  グリッド表示
def Grid():
    ax.grid()

##  x軸調整
def AutofmtX():
    fig.autofmt_xdate()

##  単純プロット(test)
def Plot(Data,Form,Color):
    ax.plot(Data,Form,color=Color)
    #print("plot")

##  図表示 
def Show():
    plt.show()


##  描画
def Draw(Candle,Technical,Result,Symbol,Indicator):
    #  ローソク描画
    Ohlc(Candle[0],Candle[1],Candle[2],Candle[3])
    #　テクニカル描画
    if Indicator == 'Sma':
        Sma(Technical[0],'#4682b4')
        Sma(Technical[1],'#ffa500')
    elif Indicator == 'Boll':
        Boll(Technical[2],Technical[3],Technical[4])
    else:
        print("no indicator")
    #  タイトル描画
    Title(Symbol)
    #  グリッド表示
    Grid()
    #  x軸調整
    AutofmtX()
    #  エントリーポイント描画
    Plot(Result[0],"ro",'#ffff00')
    #  日付作成
    #ax.set_xlim(Ttime[0],Time[95])

    #  図表示
    Show()

        


