#　必要モジュール
from binance.client import Client
#  認証
from Keys import *
#  描画
import pandas as pd
import matplotlib.pyplot as plt
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

#  ticker
ticker = client.get_ticker(symbol=bt.eth)
ask = ticker['askPrice']
bid = ticker['bidPrice']
#print('ask:'+str(ask))
#print('bid:'+str(bid))
print(ticker)

