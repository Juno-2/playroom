###  main3.py
###  始点program

#　必要モジュール
from binance.client import Client
#  認証モジュール
from Keys import *
#  データ作成
import numpy as np
import pandas as pd
#  描画モジュール
import drawchart as dc
#  自動取引モジュール
import systemTrade as st
#  時刻取得
from datetime import datetime,timedelta
#　取得間隔モジュール
from Interval import *
#  データ取得
import getData as gd
#  BTCペア
import SymbolBTC as bt
#  ETHペア
import SymbolETH as et
#  USDTペア
import SymbolUSDT as us

#  ろうそく足
Open = np.array([])  # 始値
High = np.array([])  # 高値
Low = np.array([])   # 低値
Close = np.array([]) # 終値
Candle = [Open,High,Low,Close] #ろうそく足

#  時刻
time = np.array([])
     
#  テクニカル
sma7 = np.array([])
sma25 = np.array([])
boll = np.array([])
upper_band = np.array([])
lower_band = np.array([])

#  現在時刻取得
#Now = datetime.now().strftime("%m/%d %H:%M:%S")

#  データ取得
gd.Klines(Candle,time,bt.eth,fiveMin,"2 day ago UTC")
#  4値格納
Open = np.append(Open,Candle[0])
High = np.append(High,Candle[1])
Low = np.append(Low,Candle[2])
Close = np.append(Close,Candle[3])

#  test
print(time)

#  時刻反転
Ttime = time[::-1]

#  時刻込み2次元配列 
#OPen = np.append(Open,Ttime).reshape(2,96)
#HIgh = np.append(High,Ttime).reshape(2,96)
#LOw = np.append(Low,Ttime).reshape(2,96)
#CLose = np.append(Close,Ttime).reshape(2,96)


### テクニカル
#  単純移動平均線
#  sma7
sma7 = pd.Series(Close).rolling(window=7).mean()
#  sma25
sma25 = pd.Series(Close).rolling(window=25).mean()

#  ボリンジャーバンド
boll = pd.Series(Close).rolling(window=21).mean()
rstd = pd.Series(Close).rolling(window=21).std()
upper_band = boll + rstd * 2
lower_band = boll - rstd * 2

Technical = [sma7,sma25,boll,upper_band,lower_band]

###
st.auto(Candle,Technical,time)


#print(Ttime)


####  test




####

###  チャート描画
#    ローソク描画
dc.ohlc(Open,High,Low,Close)
#    単純移動平均(7,25)
#dc.sma(sma7,'#4682b4')
#dc.sma(sma25,'#ffa500')
#    ボリンジャーバンド
dc.Boll(boll,upper_band,lower_band)
#    グリッド表示
dc.grid()
#    タイトル(symbol)
dc.title('ETH/BTC')
#    x軸の調整
dc.autofmtX()

#  エントリーポイント描画
dc.plot(trade_rate,"ro",'#ffff00')

#  日付作成
#ax.set_xlim(Ttime[0],Ttime[95])

#    図表示
dc.show()
