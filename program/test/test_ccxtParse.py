#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-20 11:28:40
# @Author  : Michael (mishchael@gmail.com)

import sys
sys.path.append('/Users/michael/crypto_quant/program')
# sys.path.append('/home/ubuntu/program')
# sys.path.append(r'F:\crypto_quant')
import pandas as pd
import ccxt
from datetime import datetime, timedelta
import time
from ccxtParser.bitfinex import Bitfinex

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)


proxies = {
	'http': 'socks5://127.0.0.1:1080',
	'https': 'socks5://127.0.0.1:1080'
}
apiKey = ''  # 此处加上自己的apikey和secret，都需要开通交易权限
secret = ''

bfx = ccxt.bitfinex2()
bfx.apiKey = apiKey
bfx.secret = secret
bfx.proxies = proxies
bfx.userAgent = bfx.userAgents.get('chrome')
bfx.enableRateLimit = True

bfx_v1 = ccxt.bitfinex()
bfx_v1.apiKey = apiKey
bfx_v1.secret = secret
bfx_v1.proxies = proxies
bfx_v1.userAgent = bfx.userAgents.get('chrome')
bfx_v1.enableRateLimit = True

bfxp = Bitfinex(bfx)
symbol = 'EOS/BTC'
# ===获取账户余额===
# balance = bfxp.fetch_balance()
# print(balance)

# ===获取平台状态===
# plat_status = bfxp.fetch_platform_status()
# print(plat_status)

# ===获取全部symbol的24小时行情===
# tickers = bfxp.fetch_tickers()
# print(tickers)

# ===获取某个symbol的24小时行情===
# ticker = bfxp.fetch_ticker(symbol)
# print(ticker)

# ===获取指定symbol的最近交易===
# trades = bfxp.fetch_trades(symbol)
# print(trades)

# ===获取order book ===
# order_book = bfx.fetch_order_book(symbol, limit = 20)
# print(order_book)

# ===获取symbol的stat===
# stat = bfxp.public_get_stats1_key_size_symbol_side_section({'key': 'pos.size', 'size': '1m', 'symbol': 'tBTC', 'section': 'long', 'section': 'hist'})
# print(stat)

# ===获取K线数据===
# candle = bfxp.fetch_ohlcv(symbol)
# print(candle)

# ===获取open orders===
# open_orders = bfxp.fetch_open_orders()
# print(open_orders)
# open_orders = bfxp.fetch_open_orders_v2()
# print(open_orders)

# ===获取closed orders===
# closed_orders = bfxp.fetch_closed_orders()
# print(closed_orders)
# closed_orders = bfxp.fetch_closed_orders_v2({'symbol': 'tEOSBTC'})
# closed_orders = bfxp.fetch_closed_orders_v2()
# print(closed_orders)

# ===根据order id获取订单===
# order = bfxp.fetch_order('18206271945')
# print(order)

# ===获取由order 产生的交易===
# trades = bfxp.fetch_order_trades_v2({'symbol': 'tEOSBTC', 'id': '18206271945'})
# print(trades)

# ===获取my trade===
# my_trades = bfxp.fetch_my_trades('EOS/BTC')
# print(my_trades)

# ===获取仓位===
# positions = bfxp.fetch_positions()
# print(positions)

# ===获取可用账户余额===
# body = {
# 	'symbol': 'tEOSUSD',
# 	'dir': 1,
# 	'rate': 5.4875,
# 	'type': 'MARGIN'

# }
# avail_balance = bfxp.fetch_avail_balance_v2(body = body)
# print(avail_balance)


# amount = 30
# price = 0.00000832
# # order = bfxp.create_limit_order('EOS/BTC', 'buy', amount, price, {'type': 'limit'})
# order = bfxp.create_limit_buy_order('EOS/BTC',amount, price, {'type': 'limit'})
# print(order)

# margin_info = bfxp.fetch_margin_info_v2({'key': 'tEOSBTC'})
# margin_info_base = bfxp.fetch_margin_info_v2({'key': 'base'})
# print(margin_info)
# print(margin_info_base)

# margin_info_v1 = bfxp.fetch_margin_info_v1()
# print(margin_info_v1)





body = {
	'symbol': 'tEOSBTC',
	'dir': 1,
	'rate': 0.00083238,
	'type': 'MARGIN'

}
balance = bfxp.fetch_balance()
# avail_balance = bfxp.fetch_avail_balance_v2(body = body)
margin_info = bfxp.fetch_margin_info_v2({'key': 'base'})
# usd_amount = margin_info[1][2]
# print(usd_amount)
# order_book = bfxp.fetch_order_book('BTC/USDT')
# btc_price = order_book['bids'][0][0]
# ticker = bfxp.fetch_ticker('BTC/USDT')
# btc_amount = balance['margin']['BTC']['total']

# btc_price = ticker['last']
# usd_amount = btc_price * btc_amount
# amount = usd_amount * 3.3 / btc_price / 0.00083238
# print('usd_amount:%s' % usd_amount)
# print('btc_price:%s' % btc_price)
# print('amount:%s' % amount)
# print(avail_balance['amount_avail'])
print(margin_info)




