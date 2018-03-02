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
##  ろうそく足
Open = np.array([])     # 始値
High = np.array([])     # 高値
Low = np.array([])      # 低値
Close = np.array([])    # 終値
Time = np.array([])     # 時刻
Volume = np.array([])   # 出来高
Candle = [Open,High,Low,Close,Time,Volume] #ろうそく足

##  テクニカル                    
sma7 = np.array([])         #単純移動平均(MA)
sma25 = np.array([])        #単純移動平均(MA)
boll = np.array([])         #ボリンジャーバンド(BOLL)
upper_band = np.array([])   #ボリンジャーバンド上(BOLL)
lower_band = np.array([])   #ボリンジャーバンド下(BOLL)
ema12 = np.array([])        #指数移動平均(MACD)
ema26 = np.array([])        #指数移動平均(MACD)
ema9 = np.array([])         #指数移動平均(MACD)
macd = np.array([])         #MACD(MACD)
histgram =np.array([])      #棒グラフ(MACD)
Technical = [sma7,sma25,boll,upper_band,lower_band,ema12,ema26,ema9,macd,histgram]

##  自動取引
EntryPoint = np.array([])
FirstAsset = np.array([])
Result = [EntryPoint,FirstAsset]
###

### Backtest
# 通貨ペア 
Symbol = us.btc
#Symbol = bt.eth 
# 初期保有通貨量=FirstAsset(float)
Result[1] = 10000.0
###


#  現在時刻取得
#Now = datetime.now().strftime("%m/%d %H:%M:%S")

###  データ取得
#    引数(ローソク足,時刻,通貨ペア(ref:Symbol~~.py),取得間隔(ref:Interval.py),取得期間(ref:後で作る)
gd.Klines(Candle,Symbol,m5,"2 day ago UTC")
###

###  test OK
#print("----main---")
#print(Candle[4])
###  

###  テクニカルデータ生成
#    引数(ローソク足,テクニカルデータ)
ta.TechAnalytic(Candle,Technical)
###

###  自動取引
#    初期設定
#    引数(ローソク足,テクニカルデータ,通貨ペア,結果用配列)
st.auto(Candle,Technical,Symbol,Result)
###


####  test

####


###  描画
#    引数(ローソク足,テクニカルデータ,自動取引結果,チャートタイトル(通貨ペア),インジケータ(Sma,Boll))
dc.Draw(Candle,Technical,Result,Symbol,'Boll')
###



