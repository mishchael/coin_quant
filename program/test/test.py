#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-14 14:39:59
# @Author  : Michael (mishchael@gmail.com)

import sys
# sys.path.append('/Users/michael/crypto_quant/program')
sys.path.append('/home/ubuntu/program')
sys.path.append(r'F:\crypto_quant')
import pandas as pd
import ccxt
from datetime import datetime, timedelta
import time
from program.OriginApi.bitfinex2 import Bitfinex2


pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)


# proxies = {
# 	'http': 'socks5://127.0.0.1:1080',
# 	'https': 'socks5://127.0.0.1:1080'
# }
# proxies = {
#     'http': 'http://127.0.0.1:1080',
#     'https': 'https://127.0.0.1:1080'
# }
# bfx = ccxt.bitfinex2()
# bfx.apiKey = 'TaEb52N8Z8wBavUUq0VjxhKa6IclO9NfopbGuTUVz51'
# bfx.secret = 'xVCgYxqqwKVQ3QVm9KNuILsY1by37bcE3EhT8YZZiv6'
# bfx.proxies = proxies
# bfx.userAgent = bfx.userAgents.get('chrome')
# bfx.enableRateLimit = True

# bfx_v1 = ccxt.bitfinex()
# bfx_v1.apiKey = 'TaEb52N8Z8wBavUUq0VjxhKa6IclO9NfopbGuTUVz51'
# bfx_v1.secret = 'xVCgYxqqwKVQ3QVm9KNuILsY1by37bcE3EhT8YZZiv6'
# bfx_v1.proxies = proxies
# bfx_v1.userAgent = bfx.userAgents.get('chrome')
# bfx_v1.enableRateLimit = True

# okex = ccxt.okex()
# okex.apiKey = 'c50ec8cc-965d-4aa8-84dc-88a4834ddfb6'
# okex.secret = '5BFE032BA7885B629B1695A65C3C2FB8'
# okex.proxies = proxies
# okex.userAgent = okex.userAgents.get('chrome')
# okex.enableRateLimit = True

# balance = bfx_v1.fetch_balance()
# print(balance)

# content = bfx.fetch_ohlcv(symbol = 'EOS/BTC', timeframe = '15m', limit = 999)
# df = pd.DataFrame(content, dtype = float)
# df.rename(columns = {0: 'MTS', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace = True)
# df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit = 'ms')
# df['candle_begin_time_GMT8'] = df['candle_begin_time'] + timedelta(hours = 8)
# print(df)

# content = okex.fetch_ohlcv(symbol = 'EOS/USD', timeframe = '1m', since = 0)
# df = pd.DataFrame(content, dtype = float)
# df.rename(columns = {0: 'MTS', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace = True)
# df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit = 'ms')
# df['candle_begin_time_GMT8'] = df['candle_begin_time'] + timedelta(hours = 8)
# print(df)
# bfx.markets['EOS/BTC']['precision'] = {'price': 8, 'amount': 8}
# bfx.load_markets()
# symbol_market = bfx.symbols
# print(symbol_market)



# has= bfx_v1.has
# print(has)
# position = bfx.fetch_orders(symbol = 'EOS/BTC')
# position = bfx_v1.fetch_my_trades()
# print(position)
api_key = 'TaEb52N8Z8wBavUUq0VjxhKa6IclO9NfopbGuTUVz51'
api_secret = 'xVCgYxqqwKVQ3QVm9KNuILsY1by37bcE3EhT8YZZiv6'
bfx = Bitfinex2()
bfx.api_key = api_key
bfx.api_secret = api_secret
# balance=bfx.get_wallets()
# print(balance)

# tickers = bfx.get_tickers(['EOS/BTC', 'ETH/BTC'])
# print(tickers)

# symbol = bfx.parse_symbol_bfx2std('tEOSBTC')
symbol = bfx.parse_symbols_bfx2std('tETHBTC,tEOSBTC')
# symbol = bfx.parse_symbols_bfx2std('tEOSBTC')
print(symbol)