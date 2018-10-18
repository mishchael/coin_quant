#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-13 14:33:09
# @Author  : Michael (mishchael@gmail.com)

import pandas as pd
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)

# =====布林线策略=====
# 简单布林线策略
def signal_bolling(df, para = [100,2]):
	"""
	布林线中轨：n天收盘价的移动平均线
    布林线上轨：n天收盘价的移动平均线 + m * n天收盘价的标准差
    布林线上轨：n天收盘价的移动平均线 - m * n天收盘价的标准差
    当收盘价由下向上穿过上轨的时候，做多；然后由上向下穿过下轨的时候，平仓。
    当收盘价由上向下穿过下轨的时候，做空；然后由下向上穿过上轨的时候，平仓。
    :param df:  原始数据
    :param para:  参数，[n, m]
    :return:
	"""

	# ===计算指标===
	n = para[0]
	m = para[1]

	# 计算均线
	df['median'] = df['close'].rolling(n, min_periods = 1).mean()

	# 计算上轨、下跪
	df['std'] = df['close'].rolling(n, min_periods = 1).std(ddof = 0)
	df['upper'] = df['median'] + m * df['std']
	df['lower'] = df['median'] - m * df['std']

	# ===找出做多信号===
	condition1 = df['close'] > df['upper']
	condition2 = df['close'].shift(1) <= df['upper'].shift(1)
	df.loc[condition1 & condition2, 'signal_long'] = 1

	# ===找出做多平仓信号===
	condition1 = df['close'] < df['median']
	condition2 = df['close'].shift(1) >= df['median'].shift(1)
	df.loc[condition1 & condition2, 'signal_long'] = 0

	# ===找出做空心血号===
	condition1 = df['close'] < df['lower']
	condition2 = df['close'].shift(1) >= df['lower'].shift(1)
	df.loc[condition1 & condition2, 'signal_short'] = -1

	# ===找出做空平仓信号===
	condition1 = df['close'] > df['median']
	condition2 = df['close'].shift(-1) <= df['median'].shift(-1)
	df.loc[condition1 & condition2, 'signal_short'] = 0

	# ===合并做多做空信号，去除重复信号===
	df['signal'] = df[['signal_long', 'signal_short']].sum(axis = 1, min_count = 1, skipna = True)
	temp = df[df['signal'].notnull()][['signal']]
	temp = temp[temp['signal'] != temp['signal'].shift(1)]
	df['signal'] = temp['signal']
	df.drop(['median', 'std', 'upper', 'lower', 'signal_long', 'signal_short'], axis = 1, inplace = True)

	# ===由signal计算出实际的每天持有仓位===
	df['pos'] = df['signal'].shift(1)
	df['pos'].fillna(method = 'ffill', inplace = True)
	df['pos'].fillna(value = 0, inplace = True)

	return df

# ===移动平均线策略===
# 简单移动均线策略
def signal_moving_average(df, para = [5, 60]):
	"""
	简单的移动平均线策略
    当短期均线由下向上穿过长期均线的时候，买入；然后由上向下穿过的时候，卖出。
    :param df:  原始数据
    :param para:  参数，[ma_short, ma_long]
    :return:
	"""

	# ===计算指标===
	ma_short = para[0]
	ma_long = para[1]

	# 计算均线
	df['ma_short'] = df['close'].roling(ma_short, min_period = 1).mean()
	df['ma_long'] = df['close'].rolling(ma_long, min_period = 1).mean()

	# ===找出买入信号===
	condition1 = df['ma_short'] > df['ma_long']
	condition2 = df['ma_short'].shift(1) <= df['ma_long'].shift(1)
	df.loc[condition1 & condition2, 'signal'] = 1

	# ===找出卖出信号===
	condition1 = df['ma_short'] < df['ma_long']
	condition2 = df['ma_short'].shift(1) >= df['ma_long'].shift(1)
	df.loc[condition1 & condition2, 'signal'] = 0

	df.drop(['ma_short', 'ma_long'], axis = 1, inplace = True)

	# ===由signal计算出实际的每天持有仓位
	# signal的计算运用了收盘价，是每根K线收盘之后产生的信号，到第二根开盘的时候才买入，仓位才会改变。
	f['pos'] = df['signal'].shift()
	df['pos'].fillna(method = 'ffill', inplace = True)
	df['pos'].fillna(value = 0, inplace = True)

	return df














