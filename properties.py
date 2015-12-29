#!/usr/bin/env python3

import urllib.request
import re
from bs4 import BeautifulSoup
import webbrowser
from trademe_property import Trademe_Property
import blacklist
import sys, getopt

def get_urls(url):
	urls = list()
	try:
		html_page = urllib.request.urlopen(url)
	except urllib.error.URLError:
		print("Timed out trying to get page")
		exit(1)
	soup = BeautifulSoup(html_page, "html.parser")
	for link in soup.findAll('a'):
		urls.append(link.get('href'))
	return urls

def get_properties_trademe(price_start, price_end, keywords=[]):
	keywords_str = '+'.join(map(str, keywords))
	url = 'http://www.trademe.co.nz/Browse/CategoryAttributeSearchResults.aspx?search=1&cid=5748&sidebar=1&rptpath=350-5748-4233-&132=FLAT&selected135=7&selected136=89&134=1&135=7&136=89&216=0&216=0&217=0&217=0&153=' + keywords_str + '&122=0&122=1&59=' + price_start + '00' + '&59=' + price_end + '00' + '&178=0&178=0&sidebarSearch_keypresses=0&sidebarSearch_suggested=0'

	urls = get_urls(url)
	properties = list()
	for u in urls:
		if u is not None and 'auction' in u:
			properties.append(u)

	properties.sort()
	properties = list(set(properties))

	for i in range(0, len(properties)):
		properties[i] = 'http://www.trademe.co.nz' + properties[i]

	return properties

def words_in_string(words, string):
	for word in words:
		if word_in_string(word, string):
			return True
	return False

def word_in_string(word, string):
	return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search(string)

# Stolen from stackoverflow (http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text)
def visible(element):
	if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
		return False
	elif re.match('<!--.*-->', str(element)):
		return False
	return True

def print_help():
	print("Search for properties in price range")
	print("./properties -s <start price> -e <end price>")
	print("Blacklist a property")
	print("./properties -b <url>")
	print("Print this message")
	print("./properties -h")

if __name__ == '__main__':
	# Command line options
	start_price = None
	end_price = None
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hs:e:b:", ["help", "start_price", "end_price", "blacklist"])
	except getopt.GetoptError:
		print_help()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print_help()
			sys.exit(2)
		elif opt in ("-b", "--blacklist"):
			blacklist.blacklist(arg)
			print("Blacklisted " + arg);
			sys.exit(0)
		elif opt in ("-s", "--start_price"):
			start_price = arg
		elif opt in ("-e", "--end_price"):
			end_price = arg

	if start_price is None or end_price is None:
		print_help()
		sys.exit(1)

	urls = get_properties_trademe(start_price, end_price)
	properties = list()
	for url in urls:
		if not blacklist.is_blacklisted(url):
			properties.append(Trademe_Property(url))

	unfurnished = list()
	for p in properties:
		p_text = filter(visible, p.get_soup().findAll(text=True))
		p_text = " ".join(p_text)
		if not words_in_string(["furnished", "rented", "bed"], p_text):
			unfurnished.append(p)

	unfurnished = list(set(unfurnished))

	for p in unfurnished:
		print("Title: " + p.get_title())
		#print("Description:")
		#print(p.get_description()[:200])
		print("url: " + p.url)
		print("Price: " + p.get_price())
		print("Address: " + ", ".join(p.get_address().splitlines()))
		print()
