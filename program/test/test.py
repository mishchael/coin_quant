#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-14 14:39:59
# @Author  : Michael (mishchael@gmail.com)

import pandas as pd
import ccxt
from datetime import datetime, timedelta
import time

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)


proxies = {
	'http': 'socks5://127.0.0.1:1080',
	'https': 'socks5://127.0.0.1:1080'
}
bfx = ccxt.bitfinex2()
bfx.apiKey = 'VIKFh7gMpiJ4XoQoAc0SHTup1AQ3EJjYhdBtfd4mTt9'
bfx.secret = 'ERepLdFjPMXeBSxqkAqrnWAQ1ipVEKG6oFr72owP6Du'
bfx.proxies = proxies
bfx.userAgent = bfx.userAgents.get('chrome')
bfx.enableRateLimit = True

okex = ccxt.okex()
okex.apiKey = 'c50ec8cc-965d-4aa8-84dc-88a4834ddfb6'
okex.secret = '5BFE032BA7885B629B1695A65C3C2FB8'
okex.proxies = proxies
okex.userAgent = okex.userAgents.get('chrome')
okex.enableRateLimit = True

total_amount = bfx.fetch_balance()
print(total_amount)

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




