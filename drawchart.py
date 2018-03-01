###  drawchart.py
###  描画モジュール
import re
import pandas as pd
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
    # /の挿入位置取得
    slash = re.search(r'BTC$',Title)
    if slash == None:
        slash = re.search(r'ETH$',Title)
    if slash == None:
        slash = re.search(r'USDT$',Title)
    # /加えて整形
    Titles = Title[:slash.start()] + '/' + Title[slash.start():]
    plt.title(Titles)

##  グリッド表示
def Grid():
    ax.grid()

##  日付表示
def Set_xlabels(DataFrame):
    ax.set_xticklabels([(DataFrame.index[int(x)].strftime("%m-%d %H:%M:%S") if x < DataFrame.shape[0] else x) for x in ax.get_xticks()], rotation=30)
    #ax.set_xlim([0,DataFrame.shape[0]])

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
    #  データフレーム作成
    df = pd.DataFrame({'Open':Candle[0], 'High':Candle[1], 'Low':Candle[2], 'Close':Candle[3]}, index = Candle[4])
    #  ローソク描画
    Ohlc(df['Open'],df['High'],df['Low'],df['Close'])                                                
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
    #  日付表示
    Set_xlabels(df)
    #  グリッド表示
    Grid()
    #  x軸調整
    AutofmtX()
    #  エントリーポイント描画
    Plot(Result[0],"ro",'#ffff00')
    #  図表示
    Show()

        


