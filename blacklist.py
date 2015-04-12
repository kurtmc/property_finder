#!/usr/bin/env python3

def is_blacklisted(url):
	try:
		file = open('.blacklist')
	except FileNotFoundError:
		return False
	blacklisted = url in file.read()
	file.close()
	return blacklisted

def blacklist(url):
	if not is_blacklisted(url):
		file = open('.blacklist', 'a')
		file.write(url + "\n")
