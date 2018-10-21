#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-21 10:46:27
# @Author  : Michael (mishchael@gmail.com)
import sys
sys.path.append('/Users/michael/crypto_quant/program')
# sys.path.append('/home/ubuntu/program')
# sys.path.append(r'F:\crypto_quant')
import pandas as pd
from datetime import datetime, timedelta
import time
from OriginApi.bitfinex2 import Bitfinex2API


def parse_positions(response):
		"""
		获取持仓仓位
		:return:
		{
			'EOS/BTC': 
				{
					'symbol': 'EOS/BTC', 
					'status': 'ACTIVE',   //(ACTIVE, CLOSED).
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
		if response:
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
