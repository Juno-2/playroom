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
#    認証
client = Client(api_key,api_secret)

def Klines(candle,Time,symbol,interval,period):
    Now = datetime.now()
    time = np.array([])
    count = 0
    delta = 0
    klines = client.get_historical_klines(symbol,interval,period)
    for index,item in enumerate(klines):
        #  始値
        candle[0] = np.append(candle[0],float(klines[index][1]))
        #  高値
        candle[1] = np.append(candle[1],float(klines[index][2]))
        #  低値
        candle[2] = np.append(candle[2],float(klines[index][3]))
        #  終値
        candle[3] = np.append(candle[3],float(klines[index][4]))
        #  時刻
        delta = -1 * 5 * count
        time = np.append(time, (Now + timedelta(minutes=(delta))))

        count += 1
    Time = np.append(Time,time)
    #print(Time)

