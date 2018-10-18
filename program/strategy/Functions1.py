#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-13 14:33:49
# @Author  : Michael (mishchael@gmail.com)

import pandas as pd
pd.set_option('expand_frame_repr', False)
# pd.set_option('diaplay.max_rows', 1000)

def transfer_to_period_data(df, rule_type = '15T'):
	"""
	将数据转换为其它周期的数据
	:param df:
	:param rule_type:
	:return:
	"""

	# ===转换为其它分钟数据
	period_df = df.resample(rule = rule_type, on = 'candle_begin_time', label = 'left', closed = 'left').agg(
		{
			'open': 'first',
			'high': 'max',
			'low': 'min',
			'close': 'last',
			'volume': 'sum'
		})

	period_df.dropna(subset = ['open'], inplace = True)
	period_df = period_df[period_df['volume'] > 0]
	period_df.reset_index(inplace = True)
	df = period_df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]

	return df
