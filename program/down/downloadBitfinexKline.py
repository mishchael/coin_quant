# -*- coding: utf-8 -*-
import time
import ccxt
import datetime
import pandas as pd
import os

"""
AUTHOR : 小倩Sophie
FUNCTION : 从Bitfinex下载历史k线
DATE : Sep 15,2018
ENVIRONMENT : Python 2.7
NOTE:已设置断点续传。若有中断直接run程序即可。
"""
#---------- 定义函数，将任意毫秒级x变量转换为字符串，适用于单变量转换
def millisecondsToTime(milliseconds):
    timearr = time.localtime(milliseconds/1000)
    timeString = time.strftime("%Y-%m-%d %H:%M:%S", timearr)
    return timeString
#---------- 定义函数，将任意毫秒级x变量转换为字符串,为下面dataframe某一列批量做准备
f = lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x/1000))
def calcEnd():
    if os.path.exists(file_name):#如果已经存在数据文件，则读取数据文件中的最旧时间点为结束日期(即使程序中断，也可以直接继续下载)
        df = pd.read_csv(file_name,index_col=None)
        lenth = len(df)
        endDt=df.loc[lenth-1,'date']
        end = int(time.mktime(time.strptime(endDt, "%Y-%m-%d %H:%M:%S")))*1000
    else:
        end = datetime.datetime.strptime('2018101620', '%Y%m%d%H') #如果不存在数据文件，则以今天为结束时间
        end = int(time.mktime(end.timetuple())) * 1000
        endDt = millisecondsToTime(end)
    return end

def downKline(end):
    since = end - (limit) * 60 * int(timeframe.strip('m')) * 1000  # 计算每次抓取的起始时间(用k线数量*k线分钟数*60秒*1000毫秒/秒)
    data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since)[0:limit]
    df = pd.DataFrame(data=data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df = df.sort_values(by='date', ascending=False)
    df = df[(df['date'] < end) & (df['date'] >= since)]  # 筛选本次获取的df，保证在起止时间范围内，避免数据重复
    df['date'] = df['date'].map(f)  # 用上面的f函数，将df['date']中的每个单元格转换为时间字符串
    length = len(df)
    if length==0:
        startIsTrue = False
    else:
        startIsTrue = True
    sinceDt = millisecondsToTime(since)
    endDt = millisecondsToTime(end)
    if os.path.exists(file_name):
        df.to_csv(file_name, index=None, mode='a', header=False)  # 保存文档，如果已存在，则不保存列名
    else:
        df.to_csv(file_name, index=None, mode='a')

    print (u'==================已存储%s至%s的1分钟K线' % (sinceDt,endDt))
    print (df[:5])
    return startIsTrue
if __name__ == '__main__':
    exchange = ccxt.bitfinex2()  # 创建交易所，此处为bitfinex交易所
    exchange.proxies = {
        'http': 'socks5://127.0.0.1:1080',
        'https': 'socks5://127.0.0.1:1080'
    }# 请修改为自己的SOCKS5代理配置
    exchange.enableRateLimit = True 
    symbol = 'LTC/USDT'
    timeframe = '1m' # 设置k线频率
    limit = 999  # 设置每次获取k线的最大数量，避免服务器过大压力
    file_name = '../data/BITFINEX_LTC_USDT_1MIN.csv'
    startIsTrue = True

    while startIsTrue:
        end = calcEnd()
        startIsTrue = downKline(end)
        time.sleep(exchange.rateLimit / 1000)  # 一分钟请求20次以内
    print (u'数据获取完毕')


