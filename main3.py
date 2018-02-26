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


###  バックテスト
#  
vStockBTC = 1.0  #BTC
vStockETH = 0.0  #ETH
inventry = 0.0 #在庫
lot = 0.001  #ロット
up_flag = 0
under_flag = 0
bid = 0.0  
ask = 0.0
all_fee = 0.0
trans_fee = 0.0
trade = 0
trade_rate = np.array([])


##  トレードアルゴ
##
##
for index,item in enumerate(upper_band):
    if High[index] >= upper_band[index]:
        print("upper boll touch! time: "+str(index))
        up_flag = 1
        #  time update
        trade_rate = np.append(trade_rate,np.nan)
          
    elif up_flag == 1 and High[index] <= upper_band[index]:
        print("go down! sell! time: "+str(index))
        up_flag = 0
        if index == 575:
            bid = (High[index] + Low[index])
        else:
            bid = (High[index+1] + Low[index+1]) / 2
        #   time update
        if vStockETH > 0.0:
            vStockBTC += vStockETH * bid
            trans_fee = vStockBTC * 0.001
            vStockBTC -= trans_fee
            #all_fee += trans_fee
            vStockETH = 0.0
            trade += 1
            trade_rate = np.append(trade_rate,bid)
        else:
            trade_rate = np.append(trade_rate,np.nan)
            
    elif Low[index] <= lower_band[index]:
        print("under boll touch! time: "+str(index))
        under_flag = 1
        #  time update
        trade_rate = np.append(trade_rate,np.nan)

    elif under_flag == 1 and Low[index] >=lower_band[index]:
        print("go up! buy! time: "+str(index))
        under_flag = 0
        if index == 575:
            ask = (High[index] + Low[index])
        elif index < 575:
            ask = (High[index+1] + Low[index+1]) / 2
        #   time update    
        if vStockBTC > 0.0 and index == 575:
            #vStockBTC -= -1 * lot
            print("No buy")
            trade_rate = np.append(trade_rate,np.nan)
        elif vStockBTC > 0.0:
            vStockETH += vStockBTC / ask
            trans_fee = vStockETH * 0.001
            vStockETH -= trans_fee
            #all_fee += trans_fee
            vStockBTC = 0.0
            trade += 1
            trade_rate = np.append(trade_rate,ask)
        else:
            trade_rate = np.append(trade_rate,np.nan)

    
    #   time update
    elif index == 575:
        print("back to BTC")
        vStockBTC += vStockETH * bid
        trans_fee = vStockBTC * 0.001
        vStockBTC -= trans_fee
        #all_fee += trans_fee
        vStockETH = 0.0
        trade += 1
        trade_rate = np.append(trade_rate,bid)


    else:
        trade_rate = np.append(trade_rate,np.nan)

###  result表示      
print("-----result-----")
print("first asset: 1.0BTC ")
print("final BTC: "+str(vStockBTC))
print("final ETH: "+str(vStockETH))
#print("transaction fee: "+str(fee)+"BTC")

print("num of transactions: "+str(trade))
print("time of transactions: ")
#print(trade_time)
print("-----profit-----")
print(str(vStockBTC-1.0)+"BTC")

print(Ttime)


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
