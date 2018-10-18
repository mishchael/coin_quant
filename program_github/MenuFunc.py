#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-16 22:03:13
# @Author  : Michael (mishchael@gmail.com)
import sys
# sys.path.append('/Users/michael/crypto_quant/program')
sys.path.append('/home/ubuntu/program')
import os
import subprocess
import numpy as np
import pandas as pd
import ccxt
import signal
from com.logger import Logger
from common import *

log_name = 'wechat_bfx'
log_path = '../logs/' + log_name + '.log'
log = Logger(name = log_name, path = log_path)

wechat = Send_Message()
# os.system('python ../program/test/test.py')
# os.popen("python ../program/test/test.py") 
# os.popen("kill -9 $(ps -aux|grep test.py|awk '{print $2}')")

proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}
apiKey = ''  # 此处加上自己的apikey和secret，都需要开通交易权限
secret = ''
bfx = ccxt.bitfinex2()  # 创建交易所，此处为okex交易所
bfx.apiKey = apiKey
bfx.secret = secret
# bfx.proxies = proxies
bfx_v1 = ccxt.bitfinex()
bfx_v1.apiKey = apiKey
bfx_v1.secret = secret
# bfx_v1.proxies = proxies







# 获取bfx的账户余额
def get_bfx_balance():
	balance = bfx.fetch_balance()
	balance_exchange_total = balance['total']
	balance_exchange_free = balance['free']
	balance_exchange_used = balance['used']

	balance_margin_total = balance['info'][0][2]

	rtn_balance = 'Exchange账户\n账户余额：%s\n可用余额：%s\n已用余额：%s\n\nMargin账户\n账户余额：%s BTC' % (balance_exchange_total, balance_exchange_free, balance_exchange_used, balance_margin_total)
	return rtn_balance

# 查询bfx持仓
def get_bfx_position():
	pass

# 获取bfx运行参数
def get_bfx_run_param(strategy, symbol):
	pass

# 获取脚本执行日志
def get_bfx_run_log():
	pass

# 获取交易记录
def get_order_info():
	pass

# 获取参数调优结果
def get_optimal_param():
	pass

# 修改策略参数
def strategy_param_modify():
	pass

# 启动策略
def strategy_start(name):
	child = subprocess.Popen(["pgrep","-f",name],stdout=subprocess.PIPE,shell=False)
	pid = child.communicate()[0].decode('utf-8')
	if pid:
		wechat.send_message('ZhangShiChao', '已有一个策略在运行，pid：%s，请检查！' % pid)
		log.info('已有一个策略在运行，pid：%s，请检查！' % pid)
		return None
	else:
		start_script_path = '../trade/script_detect.py'
		
		# start_cmd = 'python ' + start_script_path
		start_cmd = 'python ' + start_script_path
		proc = subprocess.Popen(start_cmd, stdout=subprocess.PIPE, shell=True)
		pid = proc.pid
	# print(proc.communicate())
		return pid

# 停止策略
def strategy_stop(name, max_try = 5):
	# rtn = False
	# while True:
	# 	status = subprocess.Popen.poll(proc)
	# 	if status == 0:
	# 		rtn = True
	# 		break
	# 	elif status == None:
	# 		if max_try > 0:
	# 			try:
	# 				proc.kill()
	# 				max_try -= 1
	# 			except Exception as e:
	# 				print(e)
	# 			else:
	# 				# os.killpg(proc.pid, signal.SIGTERM)
	# 				os.killpg(os.getpgid(proc.pid), 9)

	# return rtn

	# kill_script_detect = '''sudo kill -9 `ps -ef|grep run|awk '{print $2}'`'''
	# kill_run = '''sudo kill -9 `ps -ef|grep run|awk '{print $2}'`'''
	# os.system(kill_script_detect)
	# os.system(kill_run)
	child = subprocess.Popen(["pgrep","-f",name],stdout=subprocess.PIPE,shell=False)
	pid = child.communicate()[0].decode('utf-8')
	
	rtn = ''
	if not pid:
		rtn = '策略%s未运行，请检查！' % name
		# print(rtn)
	 	# sys.exit(1)
		return rtn
		
	result=os.system("kill -9 "+pid)
	if result==0:
		rtn = '策略%s已成功终止！' % name
		return rtn
	# else:
	#     sys.exit(1)