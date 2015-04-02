#!/usr/bin/env python3

import urllib.request
import re
from bs4 import BeautifulSoup
import webbrowser
from trademe_property import Trademe_Property

def get_urls(url):
	urls = list()
	try:
		html_page = urllib.request.urlopen(url)
	except urllib.error.URLError:
		print("Timed out trying to get page")
		exit(1)
	soup = BeautifulSoup(html_page)
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

if __name__ == '__main__':
	urls = get_properties_trademe('250', '400')
	properties = list()
	for url in urls:
		properties.append(Trademe_Property(url))

	unfurnished = list()
	for p in properties:
		p_html = p.build_string(p.get_soup())
		if not words_in_string(["furnished", "rented", "bed"], p_html):
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
