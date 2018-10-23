#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-14 00:42:23
# @Author  : Michael (mishchael@gmail.com)

import sys
sys.path.append(r'F:\crypto_quant\program')
# sys.path.append('/Users/michael/crypto_quant/program')

import pandas as pd
import numpy as np
from strategy.Functions import transfer_to_period_data, transfer_utc_to_gmt8
from strategy.Signals import signal_bolling, signal_bolling_with_stop_lose
from strategy.Evaluate import equity_curve_with_long_and_short
import warnings
warnings.simplefilter(action = 'ignore', category = FutureWarning)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 1000)

# ===交易品种===
symbol = 'EOS/USDT'
base_coin = symbol.split('/')[-1]
trade_coin = symbol.split('/')[0]

# ===寻找最优参数===
# 导入数据
# all_data = pd.read_hdf('../data/class8/eth_1min_data.h5', key = 'all_data')
all_data = pd.read_csv('../data/BITFINEX_EOS_USDT_1MIN.csv')
all_data = transfer_utc_to_gmt8(all_data)
# all_data['candle_begin_time'] = pd.to_datetime(all_data['date']) + pd.Timedelta(hours = 8)
# all_data = all_data[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]

# #转换周期数据
# rule_type = '15T'
# all_data = transfer_to_period_data(all_data, rule_type)
# #读取时间段
# all_data = all_data[all_data['candle_begin_time'] >= pd.to_datetime('2018-06-01')]
# all_data.reset_index(inplace = True, drop = True)

# all_data = all_data[all_data['candle_begin_time'] <= pd.to_datetime('2018-07-01')]
# all_data = all_data[all_data['candle_begin_time'] >= pd.to_datetime('2018-05-01')]

# ===数据集划分===
# 回测数据集，70%
df_test = all_data[all_data['candle_begin_time'] <= pd.to_datetime('2018-06-01')]
df_test = all_data[all_data['candle_begin_time'] >= pd.to_datetime('2016-01-01')]
# df_test = all_data[all_data['candle_begin_time'] <= pd.to_datetime('2018-06-01')]
# df_test = all_data[all_data['candle_begin_time'] >= pd.to_datetime('2018-05-01')]
# 验证数据集，30%
df_verify = all_data[all_data['candle_begin_time'] <= pd.to_datetime('2018-10-22')]
df_verify = all_data[all_data['candle_begin_time'] > pd.to_datetime('2018-06-01')]
# df_verify = all_data[all_data['candle_begin_time'] <= pd.to_datetime('2018-07-01')]
# df_verify = all_data[all_data['candle_begin_time'] > pd.to_datetime('2018-06-01')]


# 构建参数候选组合
# boll n
n_list = range(20, 50, 10)
# boll m
# m_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
m_list = [round(x, 1) for x in np.arange(0.5, 2 ,0.5)]
# K线时间周期
# rule_type_list = ['5T', '10T', '15T', '20T', '25T', '30T']
rule_type_list = [str(x) + 'T' for x in range(5, 20, 5)]
# 止损百分比
stop_pct_list = [round(x, 1) for x in np.arange(2, 2.5 , 0.5)]
# 编列所有参数组合
rtn = pd.DataFrame()

# 全部回测收益
for rule_type in rule_type_list:
	#转换周期数据
	all_data = transfer_to_period_data(all_data, rule_type)
	#读取时间段
	# all_data = all_data[all_data['candle_begin_time'] >= pd.to_datetime('2018-07-01')]
	# all_data = all_data[all_data['candle_begin_time'] <= pd.to_datetime('2018-10-22')]
	all_data.reset_index(inplace = True, drop = True)

	for n in n_list:
		for m in m_list:
			for stop in stop_pct_list:
				para = [n, m, stop]

				# 计算交易信号
				# df = signal_bolling(all_data.copy(), para)
				df = signal_bolling_with_stop_lose(all_data.copy(), para)

				#计算资金曲线
				df, is_blow_up = equity_curve_with_long_and_short(df, leverage_rate = 3, c_rate = 2.0/1000)

				print(str([rule_type] + para), '策略全部回测最终收益:', df.iloc[-1]['equity_curve'])

				#存储数据
				rtn.loc[str([rule_type] + para), '全部回测爆仓'] = is_blow_up
				rtn.loc[str([rule_type] + para), '全部回测收益'] = df.iloc[-1]['equity_curve']

# 70%回测收益
for rule_type in rule_type_list:
	#转换周期数据
	df_test = transfer_to_period_data(df_test, rule_type)
	#读取时间段
	# all_data = all_data[all_data['candle_begin_time'] >= pd.to_datetime('2018-07-01')]
	# all_data = all_data[all_data['candle_begin_time'] <= pd.to_datetime('2018-10-22')]
	df_test.reset_index(inplace = True, drop = True)

	for n in n_list:
		for m in m_list:
			for stop in stop_pct_list:
				para = [n, m, stop]

				# 计算交易信号
				# df = signal_bolling(all_data.copy(), para)
				df = signal_bolling_with_stop_lose(df_test.copy(), para)

				#计算资金曲线
				df, is_blow_up = equity_curve_with_long_and_short(df, leverage_rate = 3, c_rate = 2.0/1000)

				print(str([rule_type] + para), '策略70%回测最终收益:', df.iloc[-1]['equity_curve'])

				#存储数据
				rtn.loc[str([rule_type] + para), '70回测爆仓'] = is_blow_up
				rtn.loc[str([rule_type] + para), '70回测收益'] = df.iloc[-1]['equity_curve']

# 30%验证收益
for rule_type in rule_type_list:
	#转换周期数据
	df_verify = transfer_to_period_data(df_verify, rule_type)
	#读取时间段
	# all_data = all_data[all_data['candle_begin_time'] >= pd.to_datetime('2018-07-01')]
	# all_data = all_data[all_data['candle_begin_time'] <= pd.to_datetime('2018-10-22')]
	df_verify.reset_index(inplace = True, drop = True)

	for n in n_list:
		for m in m_list:
			for stop in stop_pct_list:
				para = [n, m, stop]

				# 计算交易信号
				# df = signal_bolling(all_data.copy(), para)
				df = signal_bolling_with_stop_lose(df_verify.copy(), para)

				#计算资金曲线
				df, is_blow_up = equity_curve_with_long_and_short(df, leverage_rate = 3, c_rate = 2.0/1000)

				print(str([rule_type] + para), '策略30%验证最终收益:', df.iloc[-1]['equity_curve'])

				#存储数据
				rtn.loc[str([rule_type] + para), '30验证爆仓'] = is_blow_up
				rtn.loc[str([rule_type] + para), '30验证收益'] = df.iloc[-1]['equity_curve']


rtn.sort_values(by = ['全部回测收益', '70回测收益', '30验证收益'], ascending = False, inplace = True)
rtn.reset_index(inplace = True)
file_path = 'logs/' + trade_coin + '_' + base_coin + '.csv'
rtn.to_csv(file_path, mode = 'w')
print(rtn)












