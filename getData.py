###  getData.py
###  データ取得
#    バイナンスAPI
from binance.client import Client
#    認証鍵
from Keys import *
#    データ成形
import numpy as np
import pandas as pd
#    日付取得
from datetime import datetime,timedelta
#    取得間隔自動補正
import interval_number as inum
#    正規表現
import re
#    認証
client = Client(api_key,api_secret)


###  現在時刻からperiodまでの期間の4値データ取得
#  @param:      引数
#     Candle:   配列[ローソク足データ(4値)]
#     Time:     配列[時刻]
#     Symbol:   通貨ペア
#     Interval: 取得間隔
#     Period:   取得期間
def Klines(Candle,Symbol,Interval,Period):
    Now = datetime.now()
    times = np.array([])
    count = 0
    interval = inum.toNum(Interval)
    timeflag = inum.toFlag(Interval)
    delta = 0
    #   現在時刻からperiodまでの期間の4値データ取得
    klines = client.get_historical_klines(Symbol,Interval,Period)
    for index,item in enumerate(klines):
        #  始値
        Candle[0] = np.append(Candle[0],float(klines[index][1]))
        #  高値
        Candle[1] = np.append(Candle[1],float(klines[index][2]))
        #  低値
        Candle[2] = np.append(Candle[2],float(klines[index][3]))
        #  終値
        Candle[3] = np.append(Candle[3],float(klines[index][4]))
        #  出来高
        Candle[5] = np.append(Candle[5],float(klines[index][5]))
        #  時刻
        delta = -1 * interval * count                              
        if timeflag == 0:
            times = np.append(times, (Now + timedelta(minutes=(delta))))
        elif timeflag == 1:
            times = np.append(times, (Now + timedelta(hours=(delta))))
        elif timeflag == 2:
            times = np.append(times, (Now + timedelta(days=(delta))))
        elif timeflag == 3:
            times = np.append(times, (Now + timedelta(weeks=(delta))))
        elif timeflag == 4:
            #times = np.append(times, (Now + timedelta(months=(delta))))
            print("月減算未実装:python-dateutil")
            
        count += 1
    #Time.append(times[::-1])
    Candle[4] = np.append(Candle[4],times[::-1])
    #print("in getData")
    #print(Candle[5])

