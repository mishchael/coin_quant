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
bfx = ccxt.bitfinex()  # 创建交易所，此处为okex交易所
bfx.apiKey = apiKey
bfx.secret = secret
bfx.load_markets()
# bfx.proxies = proxies
bfx2 = ccxt.bitfinex2()
bfx2.apiKey = apiKey
bfx2.secret = secret
bfx2.load_markets()
# bfx2.proxies = proxies



# 策略脚本进程
proc = None

# 获取bfx的账户余额
def get_bfx_balance():
	exchange_balance = bfx.fetch_balance(params = {'type': 'exchange'})
	margin_balance = bfx.fetch_balance(params = {'type': 'trading'})

	exchange_msg = 'Exchange账户\n总余额：'
	for currency, balance in exchange_balance['total'].items():
		msg = str(balance) + ' ' + currency + '\n'
		exchange_msg += msg
	exchange_msg += '可用余额：'
	for currency, balance in exchange_balance['free'].items():
		msg = str(balance) + ' ' + currency + '\n'
		exchange_msg += msg
	exchange_msg += '已用余额：'
	for currency, balance in exchange_balance['used'].items():
		msg = str(balance) + ' ' + currency + '\n'
		exchange_msg += msg

	margin_msg = 'Margin账户\n总余额：'
	for currency, balance in margin_balance['total'].items():
		msg = str(balance) + ' ' + currency + '\n'
		margin_msg += msg
	margin_msg += '可用余额：'
	for currency, balance in margin_balance['free'].items():
		msg = str(balance) + ' ' + currency + '\n'
		margin_msg += msg
	margin_msg += '已用余额：'
	for currency, balance in margin_balance['used'].items():
		msg = str(balance) + ' ' + currency + '\n'
		margin_msg += msg

	return exchange_msg + margin_msg

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

# 检查脚本运行状态
def check_script_status(script_name_list):
	msg_list = []
	for script_name in script_name_list:
		child = subprocess.Popen(["pgrep","-f",script_name],stdout=subprocess.PIPE,shell=False)
		pid = child.communicate()[0].decode('utf-8')
		if pid:
			msg = '脚本%s正在运行，pid：%s' % (script_name, pid)
			msg_list.append(msg)
		else:
			msg = '脚本%s未运行!' % script_name
			msg_list.append(msg)
	return msg_list


# 启动策略
def strategy_start(name):
	child = subprocess.Popen(["pgrep","-f",name],stdout=subprocess.PIPE,shell=False)
	pid = child.communicate()[0].decode('utf-8')
	if pid:
		wechat.send_message('ZhangShiChao', '已有一个策略在运行，pid：%s，请检查！' % pid)
		log.info('已有一个策略在运行，pid：%s，请检查！' % pid)
		return None
	else:
		start_script_path = '/home/ubuntu/program/trade/script_detect.py'
		print(os.getcwd())
		os.chdir('/home/ubuntu/program/trade/')
		print(os.getcwd())
		
		# start_cmd = 'python ' + start_script_path
		start_cmd = 'python bfx_main.py'
		proc = subprocess.Popen(start_cmd, stdout=subprocess.PIPE, shell=False)
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