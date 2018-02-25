#　必要モジュール
from binance.client import Client
#  認証
from Keys import *
#  描画
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
#  時刻取得
from datetime import datetime,timedelta
#　取得間隔モジュール
from Interval import *
#  BTCペア
import SymbolBTC as bt
#  ETHペア
import SymbolETH as et
#  USDTペア
import SymbolUSDT as us

#  認証
client = Client(api_key,api_secret)
#  ろうそく足
Open = np.array([])  # 始値
Close = np.array([]) # 終値
High = np.array([])  # 高値
Low = np.array([])   # 低値

#  現在時刻取得
#Now = datetime.now().strftime("%m/%d %H:%M:%S")
Now = datetime.now()

time = np.array([])
count = 0
delta = 0

#  テクニカル
sma7 = np.array([])
sma25 = np.array([])
boll = np.array([])
upper_band = np.array([])
lower_band = np.array([])


#  draw charts
klines = client.get_historical_klines(bt.eth,fiveMin,"2 day ago UTC")
for index, item in enumerate(klines):
    #  始値
    Open = np.append(Open,float(klines[index][1]))
    #print(Open[index])
    #  高値
    High = np.append(High,float(klines[index][2]))
    #  低値
    Low = np.append(Low,float(klines[index][3]))
    #  終値
    Close = np.append(Close,float(klines[index][4]))
    #  時刻
    delta = -1 * 5 * count
    time = np.append(time, (Now + timedelta(minutes=(delta))))
    
    
    count += 1
    
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
fee = 0.0
trade = 0
trade_time = np.array([])


##  トレードアルゴ
##
##
for index,item in enumerate(upper_band):
    if High[index] >= upper_band[index]:
        print("upper boll touch! time: "+str(index))
        up_flag = 1

    elif up_flag == 1 and High[index] <= upper_band[index]:
        print("go down! sell! time: "+str(index))
        up_flag = 0
        if index == 575:
            bid = (High[index] + Low[index])
        else:
            bid = (High[index+1] + Low[index+1]) / 2
        
        if vStockETH > 0.0:
            vStockBTC += vStockETH * bid
            fee += vStockBTC * 0.001
            vStockETH = 0.0
            trade += 1
            trade_time = np.append(trade_time,index)
    elif Low[index] <= lower_band[index]:
        print("under boll touch! time: "+str(index))
        under_flag = 1

    elif under_flag == 1 and Low[index] >=lower_band[index]:
        print("go up! buy! time: "+str(index))
        under_flag = 0
        if index == 575:
            ask = (High[index] + Low[index])
        elif index < 575:
            ask = (High[index+1] + Low[index+1]) / 2
        if vStockBTC > 0.0 and index == 575:
            #vStockBTC -= -1 * lot
            print("No buy")
        elif vStockBTC > 0.0:
            vStockETH += vStockBTC / ask
            fee += vStockBTC * 0.001
            vStockBTC = 0.0
            trade += 1
            trade_time = np.append(trade_time,index)

    elif index == 575:
        print("back to BTC")
        vStockBTC += vStockETH * bid
        fee += vStockBTC * 0.001
        vStockETH = 0.0
        trade += 1
        trade_time = np.append(trade_time,index)


    #else:
    #    trade_time = np.append(trade_time,0)

###  result表示      
print("-----result-----")
print("first asset: 1.0BTC ")
print("final BTC: "+str(vStockBTC))
print("final ETH: "+str(vStockETH))
print("transaction fee: "+str(fee)+"BTC")

print("num of transactions: "+str(trade))
print("time of transactions: ")
print(trade_time)
print("-----profit-----")
print(str(vStockBTC-1.0)+"BTC")


###  チャート描画
fig = plt.figure()
ax = plt.subplot()

#  ローソク足描画
mpf.candlestick2_ohlc(ax,Open,High,Low,Close,width=0.8,colorup='#008000',colordown='#ff0000',alpha=0.75)
#mpf.candlestick2_ohlc(ax,OPen,HIgh,LOw,CLose,width=0.8,colorup='g',colordown='r',alpha=0.75)
## テクニカル描画
#  7MA描画
#ax.plot(sma7,color="#4682b4")
#  25MA描画
#ax.plot(sma25,color="#ffa500")
#  ボリンジャーバンド描画
ax.plot(boll,color="#ff1493")
ax.plot(upper_band,color="#ff1493")
ax.plot(lower_band,color="#ff1493")

#  エントリーポイント描画
#ax.plot(trade_time,"ro",color="#ffff00")

#  日付作成
#ax.set_xlim(Ttime[0],Ttime[95])

#  グリッド表示
ax.grid()
#  x軸の調整
fig.autofmt_xdate()
#  タイトル
plt.title("ETH/BTC")
#  図表示
plt.show()
