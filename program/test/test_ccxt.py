#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-20 10:10:53
# @Author  : Michael (mishchael@gmail.com)

import sys
sys.path.append('/Users/michael/crypto_quant/program')
# sys.path.append('/home/ubuntu/program')
# sys.path.append(r'F:\crypto_quant')
import pandas as pd
import ccxt
from datetime import datetime, timedelta
import time
from OriginApi.bitfinex2 import Bitfinex2API
from trade.Trade import *


pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)


proxies = {
	'http': 'socks5://127.0.0.1:1080',
	'https': 'socks5://127.0.0.1:1080'
}
apiKey = ''  # 此处加上自己的apikey和secret，都需要开通交易权限
secret = ''

bfx2 = ccxt.bitfinex2()
bfx2.apiKey = apiKey
bfx2.secret = secret
bfx2.proxies = proxies
bfx2.userAgent = bfx2.userAgents.get('chrome')
bfx2.enableRateLimit = True

bfx = ccxt.bitfinex()
bfx.apiKey = apiKey
bfx.secret = secret
bfx.proxies = proxies
bfx.userAgent = bfx.userAgents.get('chrome')
bfx.enableRateLimit = True

okex = ccxt.okex()
okex.apiKey = 'c50ec8cc-965d-4aa8-84dc-88a4834ddfb6'
okex.secret = '5BFE032BA7885B629B1695A65C3C2FB8'
okex.proxies = proxies
okex.userAgent = okex.userAgents.get('chrome')
okex.enableRateLimit = True

symbol = 'EOS/BTC'
# all_methods = dir(bfx)
# print(all_methods)

# print(dir(bfx))

# ===获取仓位positions===
# positons = bfx.private_post_auth_r_positions()
# print(positons)

# ===获取账户余额===
# balance = bfx.fetch_balance()
# print(balance)

# ===获取全部symbol的24小时行情===
# tickers = bfx.fetch_tickers()
# print(tickers)

# ===获取某个symbol的24小时行情===
# ticker = bfx.fetch_ticker(symbol)
# print(ticker)

# ===获取交易信息===
# trades = bfx.fetch_trades(symbol)
# print(trades)

# ===获取order book ===
# order_book = bfx.fetch_order_book(symbol)
# print(order_book)

# ===获取symbol的stat===
# stat = bfx.public_get_stats1_key_size_symbol_long_hist({'key': 'pos.size', 'size': '1m', 'symbol': 'fUSD'})
# print(stat)

# ===获取K线数据===
# candle = bfx.fetch_ohlcv(symbol)
# print(candle)

# ===获取open orders===
# open_orders = bfx.fetch_open_orders()
# print(open_orders)


balance1 = bfx.fetch_balance()
# balance2 = bfx.fetch_balance(params = {'type': 'trading'})
print(balance1)
# print(balance2.get('free').get('BTC'))

# ticker = bfx2.fetch_ticker(symbol)
# print(ticker)

# order_info = place_bfx_limit_order(bfx,symbol,'buy',10,0.00000001, {'type': 'limit'})
# order_info = place_bfx_order(bfx, symbol ,'limit' ,'buy', 10, 0.00000001, {'type': 'limit'})

# pos = check_bfx_margin_positions(bfx2, symbol)
# print(pos)

# df = get_bfx_candle_data(bfx2, symbol, '1m')
# print(df)

dict(abc)
for k,v in abc.items():
	pass

