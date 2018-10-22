#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-22 11:24:55
# @Author  : mishchael (mishchael@gmail.com)

import sys
sys.path.append(r'F:\crypto_quant\program')
import os
import json
from trade.Trade import *

last_position = {}
last_position['side'] = 'long'
last_position['status'] = 'buy'
last_position['amount'] = 8.5
last_position['base_price'] = 0.00085352
last_position['leverage'] = 3


# =====交易品种=====
symbol = 'EOS/BTC'  # 交易品种
base_coin = symbol.split('/')[-1]
trade_coin = symbol.split('/')[0]
# =====日志初始化=====
log_name = 'Script_Bolling_Stop_' + trade_coin + '_' + base_coin
# =====记录上次交易仓位的json文件位置====
last_position_file = '../logs/trade/' + log_name + '_last.json'
update_last_position(file_path = last_position_file, pos_dict = last_position)