#!/usr/bin/env python 
# -*- coding:utf-8 -*- 
# infoga - Gathering Email Information Tool
# Coded by M0M0 (m4ll0k)


import requests
import re
import string 
import sys 
from lib import color
from lib import parser

class google_search:

	""" Google Search Engine """
	
	def __init__(self, keyword):
		self.keyword = keyword
		self.results = ""
		self.tresult = ""
		self.server = "www.google.com"
		self.u_agent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
		self.r    = color.incolor.RED 
		self.y   = color.incolor.YELLOW
		self.w   = color.incolor.WHITE
		self.t  = color.incolor.RESET 

	def run_search(self):
		try:
			urlfy = "http://" +self.server+ "/search?num=500&start=50&hl=en&meta=&q=%40\"" +self.keyword+ "\""
			try:
				req = requests.get(urlfy)
				self.results = req.content
				self.tresult += self.results
			except Exception as err:
				print "\t\t|"
				print "\t\t|__"+self.r+" Server not found!!\n"+self.t
		except Exception as err:
			print str(err)

	def get_emails(self):
		_findemails = parser.inparser(self.tresult, self.keyword)
		return _findemails._emails()

	def process(self):
		self.run_search()




