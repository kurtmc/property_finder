import urllib.request
from bs4 import BeautifulSoup

class Trademe_Property:
	def __init__(self, url):
		self.url = url
		self.html_page = None
		self.soup = None

	def build_string(self, soup):
		result = ''
		for s in soup.contents:
			result = result + str(s)
		return self.html_to_text(result.strip())

	def get_soup(self):
		if self.soup is None:
			self.soup = BeautifulSoup(self.get_html())
		return self.soup
		

	def html_to_text(self, html_string):
		return html_string.replace("<br/>", "\n")

	def get_attribute(self, tag, attrs={}):
		soup = self.get_soup()
		attribute = soup.find(tag, attrs)
		return self.build_string(attribute)

	def get_description(self):
		return self.get_attribute('div', {'id': 'ListingDescription_ListingDescription'})
	
	def get_price(self):
		return self.get_attribute('li', {'id': 'ListingTitle_classifiedTitlePrice'})

	def get_address(self):
		soup = self.get_soup()
		address = soup.find('th', {'id': 'ListingAttributes_AttributesRepeater_ctl01_ltHeaderRow'}).parent.findNext('td')
		return self.build_string(address)

	def get_title(self):
		return self.get_attribute('h1', {'id': 'ListingTitle_title'})

	def get_html(self):
		if self.html_page is None:
			self.html_page = urllib.request.urlopen(self.url)
		return self.html_page
			

