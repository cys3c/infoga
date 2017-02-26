#!/usr/bin/env python 
# -*- coding:utf-8 -*- 
# infoga - Gathering Email Information Tool
# Coded by M0M0 (m4ll0k)

import httplib
import re
import string 
import sys
from lib import color
from lib import parser


class bing_search:
	
	""" Bing Search Engine"""

	def __init__(self, keyword):
		self.keyword = keyword 
		self.results = ""
		self.tresult = ""
		self.server = "www.bing.com"
		self.host = "www.bing.com"
		self.u_agent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
		self.t  = color.incolor.RESET  
		self.r  = color.incolor.RED
		self.y = color.incolor.YELLOW

	def run_search(self):
		try:
			con = httplib.HTTP(self.server)
			con.putrequest('GET', '/search?q=%40'+self.keyword)
			con.putheader('Host', self.host)
			con.putheader('Cookie', 'SRCHHPGUSR=ADLT=DEMOTE&NRSLT=50')
			con.putheader('Accept-Language', 'en-us,en')
			con.putheader('User-agent', self.u_agent)
			con.endheaders()
			# return code,messagge and header
			returncode, returnmsg, header = con.getreply()
			self.results = con.getfile().read()
			self.tresult += self.results
		except Exception as err: 
			print "\t\t|"
			print "\t\t|__"+self.r+" Server not found!!\n"+self.t

	def get_emails(self):
		_findemail = parser.inparser(self.results, self.keyword)
		return _findemail._emails()

	def process(self):
		self.run_search()