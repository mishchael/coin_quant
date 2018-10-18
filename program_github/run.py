#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-14 00:42:23
# @Author  : Michael (mishchael@gmail.com)
import sys
# sys.path.append('/Users/michael/crypto_quant/program')
sys.path.append('/home/ubuntu/program')


from datetime import datetime, timedelta
import pandas as pd
from time import sleep
import ccxt
from trade.Trade import next_run_time, place_order, get_okex_candle_data, get_bfx_candle_data, auto_send_email
from strategy.Signals import signal_moving_average, signal_bolling, signal_bolling_with_stop_lose
from wx.common import *
from com.logger import Logger
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

"""
自动交易主要流程
 
# 通过while语句，不断的循环

# 每次循环中需要做的操作步骤
    1. 更新账户信息
    2. 获取实时数据
    3. 根据最新数据计算买卖信号 
    4. 根据目前仓位、买卖信息，结束本次循环，或者进行交易
    5. 交易
"""

# =====参数
time_interval = '5m'  # 间隔运行时间，不能低于5min

proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}
apiKey = ''  # 此处加上自己的apikey和secret，都需要开通交易权限
secret = ''
exchange = ccxt.bitfinex2()  # 创建交易所，此处为okex交易所
exchange.apiKey = apiKey
exchange.secret = secret
exchange.proxies = proxies
exchange_v1 = ccxt.bitfinex()
exchange_v1.apiKey = apiKey
exchange_v1.secret = secret
exchange_v1.proxies = proxies
symbol = 'EOS/BTC'  # 交易品种
base_coin = symbol.split('/')[-1]
trade_coin = symbol.split('/')[0]

para = [210, 2]  # 策略参数

# 微信
wechat = Send_Message()
# 日志
log_name = 'Script_Bolling_Stop_' + trade_coin + '_' + base_coin
log_path = '../logs/' + log_name + '.log'
log = Logger(name = log_name, path = log_path)
msg = log_name + '策略启动'
wechat.send_message('ZhangShiChao', msg)
log.info('策略启动')
exit()
# =====主程序
while True:
    # ===监控邮件内容
    msg_title = '策略报表' + '\n'
    msg_content = ''

    # ===从服务器更新账户balance信息
    balance = exchange.fetch_balance()['total']
    if base_coin in balance.keys():
        base_coin_amount = float(balance[base_coin])
    else:
        base_coin_amount = 0.0
    if trade_coin in balance.keys():
        trade_coin_amount = float(balance[trade_coin])
    else:
        trade_coin_amount = 0.0
    print('当前资产:\n', base_coin, base_coin_amount, trade_coin, trade_coin_amount)
    # # ===sleep直到运行时间
    run_time = next_run_time(time_interval)
    sleep(max(0, (run_time - datetime.now()).seconds))
    while True:  # 在靠近目标时间时
        if datetime.now() < run_time:
            continue
        else:
            break

    # ===获取最新数据
    while True:
        # 获取数据
        df = get_bfx_candle_data(exchange, symbol, time_interval)
        # 判断是否包含最新的数据
        _temp = df[df['candle_begin_time_GMT8'] == (run_time - timedelta(minutes=int(time_interval.strip('m'))))]
        if _temp.empty:
            print('获取数据不包含最新的数据，重新获取')
            continue
        else:
            print('已获取最新的数据')
            break
    
    # ===产生交易信号
    df = df[df['candle_begin_time_GMT8'] < pd.to_datetime(run_time)]  # 去除target_time周期的数据
    # df = signal_moving_average(df, para=para)
    df = signal_bolling_with_stop_lose(df, para = para + [5])
    signal = df.iloc[-1]['signal']
    print('\n交易信号', signal)
    print(df)
    exit()
    # =====卖出品种
    if trade_coin_amount > 0 and signal == 0:
        print('\n卖出')
        # 获取最新的卖出价格
        price = exchange.fetch_ticker(symbol)['bid']  # 获取买一价格
        # 下单
        sell_amount = trade_coin_amount * 3
        # place_order(exchange, order_type='limit', buy_or_sell='sell', symbol=symbol, price=price*0.98, amount=trade_coin_amount)
        place_order(exchange_v1, order_type='limit', buy_or_sell='sell', symbol=symbol, price=price*1000, amount=sell_amount)
        # 邮件标题
        msg_title += '_卖出_' + trade_coin + '\n'
        # 邮件内容
        msg_content += '卖出信息：\n'
        msg_content += '卖出数量：' + str(trade_coin_amount) + '\n'
        msg_content += '卖出价格：' + str(price) + '\n'

        wechat.send_message('ZhangShiChao', msg_title.encode('utf-8') + msg_content.encode('utf-8'))
        log.info(msg_title + msg_content)

    # =====买入品种
    if trade_coin_amount == 0 and signal == 1:
        print('\n买入')
        # 获取最新的买入价格
        price = exchange.fetch_ticker(symbol)['ask']  # 获取卖一价格
        # 计算买入数量
        buy_amount = base_coin_amount / price * 3
        # 获取最新的卖出价格
        # place_order(exchange, order_type='limit', buy_or_sell='buy', symbol=symbol, price=price*1.02, amount=buy_amount)
        place_order(exchange_v1, order_type='limit', buy_or_sell='buy', symbol=symbol, price=price*0.0001, amount=buy_amount)
        # 邮件标题
        msg_title += '_买入_' + trade_coin + '\n'
        # 邮件内容
        msg_content += '买入信息：\n'
        msg_content += '买入数量：' + str(buy_amount) + '\n'
        msg_content += '买入价格：' + str(price) + '\n'

        wechat.send_message('ZhangShiChao', msg_title.encode('utf-8') + msg_content.encode('utf-8'))
        log.info(msg_title + msg_content)



    # =====发送邮件
    # 每个半小时发送邮件
    if run_time.minute % 30 == 0:
        # 发送邮件
        auto_send_email('2151680@qq.com', msg_title, msg_content)

    # =====本次交易结束
    print(msg_title)
    print(msg_content)
    print('=====本次运行完毕\n')
    sleep(6 * 1)
