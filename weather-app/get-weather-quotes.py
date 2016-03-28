# Use virtualenv
# pip install virtualenv (optional)
# pip install selenium
# brew install phantomjs

import pprint
import requests
from selenium import webdriver

#browser = webdriver.Firefox()
browser = webdriver.PhantomJS()

# Let's get all weather quotes
# To get all weather quotes we will refer to this url: https://theysaidso.com/tag/weather

# This is our starting url to reterive weather quotes
base_website_url = "https://theysaidso.com"
base_weather_quote_url = "https://theysaidso.com/tag/weather"
quotes_page = browser.get(base_weather_quote_url)

# Find out how many pages we need to parse through to get all weather quotes
pagination_list = browser.find_elements_by_xpath("//*[@class='pagination']/li")

current_page = 1
# Penultimate element contains the last page number. Let's get that so that we can loop through and get all pages!
total_pages = int(len(pagination_list)-2)

quotes_array = []

# For Each page
for i in range(0,total_pages+1):
	authors = []
	quote_links = []
	
	# Get Author links available on this page
	author_links = browser.find_elements_by_xpath("//*[@class='timeline-title']/a")
	for author in author_links:
		#print author.text
		authors.append(author.text)
	
	# Extract links to detail quotes
	quote_pointers = browser.find_elements_by_xpath("//*[@class='timeline-body']/p[@class='desc']/a")
	for quote_pointer in quote_pointers:
		#print quote_pointer.get_attribute('href')
		quote_links.append(quote_pointer.get_attribute('href'))
	
	# Now get all quotes first before we move to next quotes page!
	quotes = []
	for link in quote_links:
		#print link
		browser.get(link)
		# There is only one quote element on this page!
		quote = browser.find_element_by_xpath("//*[@class='lead']")
		#print quote.text
		quotes.append(quote.text)
	
	# Build json object
	for k in range(len(authors)):
		single_quote_dict = {}
		single_quote_dict["Author"] = authors[k]
		single_quote_dict["Quote"] = quotes[k]
		single_quote_dict["Source"] = quote_links[k]
		single_quote_dict["Category"] = "weather"
		quotes_array.append(single_quote_dict)
		
	# Go to next page https://theysaidso.com/tag/weather/<page_number>"
	browser.get(base_weather_quote_url + "/" + str(i))
	
browser.close()
pprint.pprint(quotes_array)
