#!/usr/bin/env python
# -*- coding: utf-8 -*-
# infoga - Gathering Email Information Tool
# by M0M0 (m4ll0k) - (c) 2017


__license__ = """
Copyright (c) 2017, {M0M0 (m4ll0k)}
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * Neither the name of EnableSecurity or Trustwave nor the names of its contributors
      may be used to endorse or promote products derived from this software
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.
"""


from lib import color, parser
from recon import *
from lib import info

# simple list colors 
r = color.incolor.RED 
y = color.incolor.YELLOW 
w = color.incolor.WHITE
t = color.incolor.RESET
g = color.incolor.GREEN
b = color.incolor.BLUE
c = color.incolor.CRIMSON
y = color.incolor.CYAN
i = color.incolor.IND
try:
	import sys
	import urllib3
	import os
	import string
	import json 
	import re
	import getopt
	import requests
	import socket
	from urlparse import urlparse
	from time import strftime 
except Exception as err:
	print r+"[!] "+t+w+str(err)+t
	sys.exit(0)

def banner():
	print r+"  ___        ___                     "+t                   
	print r+" |   .-----.'  _.-----.-----.---.-.  "+t
	print r+" |.  |     |   _|  _  |  _  |  _  |  "+t
	print r+" |.  |__|__|__| |_____|___  |___._|  "+t
	print r+" |:  |                |_____|        "+t
	print r+" |::.|"+t+y+" Infoga %s - %s         "% (info.__version__,info.__info__)
	print r+" |:..|"+t+y+" Codename\t- %s         "% (info.__codename__)
	print r+" |...|"+t+y+" Coded by\t- %s         "% (info.__author__)
	print r+" | - |"+i+" https://github.com/m4ll0k/infoga"+t+t
	print r+" `---'                               \n"+t

def usage():
	scr = os.path.basename(sys.argv[0])
	banner()
	print w+"Usage: Infoga -t [target] -s [source]:\n"+t
	print w+"\t-t\tDomain to search or company name"+t
	print w+"\t-s\tData source: all, google, bing, pgp"+t
	print w+"\t-h\tShow this help and exit\n"+t
	print w+"Examples:"+t
	print w+"\t"+scr+" -t site.com -s all"+t
	print w+"\t"+scr+" -t site.com -s [google, bing, pgp]\n"+t


def start(argv):
	if len(sys.argv) < 4:
		usage()
		sys.exit()
	try:
		opts,args = getopt.getopt(argv, "t:s:h:")
	except getopt.GetoptError: 
		usage()
		sys.exit(0)
	for opt,arg in opts:
		if opt == "-t":
			keyword = arg 
		elif opt == "-h":
			usage()
		elif opt == "-s":
			engine = arg
			if engine not in ("all, google, bing, pgp"):
				usage()
				print r+"[!] "+t+w+"Invalid search engine, try with: all, google, bing or pgp\n"+t 
				sys.exit(0) 
			else:
				pass

	o = urlparse(keyword)
	if o[0] in ['http','https', 'www']:
		usage()
		print r+"[!] "+t+w+"Try without: http://, https:// or www.[site]\n"+t
		sys.exit(0)
	else:
		pass
	_allemails = []
	strf = "[%s] "%(strftime('%H:%M:%S'))
	if engine == "google":
		banner()
		print w+strf+t+y+"Searching \""+keyword+"\" in google..."+t 
		_search = googlesearch.google_search(keyword)
		_search.process()
		_allemails = _search.get_emails()

	elif engine == "bing": 
		banner()
		print w+strf+t+y+"Searching \""+keyword+"\" in bing..."+t
		_search = bingsearch.bing_search(keyword)
		_search.process()
		_allemails = _search.get_emails()

	elif engine == "pgp":
		banner()
		print w+strf+t+y+"Searching \""+keyword+"\" in pgp..."+t
		_search = pgpsearch.pgp_search(keyword)
		_search.process()
		_allemails = _search.get_emails()

	elif engine == "all":
		banner()
		print w+strf+t+y+"Searching \""+keyword+"\" in google..."+t
		_search = googlesearch.google_search(keyword)
		_search.process()
		_emails = _search.get_emails()
		_allemails.extend(_emails)
		print w+strf+t+y+"Searching \""+keyword+"\" in bing..."+t
		_search = bingsearch.bing_search(keyword)
		_search.process()
		_emails = _search.get_emails()
		_allemails.extend(_emails)
		_allemails = sorted(set(_allemails))
		print w+strf+t+y+"Searching \""+keyword+"\" in pgp..."+t
		_search = pgpsearch.pgp_search(keyword)
		_search.process()
		_emails = _search.get_emails()
		_allemails.extend(_emails)
		_allemails = sorted(set(_allemails))

	if _allemails == []:
		print "\n"+w+strf+t+r+"Not found emails!!\n"+t
		sys.exit(0)
	else:
		print "\n"+w+strf+t+y+"Email found: \n"+t
		for x in xrange(len(_allemails)):
			data={'lang':'en'}
			data['email'] = _allemails[x]
			req = requests.post('http://www.mailtester.com/testmail.php', data=data)
			_re = re.compile(r"[0-9]+(?:\.[0-9]+){3}")
			_findip = _re.findall(req.content)
			new = []
			for q in _findip:
				if q not in new:
					new.append(q)
			print r+"Email: "+t+"%s"%(_allemails[x])
			for d in range(len(new)):
				v = '\n'.join(new)
				try:
					con = socket.gethostbyaddr(v)
				except socket.error:
					pass
				rf = urllib3.PoolManager()
				res = rf.request('GET', "https://api.shodan.io/shodan/host/%s?key=UNmOjxeFS2mPA3kmzm1sZwC0XjaTTksy"% (new[d]))
				h = json.loads(res.data, 'utf-8')

				if 'country_code' and 'country_name' in h:
					print "\t\t\t|__ %s%s%s (%s)"% (g,new[d],t,con[0])
					print "\t\t\t|\t|"
					print "\t\t\t|\t|__ Country: %s (%s) - City: %s (%s)"% (h['country_code'],h['country_name'],h['city'],h['region_code'])
					print "\t\t\t|\t|__ ISP: %s"% (h['isp'])
					print "\t\t\t|\t|__ Latitude: %s - Longitude: %s"% (h['latitude'],h['longitude'])
					print "\t\t\t|\t|__ Hostname: %s - Organization: %s"% (h['hostnames'],h['org'])
					print ""
				elif 'No information available for that IP.' or 'error' in h:
					print "\t\t\t|__ %s (%s)"% (new[d],con[0])
					print "\t\t\t|\t|__"+r+"No information available for that IP!!"+t
					print ""
				else:
					print "\t\t\t|__ %s (%s)"% (new[d],con[0])

if __name__ == "__main__":
	try:
		start(sys.argv[1:])
	except KeyboardInterrupt as err:
		print r+"\n[!] By... :)"+t
		sys.exit(0)

