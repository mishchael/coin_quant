#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-17 23:15:07
# @Author  : Michael (mishchael@gmail.com)

import logging

class Logger(object):
	"""docstring for Logger"""
	logger = None
	def __init__(self, name, path, level = logging.INFO, formatter = '%(asctime)s %(levelname)-8s: %(message)s'):
		super(Logger, self).__init__()
		self.logger = logging.getLogger(name)
		# 指定logger输出格式
		formatter = logging.Formatter(formatter)
		# 文件日志
		file_handler = logging.FileHandler(filename = path, mode = 'a', encoding = 'utf-8')
		file_handler.setFormatter(formatter)
		# 为logger添加的日志处理器
		self.logger.addHandler(file_handler)
		# 指定日志的最低输出级别，默认为WARN级别
		self.logger.setLevel(level)


	def debug(self, msg):
		self.logger.debug(msg)

	def info(self, msg):
		self.logger.info(msg)

	def warn(self, msg):
		self.logger.warn(msg)

	def error(self, msg):
		self.logger.error(msg)

	def fatal(self, msg):
		self.logger.fatal(msg)

	def critical(self, msg):
		self.logger.critical(msg)

		
		
		


