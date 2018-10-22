#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-14 14:39:59
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
from trade.Trade import get_bfx_candle_data



pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)


proxies = {
	'http': 'socks5://127.0.0.1:1080',
	'https': 'socks5://127.0.0.1:1080'
}
# proxies = {
#     'http': 'http://127.0.0.1:1080',
#     'https': 'https://127.0.0.1:1080'
# }
bfx = ccxt.bitfinex2()
bfx.apiKey = ''
bfx.secret = ''
bfx.proxies = proxies
bfx.userAgent = bfx.userAgents.get('chrome')
bfx.enableRateLimit = True

# bfx_v1 = ccxt.bitfinex()
# bfx_v1.apiKey = ''
# bfx_v1.secret = ''
# bfx_v1.proxies = proxies
# bfx_v1.userAgent = bfx.userAgents.get('chrome')
# bfx_v1.enableRateLimit = True

# okex = ccxt.okex()
# okex.apiKey = ''
# okex.secret = ''
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
# api_key = 'P1BZKFi5bOBKPl9RIrJfrNR50rLwF6G9jXry4bLbRVQ'
# api_secret = 'TBJY5S7aonIz9JDvHsqk5QxJJtjuey837dHn8TtdSxy'
# bfx = Bitfinex2API()
# bfx.api_key = api_key
# bfx.api_secret = api_secret
# balance=bfx.get_wallets().text
# print(balance)
# positions = bfx.get_positions()
# print(positions.text)
# print(bfx.get_orders().text)

# tickers = bfx.get_tickers(['EOS/BTC', 'ETH/BTC'])
# print(tickers)

# symbol = bfx.parse_symbol_bfx2std('tEOSBTC')
# symbol = bfx.parse_symbols_bfx2std('tETHBTC,tEOSBTC')
# symbol = bfx.parse_symbols_bfx2std('tEOSBTC')
# print(symbol)


candle_data = get_bfx_candle_data(bfx, 'EOS/BTC', '5m')
print(candle_data)







