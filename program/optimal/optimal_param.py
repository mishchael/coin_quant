#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-14 00:42:23
# @Author  : Michael (mishchael@gmail.com)

import sys
sys.path.append('/Users/michael/crypto_quant/program')

import pandas as pd
from strategy.Functions import transfer_to_period_data, transfer_utc_to_gmt8
from strategy.Signals import signal_bolling, signal_bolling_with_stop_lose
from strategy.Evaluate import equity_curve_with_long_and_short
import warnings
warnings.simplefilter(action = 'ignore', category = FutureWarning)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 1000)


# ===寻找最优参数===
# 导入数据
# all_data = pd.read_hdf('../data/class8/eth_1min_data.h5', key = 'all_data')
all_data = pd.read_csv('../data/BITFINEX_EOS_BTC_1MIN.csv')
all_data = transfer_utc_to_gmt8(all_data)
# all_data['candle_begin_time'] = pd.to_datetime(all_data['date']) + pd.Timedelta(hours = 8)
# all_data = all_data[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]

# #转换周期数据
# rule_type = '15T'
# all_data = transfer_to_period_data(all_data, rule_type)
# #读取时间段
# all_data = all_data[all_data['candle_begin_time'] >= pd.to_datetime('2018-06-01')]
# all_data.reset_index(inplace = True, drop = True)

# 构建参数候选组合
n_list = range(20, 500, 10)
m_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
rule_type_list = ['5T', '10T', '15T', '20T', '25T', '30T']

# 编列所有参数组合
rtn = pd.DataFrame()
for rule_type in rule_type_list:
	#转换周期数据
	all_data = transfer_to_period_data(all_data, rule_type)
	#读取时间段
	all_data = all_data[all_data['candle_begin_time'] >= pd.to_datetime('2017-01-01')]
	all_data.reset_index(inplace = True, drop = True)

	for n in n_list:
		for m in m_list:
			para = [n,m]

			# 计算交易信号
			# df = signal_bolling(all_data.copy(), para)
			df = signal_bolling_with_stop_lose(all_data.copy(), para + [5])

			#计算资金曲线
			df, is_blow_up = equity_curve_with_long_and_short(df, leverage_rate = 3, c_rate = 2.0/1000)

			print(str(para) + ',' + rule_type, '策略最终收益:', df.iloc[-1]['equity_curve'])

			#存储数据
			rtn.loc[str(para) + ',' + rule_type + ',' + is_blow_up, '收益'] = df.iloc[-1]['equity_curve']

print(rtn.sort_values(by = '收益', ascending = False))











