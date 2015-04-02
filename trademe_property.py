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

	def get_description(self):
		soup = self.get_soup()
		description = soup.find('div', {'id': 'ListingDescription_ListingDescription'})
		return self.build_string(description)
	
	def get_price(self):
		soup = self.get_soup()
		price = soup.find('li', {'id': 'ListingTitle_classifiedTitlePrice'})
		return self.build_string(price)

	def get_address(self):
		soup = self.get_soup()
		address = soup.find('th', {'id': 'ListingAttributes_AttributesRepeater_ctl01_ltHeaderRow'}).parent.findNext('td')
		return self.build_string(address)
	def get_title(self):
		soup = self.get_soup()
		title = soup.find('h1', {'id': 'ListingTitle_title'})
		return self.build_string(title)

	def get_html(self):
		if self.html_page is None:
			self.html_page = urllib.request.urlopen(self.url)
		return self.html_page
			

