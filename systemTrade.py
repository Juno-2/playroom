### systemTrade.py
##  システムトレード

import numpy as np

### 初期化
def sysInit():

    ##　初期アセット
    vStockBTC = 1.0  #BTC
    vStockETH = 0.0  #ETH
    inventry = 0.0   #在庫
    lot = 0.001      #ロット
    up_flag = 0      #上のバンドにタッチしたかのフラグ
    under_flag = 0   #下のバンドにタッチしたかのフラグ
    bid = 0.0        #bid:売り
    ask = 0.0        #ask:買い
    all_fee = 0.0    #合計手数料
    trans_fee = 0.0  #取引手数料
    trade = 0        #取引回数
    trade_rate = np.array([]) #取引レート,エントリーポイント
    print("ready")


### アルゴリズム

# @param:   引数
#    Candle:    ローソク足データ [始値,高値,低値,終値] 
#    Technical: テクニカルデータ [移動平均(7),移動平均(25),ボリンジャーバンド.真ん中(21),ボリンジャーバンド.上(21),ボリンジャーバンド.下(21)]
#    Time:      時間
#    Result:    結果入れる
def auto(Candle,Technical,Time,Result):
    #sysInit()
    vStockBTC = 1.0  #BTC
    vStockETH = 0.0  #ETH
    inventry = 0.0   #在庫
    lot = 0.001      #ロット
    up_flag = 0      #上のバンドにタッチしたかのフラグ
    under_flag = 0   #下のバンドにタッチしたかのフラグ
    bid = 0.0        #bid:売り
    ask = 0.0        #ask:買い
    all_fee = 0.0    #合計手数料
    trans_fee = 0.0  #取引手数料
    trade = 0        #取引回数
    trade_rate = np.array([])

    # 4値格納(ローソク足)
    Open = Candle[0]
    High = Candle[1]
    Low = Candle[2]
    Close = Candle[3]
    # テクニカル指標格納
    upper_band = Technical[3]
    lower_band = Technical[4]

    #print(Open)
    #### system trade
    for index, item in enumerate(upper_band):
        if High[index] >= upper_band[index]:
            print("upper boll touch! time :"+str(index))
            up_flag = 1
            #  time update
            trade_rate = np.append(trade_rate,np.nan)
        
        elif up_flag == 1 and High[index] <= upper_band[index]:
            print("go down! sell! time: "+str(index))
            up_flag = 0
            if index == 575:
                bid = (High[index] + Low[index]) / 2
            else:
                bid = (High[index+1] + Low[index+1]) / 2
            #   time update
            if vStockETH > 0.0:
                print("dk")
                vStockBTC += vStockETH * bid
                trans_fee = vStockBTC * 0.001
                vStockBTC -= trans_fee
                #all_fee += trans_fee
                vStockETH = 0.0
                trade += 1
                trade_rate = np.append(trade_rate,bid)
            else:
                trade_rate = np.append(trade_rate,np.nan)
        
        elif Low[index] <= lower_band[index] and index != 575:
            print("under boll touch! time: "+str(index))
            under_flag = 1
            #  time update
            trade_rate = np.append(trade_rate,np.nan)
         
        elif under_flag == 1 and Low[index] >=lower_band[index] and index != 575:
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


    ##### 結果表示
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
    Result[0] = np.append(Result[0],trade_rate)

