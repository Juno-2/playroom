### systemTrade.py
##  システムトレード
import re
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

### 通貨ペア取得
def GetPair(Symbol):
    #  pair2/pair1
    pair = re.search(r'BTC$',Symbol)
    if pair == None:
        pair = re.search(r'ETH$',Symbol)
    if pair == None:
        pair = re.search(r'USDT$',Symbol)
    
    pair1 = Symbol[pair.start():]
    pair2 = Symbol[:pair.start()]
    #print(pair2 + '/' + pair1)
    return [pair1,pair2]

##  bid,ask取得
def GetPrice(High,Low,Index,CandleLength):
    if Index == CandleLength:
        return (High[Index] + Low[Index]) / 2
    elif Index < CandleLength:
        return (High[Index+1] + Low[Index+1]) / 2
    else:
        print("error")
        return 0

### アルゴリズム

# @param:   引数
#    Candle:    ローソク足データ [始値,高値,低値,終値,時刻] 
#    Technical: テクニカルデータ [移動平均(7),移動平均(25),ボリンジャーバンド.真ん中(21),ボリンジャーバンド.上(21),ボリンジャーバンド.下(21)]
#    Symbol:    通貨ペア
#    Result:    結果入れる
def auto(Candle,Technical,Symbol,Result):
    #sysInit()
    # 通貨ペア 'pair2/pair1'
    #vStock = []
    # 初期保有量
    vStockPair2 = 0.0       #Pair2:
    vStockPair1 = Result[1] #Pair1:
    inventry = 0.0   #在庫
    #lot = 0.001      #ロット
    up_flag = 0      #上のバンドにタッチしたかのフラグ
    under_flag = 0   #下のバンドにタッチしたかのフラグ
    bid = 0.0        #bid:売り
    ask = 0.0        #ask:買い
    all_fee = 0.0    #合計手数料
    trans_fee = 0.0  #取引手数料
    trade = 0        #取引回数
    trade_rate = np.array([])
    # 通貨ペア取得
    vStock = GetPair(Symbol)
    #print(vStock)
    # 4値格納(ローソク足)
    Open = Candle[0]
    High = Candle[1]
    Low = Candle[2]
    Close = Candle[3]
    # テクニカル指標格納
    upper_band = Technical[3]
    lower_band = Technical[4]
    # 長さ取得
    CandleLength = len(Candle[0])-1
 
    #### system trade
    for index, item in enumerate(upper_band):
        if index == CandleLength:
            print("back to BTC")
            vStockPair1 += vStockPair2 * bid
            trans_fee = vStockPair1 * 0.001
            vStockPair1 -= trans_fee
            #all_fee += trans_fee
            vStockPair2 = 0.0
            trade += 1
            trade_rate = np.append(trade_rate,bid)
        
        elif High[index] >= upper_band[index] and index != CandleLength:
            print("upper boll touch! time :"+str(index))
            up_flag = 1
            #  time update
            trade_rate = np.append(trade_rate,np.nan)
        
        elif up_flag == 1 and High[index] <= upper_band[index]:
            print("go down! sell! time: "+str(index))
            up_flag = 0
            bid = GetPrice(High,Low,index,CandleLength)
            #  time update
            if vStockPair2 > 0.0:
                vStockPair1 += vStockPair2 * bid
                trans_fee = vStockPair1 * 0.001
                vStockPair1 -= trans_fee
                #all_fee += trans_fee
                vStockPair2 = 0.0
                trade += 1
                trade_rate = np.append(trade_rate,bid)
            else:
                trade_rate = np.append(trade_rate,np.nan)
        
        elif Low[index] <= lower_band[index] and index != CandleLength:
            print("under boll touch! time: "+str(index))
            under_flag = 1
            #  time update
            trade_rate = np.append(trade_rate,np.nan)
         
        elif under_flag == 1 and Low[index] >=lower_band[index] and index != CandleLength:
            print("go up! buy! time: "+str(index))
            under_flag = 0
            ask = GetPrice(High,Low,index,CandleLength)
            #   time update    
            if vStockPair1 > 0.0 and index == CandleLength:
                #vStockBTC -= -1 * lot
                print("No buy")
                trade_rate = np.append(trade_rate,np.nan)
            elif vStockPair1 > 0.0:
                vStockPair2 += vStockPair1 / ask
                trans_fee = vStockPair2 * 0.001
                vStockPair2 -= trans_fee
                #all_fee += trans_fee
                vStockPair1 = 0.0
                trade += 1
                trade_rate = np.append(trade_rate,ask)
            else:
                trade_rate = np.append(trade_rate,np.nan)


        else:
            trade_rate = np.append(trade_rate,np.nan)


    ##### 結果表示
    print("-----result-----")
    print("first "+str(vStock[0])+": "+str(Result[1]))
    print("final "+str(vStock[0])+": "+str(vStockPair1))
    print("final "+str(vStock[1])+": "+str(vStockPair2))
    #print("transaction fee: "+str(fee)+"BTC")
     
    print("num of transactions: "+str(trade))
    print("time of transactions: ")
    #print(trade_time)
    print("-----profit-----")
    print(str(vStockPair1-Result[1])+str(vStock[0]))
    Result[0] = np.append(Result[0],trade_rate)

