###  drawchart.py
###  描画モジュール
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.finance as mpf

### チャート描画
fig = plt.figure()
ax = fig.add_axes((0.05,0.32,0.9,0.62))
ax2 = fig.add_axes((0.05,0.21,0.9,0.1),sharex=ax)
ax3 = fig.add_axes((0.05,0.1,0.9,0.1),sharex=ax2)
#test
#fig2 = plt.figure()
#cx = plt.subplot()

##  ローソク足and出来高描画
def Ohlc(Open,High,Low,Close,Volume,MACD):
    # 出来高,MACDのy軸ラベルとチャート,出来高のx軸のラベルを非表示
    ax.tick_params(labelbottom="off")
    ax2.tick_params(labelbottom="off",labelleft='off')
    mpf.candlestick2_ohlc(ax,Open,High,Low,Close,width=0.8,colorup='#008800',colordown='#ff0000',alpha=0.75)
    mpf.volume_overlay(ax2,Open,Close,Volume,width=1,colorup='#008800',colordown='#ff0000')

##  テクニカル指標描画
##  単純移動平均線
def Sma(SmaData,Color):
    ax.plot(SmaData,color=Color)
    
##  ボリンジャーバンド
def Boll(Center,Upper,Lower):
    ax.plot(Center,color='#ff1493')
    ax.plot(Upper,color='#ff1493')
    ax.plot(Lower,color='#ff1493')

##  MACD
def Macd(Short,Long,Histgram,Time):
    ax3.set_yticks([0])
    ax3.plot(Short,color='#4682b4')
    ax3.plot(Long,color='#ffa500')
    ###  棒グラフ表示できない！(Histgram)
    #l = list(Time)
    #h = list(Histgram)
    #print(l)
    ##Time['histgram'].plot.bar(ax=cx3,rot=30)
    #cx3.bar(l,Histgram,color='#ff1493')
    #cx3.plot(Histgram,color='#ff1493')
    #print("macd")

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
    ax.set_title(Titles)

##  グリッド表示
def Grid():
    ax.grid()

##  日付表示
def Set_xlabels(DataFrame):
    ax3.set_xticklabels([(DataFrame.index[int(x)].strftime("%m-%d %H:%M:%S") if x < DataFrame.shape[0] else x) for x in ax3.get_xticks()], rotation=30)
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
    df = pd.DataFrame({'Open':Candle[0], 'High':Candle[1], 'Low':Candle[2], 'Close':Candle[3], 'Volume':Candle[5]}, index = Candle[4])
    df1 = pd.DataFrame({'ema':Technical[7], 'signal':Technical[8], 'histgram':Technical[9]}, index = Candle[4])
    #  ローソク描画
    Ohlc(df['Open'],df['High'],df['Low'],df['Close'],df['Volume'],df1)                                                
    #　テクニカル描画
    if Indicator == 'Sma':
        Sma(Technical[0],'#4682b4')
        Sma(Technical[1],'#ffa500')
    elif Indicator == 'Boll':
        Boll(Technical[2],Technical[3],Technical[4])
    else:
        print("no indicator")
    #  ema表示
    Macd(Technical[7],Technical[8],Technical[9],Candle[4])
    #  タイトル描画
    Title(Symbol)
    #  日付表示
    Set_xlabels(df)
    #  グリッド表示
    Grid()
    #  x軸調整
    AutofmtX()
    #  エントリーポイント描画
    Plot(Result[0],"o",'#ffff00')
    
    #  図表示
    Show()

        


