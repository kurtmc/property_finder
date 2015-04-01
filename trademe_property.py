import urllib.request
from bs4 import BeautifulSoup

class Trademe_Property:
	def __init__(self, url):
		self.url = url
		self.html_page = None
	def build_string(self, soup):
		result = ''
		for s in soup.contents:
			result = result + str(s)
		return result

	def get_description(self):
		soup = BeautifulSoup(self.get_html())
		description = soup.find('div', {'id': 'ListingDescription_ListingDescription'})
		return self.build_string(description)
	
	def get_price(self):
		soup = BeautifulSoup(self.get_html())
		price = soup.find('li', {'id': 'ListingTitle_classifiedTitlePrice'})
		return self.build_string(price)

	def get_address(self):
		soup = BeautifulSoup(self.get_html())
		address = soup.find('th', {'id': 'ListingAttributes_AttributesRepeater_ctl01_ltHeaderRow'}).parent.findNext('td')
		return self.build_string(address)

	def get_html(self):
		if self.html_page is None:
			self.html_page = urllib.request.urlopen(self.url)
		return self.html_page
			

