###  main3.py
###  始点program

#  データ作成
import numpy as np
#import pandas as pd
#  描画モジュール
import drawchart as dc
#  テクニカル分析モジュール
import technical as ta
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

###  各種データ定義
#  ろうそく足
Open = np.array([])  # 始値
High = np.array([])  # 高値
Low = np.array([])   # 低値
Close = np.array([]) # 終値
Time = np.array([])  # 時刻
Candle = [Open,High,Low,Close,Time] #ろうそく足

#  テクニカル
sma7 = np.array([])
sma25 = np.array([])
boll = np.array([])
upper_band = np.array([])
lower_band = np.array([])
Technical = [sma7,sma25,boll,upper_band,lower_band]

#  自動取引結果
EntryPoint = np.array([])

Result = [EntryPoint]
###


#  現在時刻取得
#Now = datetime.now().strftime("%m/%d %H:%M:%S")

###  データ取得
#    引数(ローソク足,時刻,通貨ペア(ref:Symbol~~.py),取得間隔(ref:Interval.py),取得期間(ref:後で作る)
gd.Klines(Candle,bt.eth,m5,"2 day ago UTC")
###

###  test OK
#print("----main---")
#print(Candle[4])
###  
##
###  テクニカルデータ生成
#    引数(ローソク足,テクニカルデータ)
ta.TechAnalytic(Candle,Technical)
###

###  自動取引
#    引数(ローソク足,テクニカルデータ,結果用配列)
st.auto(Candle,Technical,Result)
###


####  test

####


###  描画
#    引数(ローソク足,テクニカルデータ,自動取引結果,チャートタイトル(通貨ペア),インジケータ(Sma,Boll))
dc.Draw(Candle,Technical,Result,'ETH/BTC','Sma')
###



