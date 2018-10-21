#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-14 00:42:23
# @Author  : Michael (mishchael@gmail.com)ƒ
import sys
# sys.path.append('/Users/michael/crypto_quant/program')
sys.path.append('/home/ubuntu/program')

from datetime import datetime, timedelta
import pandas as pd
from time import sleep
import ccxt
from trade.Trade import *
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

# =====ccxt初始化=====
proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}
apiKey = ''  # 此处加上自己的apikey和secret，都需要开通交易权限
secret = ''
bfx2 = ccxt.bitfinex2()  # 创建交易所，此处为okex交易所
bfx2.apiKey = apiKey
bfx2.secret = secret
# bfx2.proxies = proxies
bfx2.load_markets()
bfx = ccxt.bitfinex()
bfx.apiKey = apiKey
bfx.secret = secret
# bfx.proxies = proxies
bfx.load_markets()

# =====交易品种=====
symbol = 'EOS/BTC'  # 交易品种
base_coin = symbol.split('/')[-1]
trade_coin = symbol.split('/')[0]


# =====参数=====
time_interval = '5m'  # 间隔运行时间，不能低于5min
para = [340, 0.5]  # 策略参数n, m
leverage = 3

# =====微信初始化=====
wechat = Send_Message()
# =====日志初始化=====
log_name = 'Script_Bolling_Stop_' + trade_coin + '_' + base_coin
log_path = '../logs/' + log_name + '.log'
log = Logger(name = log_name, path = log_path)

# =====记录日志=====
msg = log_name + '策略启动'
print(msg)
wechat.send_message('ZhangShiChao', msg)
log.info('策略启动')

# =====上次仓位信息=====
last_position = {}
# 初始仓位：无仓位
last_position['side'] = 'close'

# =====主程序=====
while True:
    # =====监控邮件内容=====
    email_title = '策略报表' + '\n'
    email_content = ''

    
    # ===margin账户余额===
    margin_balance = check_margin_balance(bfx)
    msg = '当前margin可用余额：%s BTC' % margin_balance
    print(msg)
    wechat.send_message('ZhangShiChao', msg)
    log.info(msg)


    # ===检查margin symbol持仓===
    margin_position = check_bfx_margin_positions(bfx2, symbol)

    # ===sleep直到运行时间===
    run_time = next_run_time(time_interval)
    sleep(max(0, (run_time - datetime.now()).seconds))
    while True:  # 在靠近目标时间时
        if datetime.now() < run_time:
            continue
        else:
            break

    # ===获取最新数据
    max_tries = 5
    no_data_flag = False
    less_data_flag = False
    while True:
        # 获取数据
        df = get_bfx_candle_data(bfx2, symbol, time_interval)
        # 如果K线数量少于参数n，无法产生交易信号
        if df.shape[0] < para[0]:
            less_data_flag = True
            msg = '本周期K线数量少于参数n，等待一下个周期'
            print(msg)
            wechat.send_message('ZhangShiChao', msg)
            log.info(msg)
            break
        # 判断是否包含最新的数据
        _temp = df[df['candle_begin_time_GMT8'] == (run_time - timedelta(minutes=int(time_interval.strip('m'))))]
        if (not df.empty) & _temp.empty:
            if max_tries > 0:
                msg = '获取数据不包含最新的数据，重新获取'
                print(msg)
                # wechat.send_message('ZhangShiChao', msg)
                log.info(msg)
                max_tries -= 1
                continue
            else:
                no_data_flag = True
                msg = '本周期无交易数据，等待一下个周期'
                print(msg)
                wechat.send_message('ZhangShiChao', msg)
                log.info(msg)
                break
        else:
            print('已获取最新的数据')
            break
    # 本周期无数据，运行下个周期
    if no_data_flag or less_data_flag:
        continue
    
    # ===产生交易信号
    df = df[df['candle_begin_time_GMT8'] < pd.to_datetime(run_time)]  # 去除target_time周期的数据
    # df = signal_moving_average(df, para=para)
    df = signal_bolling_with_stop_lose(df, para = para + [5])
    signal = df.iloc[-1]['signal']
    print(df.tail(10))
    print('\n交易信号', signal)
    

    # =====空仓——>做多/做空=====
    # 当前空仓
    # if not margin_position:
    if not margin_position:
        # margin账户有余额且信号为做多，开多
        if (margin_balance > 0) & (signal == 1):
            # 当前卖一价
            price = bfx2.fetch_ticker(symbol).get('ask') * 1.02
            # 买入数量
            amount = margin_balance * leverage / price
            order_info = place_bfx_order(bfx, symbol, 'limit', 'buy', amount, price , {'type': 'limit'})
            msg = '空仓开多，下单成功！\n买入品种：%s\n买入价格：%s\n买入数量：%s' % (symbol, price, amount)
            wechat.send_message('ZhangShiChao', msg)
            log.info(msg)
            email_content += msg
            # 检查仓位，确认是否已买入
            current_position = check_bfx_margin_positions(bfx2, symbol)
            if current_position:
                pos_status = current_position.get('status')
                pos_amount = current_position.get('amount')
                pos_side = current_position.get('side')
                pos_base_price = current_position.get('base_price')
                pos_leverage = current_position.get('leverage')
                if pos_status == 'AVTIVE' & pos_amount == amount:
                    msg = '开多成功！当前持仓：\n持仓状态：%s\n持仓方向：%s\n持仓数量：%s\n进入价格:%s\n持仓杠杆：%s' % (pos_status, pos_side, pos_amount, pos_base_price, pos_leverage)
                    print(msg)
                    wechat.send_message('ZhangShiChao', msg)
                    log.info(msg)
                    email_content += msg
                    # 记录本次仓位信息
                    last_position['side'] = 'long'
                    last_position['status'] = pos_status
                    last_position['amount'] = pos_amount
                    last_position['base_price'] = pos_base_price
                    last_position['leverage'] = pos_leverage
                else:
                    msg = '已下单，未交易！'
                    wechat.send_message('ZhangShiChao', msg)
                    log.info(msg)
        # margin账户有余额且信号为做空，开空
        if (margin_balance > 0) & (signal == -1):
            # 当前买一价
            price = bfx2.fetch_ticker(symbol).get('bid') * 0.98
            # 卖出数量
            amount = margin_balance * leverage / price
            order_info = place_bfx_order(bfx, symbol, 'limit', 'sell', amount, price , {'type': 'limit'})
            msg = '空仓开空，下单成功！\n卖出品种：%s\n卖出价格：%s\n卖出数量：%s' % (symbol, price, amount)
            wechat.send_message('ZhangShiChao', msg)
            log.info(msg)
            email_content += msg
            # 检查仓位，确认是否已卖出
            current_position = check_bfx_margin_positions(bfx2, symbol)
            if current_position:
                pos_status = current_position.get('status')
                pos_amount = current_position.get('amount')
                pos_side = current_position.get('side')
                pos_base_price = current_position.get('base_price')
                pos_leverage = current_position.get('leverage')
                if (pos_status == 'AVTIVE') & (pos_amount == amount):
                    msg = '开多成功！当前持仓：\n持仓状态：%s\n持仓方向：%s\n持仓数量：%s\n进入价格:%s\n持仓杠杆：%s' % (pos_status, pos_side, pos_amount, pos_base_price, pos_leverage)
                    print(msg)
                    wechat.send_message('ZhangShiChao', msg)
                    log.info(msg)
                    email_content += msg
                    # 记录本次仓位信息
                    last_position['side'] = 'long'
                    last_position['status'] = pos_status
                    last_position['amount'] = pos_amount
                    last_position['base_price'] = pos_base_price
                    last_position['leverage'] = pos_leverage
                else:
                    msg = '已下单，未交易！'
                    wechat.send_message('ZhangShiChao', msg)
                    log.info(msg)

    # =====持仓——>平仓/转换仓位=====
    # 当前持有仓位
    if margin_position:
        # 持有仓位，且为ACTIVE
        if margin_position.get('status') == 'ACTIVE':
            pos_side = margin_position.get('side')
            # =====持仓——>平仓=====
            # 当前持有多头且信号为平仓：卖出平仓,平掉多头
            if (last_position['side'] == 'long') & (pos_side == 'buy') & (signal == 0):
                # 当前买一价
                price = bfx2.fetch_ticker(symbol)['bid'] * 0.98
                amount = margin_position.get('amount')
                order_info = place_bfx_order(bfx, symbol, 'limit', 'sell', amount, price , {'type': 'limit'})
                msg = '做多平仓，下单成功！\n卖出品种：%s\n卖出价格：%s\n卖出数量：%s' % (symbol, price, amount)
                wechat.send_message('ZhangShiChao', msg)
                log.info(msg)
                email_content += msg
                # 检查仓位，确认是否已卖出
                current_position = check_bfx_margin_positions(bfx2, symbol)
                if not current_position:
                    msg = '做多平仓成功！'
                    print(msg)
                    wechat.send_message('ZhangShiChao', msg)
                    log.info(msg)
                    # 记录本次仓位信息
                    last_position['side'] = 'close'
                    last_position['status'] = 'close'
                    last_position['amount'] = 0
                    last_position['base_price'] = 0
                    last_position['leverage'] = 0
                else:
                    msg = '已下单，未交易！'
                    wechat.send_message('ZhangShiChao', msg)
                    log.info(msg)

            # 当前持有空头且信号为平仓：买入平仓,平掉空头
            if (last_position['side'] == 'short') & (pos_side == 'sell') & (signal == 0):
                # 平仓,平掉空头
                # 当前卖一价
                price = bfx2.fetch_ticker(symbol)['ask'] * 1.02
                amount = margin_position.get('amount')
                order_info = place_bfx_order(bfx, symbol, 'limit', 'buy', amount, price , {'type': 'limit'})
                msg = '做多平仓，下单成功！\n买入品种：%s\n买入价格：%s\n买入数量：%s' % (symbol, price, amount)
                wechat.send_message('ZhangShiChao', msg)
                log.info(msg)
                email_content += msg
                # 检查仓位，确认是否已买入
                current_position = check_bfx_margin_positions(bfx2, symbol)
                if not current_position:
                    msg = '做空平仓成功！'
                    print(msg)
                    wechat.send_message('ZhangShiChao', msg)
                    log.info(msg)
                    # 记录本次仓位信息
                    last_position['side'] = 'close'
                    last_position['status'] = 'close'
                    last_position['amount'] = 0
                    last_position['base_price'] = 0
                    last_position['leverage'] = 0
                else:
                    msg = '已下单，未交易！'
                    wechat.send_message('ZhangShiChao', msg)
                    log.info(msg)

            # =====持仓——>转换持仓方向=====
            # 当前持有多头且信号为做空：卖出平仓,继续卖出开空头
            if (last_position['side'] == 'long') & (pos_side == 'buy') & (signal == -1):
                # 当前买一价
                price = bfx2.fetch_ticker(symbol)['bid'] * 0.98
                amount = margin_position.get('amount')
                order_info = place_bfx_order(bfx, symbol, 'limit', 'sell', amount, price ,{'type': 'limit'})
                # 检查仓位，确认是否已卖出平仓,并开空头
                while True:
                    current_position = check_bfx_margin_positions(bfx2, symbol)
                    if not current_position:
                        msg = '做多平仓成功！准备开空头...'
                        print(msg)
                        wechat.send_message('ZhangShiChao', msg)
                        log.info(msg)
                        # 开空头
                        current_margin_balance = check_margin_balance(bfx)
                        if current_margin_balance > 0.0001: 
                            # 当前买一价
                            price = bfx2.fetch_ticker(symbol).get('bid') * 0.98
                            # 卖出数量
                            amount = current_margin_balance * leverage / price
                            order_info = place_bfx_order(bfx, symbol, 'limit', 'sell', amount, price , {'type': 'limit'})
                            msg = '开空头，下单成功！\n卖出品种：%s\n卖出价格：%s\n卖出数量：%s' % (symbol, price, amount)
                            wechat.send_message('ZhangShiChao', msg)
                            log.info(msg)
                            # 检查仓位，确认是否已卖出平仓
                            current_position = check_bfx_margin_positions(bfx2, symbol)
                            if current_position:
                                pos_status = current_position.get('status')
                                pos_amount = current_position.get('amount')
                                pos_side = current_position.get('side')
                                pos_base_price = current_position.get('base_price')
                                pos_leverage = current_position.get('leverage')
                                if (pos_status == 'AVTIVE') & (pos_amount == amount):
                                    msg = '开空成功！当前持仓：\n持仓状态：%s\n持仓方向：%s\n持仓数量：%s\n进入价格:%s\n持仓杠杆：%s' % (pos_status, pos_side, pos_amount, pos_base_price, pos_leverage)
                                    print(msg)
                                    wechat.send_message('ZhangShiChao', msg)
                                    log.info(msg)
                                    email_content += msg
                                    # 记录本次仓位信息
                                    last_position['side'] = 'short'
                                    last_position['status'] = pos_status
                                    last_position['amount'] = pos_amount
                                    last_position['base_price'] = pos_base_price
                                    last_position['leverage'] = pos_leverage
                                else:
                                    msg = '已下单，未交易！'
                                    wechat.send_message('ZhangShiChao', msg)
                                    log.info(msg)
                        break
                    else:
                        msg = '已下单，未交易！继续检查仓位并开空！'
                        wechat.send_message('ZhangShiChao', msg)
                        log.info(msg)
                        sleep(2)
                        continue
            # 当前持有空头且信号为做多：买入平仓,继续买入开多头
            if (last_position['side'] == 'short') & (pos_side == 'sell') & (signal == 1):
                # 当前卖一价
                price = bfx2.fetch_ticker(symbol)['ask'] * 1.02
                amount = margin_position.get('amount')
                order_info = place_bfx_order(bfx, symbol, 'limit', 'buy', amount, price ,{'type': 'limit'})
                # 检查仓位，确认是否已买入平仓,并开多头
                while True:
                    current_position = check_bfx_margin_positions(bfx2, symbol)
                    if not current_position:
                        msg = '做空平仓成功！准备开多头...'
                        print(msg)
                        wechat.send_message('ZhangShiChao', msg)
                        log.info(msg)
                        # 开空头
                        current_margin_balance = check_margin_balance(bfx)
                        if current_margin_balance > 0.0001: 
                            # 当前买一价
                            price = bfx2.fetch_ticker(symbol).get('bid') * 0.98
                            # 卖出数量
                            amount = current_margin_balance * leverage / price
                            order_info = place_bfx_order(bfx, symbol, 'limit', 'sell', amount, price , {'type': 'limit'})
                            msg = '开多头，下单成功！\n买入品种：%s\n买入价格：%s\n买入数量：%s' % (symbol, price, amount)
                            wechat.send_message('ZhangShiChao', msg)
                            log.info(msg)
                            email_content += msg
                            # 检查仓位，确认是否已买入平仓
                            current_position = ç(bfx2, symbol)
                            if current_position:
                                pos_status = current_position.get('status')
                                pos_amount = current_position.get('amount')
                                pos_side = current_position.get('side')
                                pos_base_price = current_position.get('base_price')
                                pos_leverage = current_position.get('leverage')
                                if (pos_status == 'AVTIVE') & (pos_amount == amount):
                                    msg = '开多成功！当前持仓：\n持仓状态：%s\n持仓方向：%s\n持仓数量：%s\n进入价格:%s\n持仓杠杆：%s' % (pos_status, pos_side, pos_amount, pos_base_price, pos_leverage)
                                    print(msg)
                                    wechat.send_message('ZhangShiChao', msg)
                                    log.info(msg)
                                    email_content += msg
                                    # 记录本次仓位信息
                                    last_position['side'] = 'long'
                                    last_position['status'] = pos_status
                                    last_position['amount'] = pos_amount
                                    last_position['base_price'] = pos_base_price
                                    last_position['leverage'] = pos_leverage
                                else:
                                    msg = '已下单，未交易！'
                                    wechat.send_message('ZhangShiChao', msg)
                                    log.info(msg)
                        break
                    else:
                        msg = '已下单，未交易！继续检查仓位并开空！'
                        wechat.send_message('ZhangShiChao', msg)
                        log.info(msg)
                        sleep(2)
                        continue

    # =====发送邮件
    # 每个半小时发送邮件
    if run_time.minute % 30 == 0:
        # 发送邮件
        auto_send_email('2151680@qq.com', email_title, email_content)

    # =====本次交易结束
    print(email_title)
    print(email_content)
    print('=====本次运行完毕\n')
    sleep(6 * 1)
