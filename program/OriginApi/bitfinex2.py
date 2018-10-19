#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-19 13:53:43
# @Author  : mishchael (mishchael@gmail.com)


import os
import requests
import time
import json
import hashlib
import hmac



proxies = {
    'http': 'http://127.0.0.1:1080',
    'https': 'https://127.0.0.1:1080'
}
userAgents = {
        'chrome': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'chrome39': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }

headers = {
	'User-Agent': userAgents['chrome']
}

class Bitfinex2(object):
	"""docstring for bitfinex"""
	BASE_URL = "https://api.bitfinex.com/"
	def __init__(self, proxies = None, user_agent = None, api_key = None, api_secret = None):
		
		userAgents = {
				'chrome': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
				'chrome39': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
			}
		self.proxies = proxies or {
			'http': 'http://127.0.0.1:1080',
			'https': 'https://127.0.0.1:1080'
		}
		self.user_agent = user_agent or userAgents['chrome']
		self.api_key = api_key
		self.api_secret = api_secret

		
	def nonce(self):
		"""
		Returns a nonce
		Used in authentication
		"""
		return str(int(round(time.time() * 1000)))

	def headers(self, path, nonce, body):

		signature = "/api/" + path + nonce + body
		print("Signing: " + signature)
		h = hmac.new(self.api_secret.encode('utf8'), signature.encode('utf8'), hashlib.sha384)
		signature = h.hexdigest()

		return {
			"User-Agent:": self.user_agent,
			"bfx-nonce": nonce,
			"bfx-apikey": self.api_key,
			"bfx-signature": signature,
			"content-type": "application/json"
		}


	def parse_symbol_bfx2std(self, symbol):
		base_currency = symbol[1:4].upper()
		quote_currency = symbol[4:7].upper()
		symbol_std = base_currency + '/' + quote_currency
		return symbol_std


	def parse_symbol_std2bfx(self, symbol):
		currency_list = symbol.split('/')
		symbol_bfx = 't'
		for currency in currency_list:
			symbol_bfx += currency.upper()
		return symbol_bfx

	def parse_symbols_std2bfx(self, symbols):
		symbols = [self.parse_symbol_std2bfx(symbol) for symbol in symbols]
		symbols_bfx = ','.join(symbols)
		return symbols_bfx
		
	def parse_symbols_bfx2std(self, symbols):
		symbols = symbols.split(',')
		symbols_std = [self.parse_symbol_bfx2std(symbol) for symbol in symbols]
		return symbols_std


	def request_get(self, path):
		url = self.BASE_URL + path
		headers = {
			'User-Agent': self.user_agent
		}
		response = requests.get(url, headers = headers, proxies = self.proxies, timeout = 5)
		return response

	def requet_post(self, path, data = {}):
		nonce = self.nonce()
		rawdata = json.dumps(data)
		headers = self.headers(path, nonce, data)
		url = self.BASE_URL + path
		response = requests.post(url, data = data, headers = headers, proxies = self.proxies, timeout = 5)
		return response.text

	def get_wallets(self):
		url = 'https://api.bitfinex.com/v2/auth/r/wallets'
		response = self.request_get(url).text

	def get_tickers(self, symbols = None):
		if type(symbols) == str:
			if symbols != 'ALL':
				basec_currency = symbols[0:3]
				quote_currency = symbols[4:7]
				symbols = 't' + basec_currency.upper() + quote_currency.upper()
			path = 'v2/tickers?symbols=%s' % symbols
		elif type(symbols) == list:
			symbols_long = ''
			for symbol in symbols:
				basec_currency = symbol[0:3]
				quote_currency = symbol[4:7]
				symbol = 't' + basec_currency.upper() + quote_currency.upper()
				symbols_long = symbols_long + ',' + symbol
			symbols_long = symbols_long.strip(',')
			path = 'v2/tickers?symbols=%s' % symbols_long
		print(path)
		response = self.request_get(path)
		return response.text
