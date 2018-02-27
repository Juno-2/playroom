###  technical.py
###  テクニカル指標

import pandas as pd
import numpy as np

#    配列位置指定
tIndex = 0

###  配列位置: +=1
def AddIndex():
    global tIndex
    tIndex += 1

###  データセット
#
#  @param:     引数
#     Tech:    配列[テクニカル指標]
#     addData: 入れたいデータ
#     index:   配列位置指定
def AddData(Tech,addData,index):
    Tech[index] = np.append(Tech[index],addData)    

###　単純移動平均線
#      
#  @param:    引数
#     Close:  終値
#     Window: 期間
def Sma(Tech,index,Close,Window):
    sma = pd.Series(Close).rolling(window=Window).mean()
    AddData(Tech,sma,index)
    AddIndex()

###  ボリンジャーバンド
#
#  @param:    引数
#     Close:  終値
#     Window: 期間
def Boll(Tech,Index,Close,Window):
    boll = pd.Series(Close).rolling(window=21).mean()
    rstd = pd.Series(Close).rolling(window=21).std()
    upper_band = boll + rstd * 2
    lower_band = boll - rstd * 2
    #  データセット
    AddData(Tech,boll,Index)
    AddData(Tech,upper_band,Index+1)
    AddData(Tech,lower_band,Index+2)

###  テクニカル分析全般
#
#  @param:     引数
#     Candle:  ローソク足データ
#     Tech:    テクニカル分析データ
def TechAnalytic(Candle,Tech):
    #Open = Candle[0]
    #High = Candle[1]
    #Low = Candle[2]
    Close = Candle[3]

    #  配列位置指定(グローバル変数)
    global tIndex

    #  移動平均
    Sma(Tech,tIndex,Close,7)
    Sma(Tech,tIndex,Close,25)
    #  ボリンジャー
    Boll(Tech,tIndex,Close,21)
    #print(Tech)
