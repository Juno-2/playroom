###  interval_number.py
###  取得間隔補正

#    正規表現モジュール
import re


###  取得間隔補正
#    引数(取得間隔(ref:Interval.py))
#    マッチした数字を返す
def toNum(interval):
    jud = re.search(r'[0-9]+',interval)
    return int(jud.group())

###  時刻減算単位判定
#    引数(取得間隔(ref:Interval.py)
#    マッチした位置を返す(0:Min,1:Hour,2:Day,3:Week,4:Month)
def  toFlag(Interval):
    print(Interval)
    time = []
    time.append(re.search(r'[0-9]+m',Interval))
    time.append(re.search(r'[0-9]+h',Interval))
    time.append(re.search(r'[0-9]+d',Interval))
    time.append(re.search(r'[0-9]+w',Interval))
    time.append(re.search(r'[0-9]+M',Interval))
    
    print(time)
    for index,item in enumerate(time):
        if item != None:
            return int(index)


