#!/usr/bin/env python 
# -*- coding:utf-8 -*- 
# infoga - Gathering Email Information Tool
# Coded by M0M0 (m4ll0k)

import re 
import string 

class inparser:
	"""Parser Results"""
	def __init__(self, results, keyword):
		self.results = results
		self.keyword = keyword
		self.tempora = []

	def _clear(self):
		self.results = re.sub('<em>','',self.results)
		self.results = re.sub('<b>','',self.results)
		self.results = re.sub('</b>','',self.results)
		self.results = re.sub('</em>','',self.results)
		self.results = re.sub('%2f',' ',self.results)
		self.results = re.sub('%3a',' ',self.results)
		self.results = re.sub('<strong>','',self.results)
		self.results = re.sub('</strong>','',self.results)
		self.results = re.sub('<wbr>','',self.results)
		self.results = re.sub('</wbr>','',self.results)

		for x in ('>', ':', '=', '<', '/', '\\', ';', '&', '%3A', '%3D', '%3C'):
			self.results = string.replace(self.results, x, ' ')

	def _unique(self):
		self.new=[]
		for x in self.tempora:
			if x not in self.new:
				self.new.append(x)
		return self.new

	def _emails(self):
		self._clear()
		_regmail = re.compile('[a-zA-Z0-9.\-_+#~!$&\',;=:]+'+'@'+'[a-zA-Z0-9.-]*'+self.keyword)
		self.tempora = _regmail.findall(self.results)
		_emails = self._unique()
		return _emails
		

