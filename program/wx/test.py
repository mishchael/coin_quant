#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-16 22:03:13
# @Author  : Michael (mishchael@gmail.com)


import sys
# sys.path.append('/home/ubuntu/program')
sys.path.append('/Users/michael/crypto_quant/program')
# sys.path.append('/Library/Python/2.7/site-packages')

import os
import subprocess
import numpy as np
import pandas as pd
import ccxt
import time
import signal
from com.logger import Logger
from common import *



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
bfx.proxies = proxies
bfx_v1 = ccxt.bitfinex()
bfx_v1.apiKey = apiKey
bfx_v1.secret = secret
bfx_v1.proxies = proxies

okex = ccxt.okex()
okex.apiKey = ''
okex.secret = ''
okex.proxies = proxies
okex.userAgent = okex.userAgents.get('chrome')
okex.enableRateLimit = True


def strategy_start(name):
	child = subprocess.Popen(["pgrep","-f",name],stdout=subprocess.PIPE,shell=False)
	pid = child.communicate()[0].decode('utf-8')
	if pid:
		wechat.send_message('ZhangShiChao', '已有一个策略在运行，pid：%s，请检查！' % pid)
		log.info('已有一个策略在运行，pid：%s，请检查！' % pid)
		return None
	else:
		start_script_path = '/Users/michael/crypto_quant/program/test/test.py'
		start_cmd = 'python ' + start_script_path
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
		print(rtn)
	    # sys.exit(1)
		return rtn
	  
	result=os.system("kill -9 "+pid)
	if result==0:
		rtn = '策略%s已成功终止！' % name
		print(rtn)
		return rtn
	# else:
	#     sys.exit(1)


if __name__ == '__main__':
	proc = strategy_start('script_detect')
	# time.sleep(301)
	# strategy_stop('script_detect')
	# strategy_stop('run')

	
