#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date	: 2018-10-20 10:54:12
# @Author  : Michael (mishchael@gmail.com)


import sys
sys.path.append('/Users/michael/crypto_quant/program')
# sys.path.append('/home/ubuntu/program')
# sys.path.append(r'F:\crypto_quant')
import pandas as pd
import ccxt
from datetime import datetime, timedelta
import time
import json
from OriginApi.bitfinex2 import Bitfinex2API

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)


proxies = {
	'http': 'socks5://127.0.0.1:1080',
	'https': 'socks5://127.0.0.1:1080'
}
apiKey = 'WvMYlyML5mjIQ5D0xliGSVzqpLlFNy2Jc1kFt7NasQg'  # 此处加上自己的apikey和secret，都需要开通交易权限
secret = 'IXmu0zGGfNu4AoO1g8IqJYWUko7vwf3ubGo3R4DrQu7'




class Bitfinex(object):
	"""docstring for Bitfinex2"""
	def __init__(self, exchange):
		# super(Bitfinex2, self).__init__()
		self.exchange = exchange
		self.exchange_v1 = ccxt.bitfinex()
		self.exchange_v1.apiKey = self.exchange.apiKey
		self.exchange_v1.secret = self.exchange.secret
		self.exchange_v1.proxies = self.exchange.proxies
		self.exchange_v1.userAgent = self.exchange.userAgent
		self.exchange_v1.enableRateLimit = self.exchange.enableRateLimit
		self.bfx2api = Bitfinex2API()
		self.bfx2api.api_key = self.exchange.apiKey
		self.bfx2api.api_secret = self.exchange.secret
		self.bfx2api.user_agent = self.exchange.userAgent
		self.bfx2api.proxies = self.exchange.proxies

	def describe(self):
		response = self.exchange.describe()
		return response

	def fetch_markets(self):
		response = self.exchange.fetch_markets()
		return response

	def fetch_balance(self):
		"""
		获取账户余额
		:return:{'margin': {'BTC': {'total': 0.021962, 'used': 0, 'free': 0.021962}}, 'exchange': {'BTC': {'total': 0.0006, 'used': 0, 'free': 0.0006}}}
		"""
		response = self.exchange.fetch_balance()
		account_dict = {}
		for balance in response['info']:
			account = balance[0]
			currency = balance[1]
			total = balance[2]
			free = balance[4]
			used = 0
			if not free:
				if free == 0:
					used = total - free
				else:
					free = total
			else:
				used = total - free
			balance_dict = {}
			balance_dict['total'] = total
			balance_dict['used'] = used
			balance_dict['free'] = free
			currency_dict = {}
			currency_dict[currency] = balance_dict
			account_dict[account] = currency_dict

		return account_dict

	def fetch_platform_status(self):
		"""
		:return: 1=operative, 0=maintenance
		"""
		response = self.exchange.public_get_platform_status()
		return response

	def fetch_tickers(self, symbols = None, params = {}):
		"""
		获取全部symbol的24小时行情
		A price ticker contains statistics for a particular market/symbol for some period of time in recent past, usually last 24 hours.
		:symbols: list ['ETH/BTC', 'LTC/BTC']
		:return: 
		{
			'symbol':		string symbol of the market ('BTC/USD', 'ETH/BTC', ...)
			'info':		{ the original non-modified unparsed reply from exchange API },
			'timestamp':	 int (64-bit Unix Timestamp in milliseconds since Epoch 1 Jan 1970)
			'datetime':	  ISO8601 datetime string with milliseconds
			'high':		  float, // highest price
			'low':			float, // lowest price
			'bid':			float, // current best bid (buy) price
			'bidVolume':	 float, // current best bid (buy) amount (may be missing or undefined)
			'ask':			float, // current best ask (sell) price
			'askVolume':	 float, // current best ask (sell) amount (may be missing or undefined)
			'vwap':		  float, // volume weighed average price
			'open':		  float, // opening price
			'close':		 float, // price of last trade (closing price for current period)
			'last':		  float, // same as `close`, duplicated for convenience
			'previousClose': float, // closing price for the previous period
			'change':		float, // absolute change, `last - open`
			'percentage':	float, // relative change, `(change/open) * 100`
			'average':		float, // average price, `(last + open) / 2`
			'baseVolume':	float, // volume of base currency traded for last 24 hours
			'quoteVolume':	float, // volume of quote currency traded for last 24 hours
		}
		"""
		response = self.exchange.fetch_tickers(symbols = symbols, params = params)
		return response

	def fetch_ticker(self, symbol, params = {}):
		"""
		获取某个symbol的24小时行情
		：symbol：
		:return: 
		{
		    'symbol':        string symbol of the market ('BTC/USD', 'ETH/BTC', ...)
		    'info':        { the original non-modified unparsed reply from exchange API },
		    'timestamp':     int (64-bit Unix Timestamp in milliseconds since Epoch 1 Jan 1970)
		    'datetime':      ISO8601 datetime string with milliseconds
		    'high':          float, // highest price
		    'low':           float, // lowest price
		    'bid':           float, // current best bid (buy) price
		    'bidVolume':     float, // current best bid (buy) amount (may be missing or undefined)
		    'ask':           float, // current best ask (sell) price
		    'askVolume':     float, // current best ask (sell) amount (may be missing or undefined)
		    'vwap':          float, // volume weighed average price
		    'open':          float, // opening price
		    'close':         float, // price of last trade (closing price for current period)
		    'last':          float, // same as `close`, duplicated for convenience
		    'previousClose': float, // closing price for the previous period
		    'change':        float, // absolute change, `last - open`
		    'percentage':    float, // relative change, `(change/open) * 100`
		    'average':       float, // average price, `(last + open) / 2`
		    'baseVolume':    float, // volume of base currency traded for last 24 hours
		    'quoteVolume':   float, // volume of quote currency traded for last 24 hours
		}
		"""
		response = self.exchange.fetch_ticker(symbol = symbol, params = params)
		return response

	def fetch_trades(self, symbol, since=None, limit=120, params={}):
		"""
		获取指定symbol的最近交易信息
		get the list of most recent trades for a particular symbol
		:symbol:
		:since: 开始时间(毫秒milliseconds)
		:limit:	最近交易数
		:params:
		:return:
		[
		    {
		        'info':       { ... },                  // the original decoded JSON as is
		        'id':        '12345-67890:09876/54321', // string trade id
		        'timestamp':  1502962946216,            // Unix timestamp in milliseconds
		        'datetime':  '2017-08-17 12:42:48.000', // ISO8601 datetime with milliseconds
		        'symbol':    'ETH/BTC',                 // symbol
		        'order':     '12345-67890:09876/54321', // string order id or undefined/None/null
		        'type':      'limit',                   // order type, 'market', 'limit' or undefined/None/null
		        'side':      'buy',                     // direction of the trade, 'buy' or 'sell'
		        'price':      0.06917684,               // float price in quote currency
		        'amount':     1.5,                      // amount of base currency
		    },
		    ...
		]
		"""
		response = self.exchange.fetch_trades(symbol = symbol, since = since, limit = limit, params = {})
		return response

	def fetch_my_trades(self, symbol=None, since=None, limit=25, params={}):
		response = self.exchange.fetch_my_trades(symbol = symbol, since = since, limit = limit, params = params)
		return response


	def fetch_order_book(self, symbol, limit=None, params={}):
		"""
		获取订单簿（market depth）
		'precision': 'R0'
		The method for fetching an order book for a particular symbol 
		An order book is also often called market depth
		:symbol:
		:limit: 返回depth数量,ccxt代码里没有使用limit参数，即该参数无效
		:params:
		:return:
		{
		    'bids': [
		        [ price, amount ], // [ float, float ]
		        [ price, amount ],
		        ...
		    ],
		    'asks': [
		        [ price, amount ],
		        [ price, amount ],
		        ...
		    ],
		    'timestamp': 1499280391811, // Unix Timestamp in milliseconds (seconds * 1000)
		    'datetime': '2017-07-05T18:47:14.692Z', // ISO8601 datetime string with milliseconds
		}
		"""
		response = self.exchange.fetch_order_book(symbol = symbol, limit = limit, params = params)
		return response

	def public_get_stats1_key_size_symbol_side_section(self, params):
		"""
		Various statistics about the requested pair.
		:params['key']: string Allowed values: "funding.size", "credits.size", "credits.size.sym", "pos.size"
		:params['size']: string Available values: '1m'
		:params['symbol']: string The symbol you want information about.
		:params['side']: string Available values: "long", "short"
		:params['section']: string  Available values: "last", "hist"
		:return:
		[ 
		  MTS,  //int millisecond timestamp
		  VALUE  //float Total amount
		]
		"""
		response = self.exchange.public_get_stats1_key_size_symbol_side_section(params = params)
		return response

	def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=1000, params={}):
		"""
		返回candle,list
		returns a list (a flat array) of OHLCV candles
		:symbol:
		:timeframe: 默认1m，Available values: '1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1d', '1w', '2w', '1M'
		:since: 默认None，返回最近1000根candle
		:limit: 默认1000， 返回最近的candle数量，最大1000
		:params:
		:return:
		[
		    [
		        1504541580000, // UTC timestamp in milliseconds, integer
		        4235.4,        // (O)pen price, float
		        4240.6,        // (H)ighest price, float
		        4230.0,        // (L)owest price, float
		        4230.7,        // (C)losing price, float
		        37.72941911    // (V)olume (in terms of the base currency), float
		    ],
		    ...
		]
		"""
		response = self.exchange.fetch_ohlcv(symbol, timeframe = timeframe, since = since, limit = limit, params = params)
		return response

	def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
		"""
		ccxt bfx_v2不支持，使用bfx_v1
		bfx_v2需使用implicit API: private_post_auth_r_orders_symbol
		获取open/active状态的订单
		Get open/active orders
		:symbol: 
		:since:
		:limit:
		:return:
		{
		    'id':                '12345-67890:09876/54321', // string
		    'datetime':          '2017-08-17 12:42:48.000', // ISO8601 datetime of 'timestamp' with milliseconds
		    'timestamp':          1502962946216, // order placing/opening Unix timestamp in milliseconds
		    'lastTradeTimestamp': 1502962956216, // Unix timestamp of the most recent trade on this order
		    'status':     'open',         // 'open', 'closed', 'canceled'
		    'symbol':     'ETH/BTC',      // symbol
		    'type':       'limit',        // 'market', 'limit'
		    'side':       'buy',          // 'buy', 'sell'
		    'price':       0.06917684,    // float price in quote currency
		    'amount':      1.5,           // ordered amount of base currency
		    'filled':      1.1,           // filled amount of base currency
		    'remaining':   0.4,           // remaining amount to fill
		    'cost':        0.076094524,   // 'filled' * 'price' (filling price used where available)
		    'trades':    [ ... ],         // a list of order trades/executions
		    'fee': {                      // fee info, if available
		        'currency': 'BTC',        // which currency the fee is (usually quote)
		        'cost': 0.0009,           // the fee amount in that currency
		        'rate': 0.002,            // the fee rate (if available)
		    },
		    'info': { ... },              // the original unparsed order structure as is
		}
		"""
		response = self.exchange_v1.fetch_open_orders(symbol = symbol, since = since, limit = limit, params = params)
		return response

	def fetch_open_orders_v2(self, params = {}):
		"""
		bfx_v2需使用implicit API: private_post_auth_r_orders_symbol
		获取open/active状态的订单
		Get open/active orders
		:params['symbol']: 
		:return:
		[
		  [
		    ID, 
		    GID,
		    CID,
		    SYMBOL, 
		    MTS_CREATE, 
		    MTS_UPDATE, 
		    AMOUNT, 
		    AMOUNT_ORIG, 
		    TYPE,
		    TYPE_PREV,
		    _PLACEHOLDER,
		    _PLACEHOLDER,
		    FLAGS,
		    STATUS,
		    _PLACEHOLDER,
		    _PLACEHOLDER,
		    PRICE,
		    PRICE_AVG,
		    PRICE_TRAILING,
		    PRICE_AUX_LIMIT,
		    _PLACEHOLDER,
		    _PLACEHOLDER,
		    _PLACEHOLDER,
		    HIDDEN, 
		    PLACED_ID,
		    ...
		  ],
		  ...
		]
		"""
		response = self.exchange.private_post_auth_r_orders_symbol(params = params)
		return response



	def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
		"""
		ccxt bfx_v2不支持，使用bfx_v1
		获取两周内closed状态的订单
		Get closed orders，Returns the most recent closed or canceled orders up to circa two weeks ago
		:symbol: 
		:since:
		:limit:
		:return:
		{
		    'id':                '12345-67890:09876/54321', // string
		    'datetime':          '2017-08-17 12:42:48.000', // ISO8601 datetime of 'timestamp' with milliseconds
		    'timestamp':          1502962946216, // order placing/opening Unix timestamp in milliseconds
		    'lastTradeTimestamp': 1502962956216, // Unix timestamp of the most recent trade on this order
		    'status':     'open',         // 'open', 'closed', 'canceled'
		    'symbol':     'ETH/BTC',      // symbol
		    'type':       'limit',        // 'market', 'limit'
		    'side':       'buy',          // 'buy', 'sell'
		    'price':       0.06917684,    // float price in quote currency
		    'amount':      1.5,           // ordered amount of base currency
		    'filled':      1.1,           // filled amount of base currency
		    'remaining':   0.4,           // remaining amount to fill
		    'cost':        0.076094524,   // 'filled' * 'price' (filling price used where available)
		    'trades':    [ ... ],         // a list of order trades/executions
		    'fee': {                      // fee info, if available
		        'currency': 'BTC',        // which currency the fee is (usually quote)
		        'cost': 0.0009,           // the fee amount in that currency
		        'rate': 0.002,            // the fee rate (if available)
		    },
		    'info': { ... },              // the original unparsed order structure as is
		}
		"""
		response = self.exchange_v1.fetch_closed_orders(symbol = symbol, since = since, limit = limit, params = params)
		return response

	def fetch_closed_orders_v2(self, params = {'symbol': ''}):
		"""
		获取两周内closed状态的订单
		bfx_v2需使用implicit API: private_post_auth_r_orders_symbol_hist
		Get closed orders，Returns the most recent closed or canceled orders up to circa two weeks ago
		:params['symbol']: 'tEOSBTC'
		:return:
		[
		  [
		    ID, 
		    GID,
		    CID,
		    SYMBOL, 
		    MTS_CREATE, 
		    MTS_UPDATE, 
		    AMOUNT, 
		    AMOUNT_ORIG, 
		    TYPE,
		    TYPE_PREV,
		    _PLACEHOLDER,
		    _PLACEHOLDER,
		    FLAGS,
		    STATUS,
		    _PLACEHOLDER,
		    _PLACEHOLDER,
		    PRICE,
		    PRICE_AVG,
		    PRICE_TRAILING,
		    PRICE_AUX_LIMIT,
		    _PLACEHOLDER,
		    _PLACEHOLDER,
		    _PLACEHOLDER,
		    NOTIFY, 
		    HIDDEN, 
		    PLACED_ID,
		    ...
		  ],
		  ...
		]
		"""
		# response = self.exchange.private_post_auth_r_orders_symbol_hist(params = params)
		# return response
		symbol = params.get('symbol')
		if symbol:
			symbol = symbol + '/'
		else:
			symbol = ''
		path = 'v2/auth/r/orders/%shist' % symbol
		response = self.bfx2api.request_post(path)
		if response.status_code == 200:
			response = response.text
		return response


	def fetch_order(self, id, symbol=None, params={}):
		"""
		根据order id获取订单信息
		:id: order id
		:symbol:
		:params:
		:return:
		{
		    'id':                '12345-67890:09876/54321', // string
		    'datetime':          '2017-08-17 12:42:48.000', // ISO8601 datetime of 'timestamp' with milliseconds
		    'timestamp':          1502962946216, // order placing/opening Unix timestamp in milliseconds
		    'lastTradeTimestamp': 1502962956216, // Unix timestamp of the most recent trade on this order
		    'status':     'open',         // 'open', 'closed', 'canceled'
		    'symbol':     'ETH/BTC',      // symbol
		    'type':       'limit',        // 'market', 'limit'
		    'side':       'buy',          // 'buy', 'sell'
		    'price':       0.06917684,    // float price in quote currency
		    'amount':      1.5,           // ordered amount of base currency
		    'filled':      1.1,           // filled amount of base currency
		    'remaining':   0.4,           // remaining amount to fill
		    'cost':        0.076094524,   // 'filled' * 'price' (filling price used where available)
		    'trades':    [ ... ],         // a list of order trades/executions
		    'fee': {                      // fee info, if available
		        'currency': 'BTC',        // which currency the fee is (usually quote)
		        'cost': 0.0009,           // the fee amount in that currency
		        'rate': 0.002,            // the fee rate (if available)
		    },
		    'info': { ... },              // the original unparsed order structure as is
		}
		"""
		response = self.exchange_v1.fetch_order(id = id, symbol = symbol, params = params)
		return response


	def fetch_order_trades_v2(self, params):
		"""
		获取由order产生的trades
		Get Trades generated by an Order
		ccxt bfx_v1和bfx_v2均不支持，需使用implicit API:private_post_auth_r_order_symbol_id_trades
		:params['symbol']: 需与order id配对,即symbol应是order的symbol
		:params['id']: order id
		:return:
		[
		  [
		    ID, 
		    PAIR, 
		    MTS_CREATE, 
		    ORDER_ID, 
		    EXEC_AMOUNT, 
		    EXEC_PRICE, 
		    _PLACEHOLDER, 
		    _PLACEHOLDER, 
		    MAKER,
		    FEE, 
		    FEE_CURRENCY, 
		    ...
		  ],
		  ...
		]
		"""
		response = self.exchange.private_post_auth_r_order_symbol_id_trades(params = params)
		return response


	def fetch_positions(self):
		"""
		获取持仓仓位
		:return:
		{
			'EOS/BTC': 
				{
					'symbol': 'EOS/BTC', 
					'status': 'ACTIVE', 
					'side': 'buy', 
					'amount': 26.68, 
					'base_price': 0.00082458, 
					'margin_funding': -9.1e-07, 
					'margin_funding_type': 'daily', 
					'profit': 0.00023159, 
					'profit_pct': 1.05267409,   
					'liquidation_price': 0.00012678,   //清算价格
					'leverage': 0.9913
				}
		}
		"""
		response = self.exchange.private_post_auth_r_positions()
		response_dict = {}
		for pos in response:
			pos_dict = {}
			symbol = self.bfx2api.parse_symbol_bfx2std(pos[0])
			pos_dict['symbol'] = symbol
			pos_dict['status'] = pos[1]
			if pos[2] > 0:
				pos_dict['side'] = 'buy'
			else:
				pos_dict['side'] = 'sell'
			pos_dict['amount'] = abs(pos[2])
			pos_dict['base_price'] = pos[3]
			pos_dict['margin_funding'] = pos[4]
			if pos[5] == 0:
				pos_dict['margin_funding_type'] = 'daily'
			elif pos[5] == 1:
				pos_dict['margin_funding_type'] = 'term'
			pos_dict['profit'] = pos[6]
			pos_dict['profit_pct'] = pos[7]
			pos_dict['liquidation_price'] = pos[8]
			pos_dict['leverage'] = pos[9]
			response_dict[symbol] = pos_dict

		return response_dict

	def fetch_avail_balance_v2(self, symbol = None, direction = None, rate = None, order_type = None, body = {}):
		"""
		获取可用于某个symbol的可买/可卖数量
		Calculate available balance for order/offer
		implicit API : private_post_auth_calc_order_avail
		:symbol:  std symbol
		:direction: direction of the order/offer (orders: 1 buy, -1 sell | offers: 1 sell, -1 buy)
		:rate: Rate of the order/offer，即买价/卖价
		:order_type: Type of the order/offer EXCHANGE or MARGIN
		:return: 
		{'amount_avail': 88.7437789}  //float Amount available for order/offer
		"""
		# response = self.exchange.private_post_auth_calc_order_avail(body = body)
		# return response

		path = 'v2/auth/calc/order/avail'
		if symbol:
			symbol = self.bfx2api.parse_symbol_std2bfx(symbol)
		body = body or {
			'symbol': symbol,
			'dir': direction,
			'rate': rate,
			'type': order_type.upper()
		}
		response = self.bfx2api.request_post(path, data = body)
		response_dict = {}
		if response.status_code == 200:
			response = response.text
			response_dict = {'amount_avail' : float(response[1:-1])}
		return response_dict

	def create_order(self, symbol, type, side, amount, price=None, params={}):
		"""
		下单
		bfx_v2不支持，使用bfx_v1
		:symbol: a string literal symbol of the market you wish to trade on, like BTC/USD, ZEC/ETH, DOGE/DASH, etc.
		:type: a string literal type of order, market and limit
		:side:  a string literal for the direction of your order, buy or sell.
		:amount: how much of currency you want to trade
		:price: how much quote currency you are willing to pay for a trade lot of base currency (for limit orders only)
		:params: 
		:returns:
		"""
		response = self.exchange_v1.create_order(symbol = symbol, type = type, side = side, amount = amount, price = price, params = params)
		return response

	def cancel_order(self, id, symbol=None, params={}):
		"""
		取消订单
		bfx_v2不支持，使用bfx_v1
		:id: order id
		:symbol:
		:return:
		"""
		response = self.exchange_v1.cancel_order(id = id, symbol = symbol, params = params)
		return response

	def create_limit_order(self, symbol, *args):
		"""
		下限价单
		:symbol: a string literal symbol of the market you wish to trade on, like BTC/USD, ZEC/ETH, DOGE/DASH, etc.
		:side:  a string literal for the direction of your order, buy or sell.
		:amount: how much of currency you want to trade
		:price: how much quote currency you are willing to pay for a trade lot of base currency (for limit orders only)
		:params['type']: Either “market” / “limit” / “stop” / “trailing-stop” / “fill-or-kill” / “exchange market” / “exchange limit” / “exchange stop” / “exchange trailing-stop” / “exchange fill-or-kill”. (type starting by “exchange ” are exchange orders, others are margin trading orders) 
		:returns:
		"""
		response = self.exchange_v1.create_limit_order(symbol, *args)
		return response

	def create_market_order(self, symbol, *args):
		"""
		下市价单
		:symbol: a string literal symbol of the market you wish to trade on, like BTC/USD, ZEC/ETH, DOGE/DASH, etc.
		:side:  a string literal for the direction of your order, buy or sell.
		:amount: how much of currency you want to trade
		:params['type']: Either “market” / “limit” / “stop” / “trailing-stop” / “fill-or-kill” / “exchange market” / “exchange limit” / “exchange stop” / “exchange trailing-stop” / “exchange fill-or-kill”. (type starting by “exchange ” are exchange orders, others are margin trading orders) 
		:returns:
		"""
		response = self.exchange_v1.create_market_order(symbol, *args)
		return response

	def create_limit_buy_order(self, symbol, *args):
		"""
		下限价买单
		:symbol: a string literal symbol of the market you wish to trade on, like BTC/USD, ZEC/ETH, DOGE/DASH, etc.
		:amount: how much of currency you want to trade
		:price: how much quote currency you are willing to pay for a trade lot of base currency (for limit orders only)
		:params['type']: Either “market” / “limit” / “stop” / “trailing-stop” / “fill-or-kill” / “exchange market” / “exchange limit” / “exchange stop” / “exchange trailing-stop” / “exchange fill-or-kill”. (type starting by “exchange ” are exchange orders, others are margin trading orders) 
		:returns:
		"""
		response = self.exchange_v1.create_limit_buy_order(symbol, *args)
		return response

	def create_limit_sell_order(self, symbol, *args):
		"""
		下限价卖单
		:symbol: a string literal symbol of the market you wish to trade on, like BTC/USD, ZEC/ETH, DOGE/DASH, etc.
		:amount: how much of currency you want to trade
		:price: how much quote currency you are willing to pay for a trade lot of base currency (for limit orders only)
		:params['type']: Either “market” / “limit” / “stop” / “trailing-stop” / “fill-or-kill” / “exchange market” / “exchange limit” / “exchange stop” / “exchange trailing-stop” / “exchange fill-or-kill”. (type starting by “exchange ” are exchange orders, others are margin trading orders) 
		:returns:
		"""
		response = self.exchange_v1.create_limit_sell_order(symbol, *args)
		return response

	def create_market_buy_order(self, symbol, amount, params={}):
		"""
		下市价买单
		:symbol: a string literal symbol of the market you wish to trade on, like BTC/USD, ZEC/ETH, DOGE/DASH, etc.
		:side:  a string literal for the direction of your order, buy or sell.
		:amount: how much of currency you want to trade
		:params['type']: Either “market” / “limit” / “stop” / “trailing-stop” / “fill-or-kill” / “exchange market” / “exchange limit” / “exchange stop” / “exchange trailing-stop” / “exchange fill-or-kill”. (type starting by “exchange ” are exchange orders, others are margin trading orders) 
		:returns:
		"""
		response = self.exchange_v1.create_market_buy_order(symbol = symbol, amount = amount, params = params)
		return response


	def create_market_sell_order(self, symbol, amount, params={}):
		"""
		下市价卖单
		:symbol: a string literal symbol of the market you wish to trade on, like BTC/USD, ZEC/ETH, DOGE/DASH, etc.
		:side:  a string literal for the direction of your order, buy or sell.
		:amount: how much of currency you want to trade
		:params['type']: Either “market” / “limit” / “stop” / “trailing-stop” / “fill-or-kill” / “exchange market” / “exchange limit” / “exchange stop” / “exchange trailing-stop” / “exchange fill-or-kill”. (type starting by “exchange ” are exchange orders, others are margin trading orders) 
		:returns:
		"""
		response = self.exchange_v1.create_market_sell_order(symbol = symbol, amount = amount, params = params)
		return response


	def fetch_margin_info_v2(self, params = {}):
		"""
		获取magin信息
		:praams['key']: "base" or symbol like "tEOSBTC"
		:return:
		// margin base
		[
		  "base",
		  [
		    USER_PL, 			//float	User Profit and Loss
		    USER_SWAPS, 		//float	Amount of swaps a user has
		    MARGIN_BALANCE, 	//float	Balance in your margin funding account,USD
		    MARGIN_NET,			//float	Balance after P&L is accounted for,USD
		    ...
		  ]
		]
		// margin symbol
		[
		  "sym",
		  SYMBOL,
		  [
		    TRADABLE_BALANCE,	//float	Your buying power (how large a position you can obtain)
		    GROSS_BALANCE,
		    BUY,
		    SELL,
		    ...
		  ]
		]
		"""
		response = self.exchange.private_post_auth_r_info_margin_key(params = params)
		return response


	def fetch_margin_info_v1(self):
		
		response = self.exchange_v1.private_post_margin_infos()
		return response
















