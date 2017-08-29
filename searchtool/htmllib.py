"""
	htmllib - holds functions used for extracting and parsing html
"""
import sys
import urllib3
from bs4 import BeautifulSoup
import searchtool.settings as sets


def getHTML():
	"""
		For each of the urls in query_duplications, get the HTML and store it in the query_articles collection
	"""
	db = sets.getDB()


	for item in db.query_duplications.find():
		url = item['url']

		# if the article doesn't already exist, get the html
		if db.query_articles.findOne({"url": url}).count() == 0:
			try:
				# Get raw html
				http_pool = urllib3.connection_from_url(url)
				r = http_pool.urlopen('GET', url)
				raw_html = r.data.decode('utf-8')


				# Get soup
				soup = BeautifulSoup(raw_html, 'html5lib')

				head = soup.find('head')
				body = soup.find('body')

				db.query_articles.insert({
					"url"		:	url,
					"raw_html"	:	raw_html,
					"head"		:	head,
					"body"		:	body
				})
			except:
				print("ERROR: ", sys.exc_info()[0])

	print("Finished retrieving HTML")
