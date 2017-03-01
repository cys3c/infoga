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


class pgp_search:

	"""PGP Server Search Engine"""

	def __init__(self, keyword):
		'''pgp server search'''
		self.keyword = keyword
		self.results = ""
		self.tresult = ""
		self.server = "pgp.mit.edu" 
		self.host = "pgp.mit.edu"
		self.u_agent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
		self.t  = color.incolor.RESET
		self.r = color.incolor.RED
		self.y = color.incolor.YELLOW

	def run_search(self):
		try:
			con = httplib.HTTP(self.server)
			con.putrequest('GET', "/pks/lookup?search="+self.keyword+"&op=index")
			con.putheader('Host', self.host)
			con.putheader('User-agent', self.u_agent)
			con.endheaders()
			# return code,message and header
			returncode, returnmsg, header = con.getreply()
			self.results = con.getfile().read()
			self.tresult += self.results
		except Exception as err:
			print "\t\t|"
			print "\t\t|__"+self.r+" Server not found!!\n"+self.t

	def get_emails(self):
		_findemail = parser.inparser(self.tresult, self.keyword)
		return _findemail._emails()

	def process(self):
		self.run_search()