import sys
import urllib.request	#python3
import requests
from bs4 import BeautifulSoup

def fetch_html(page_url):
	"""Returns the HTML of the page at page_url"""
	html = ""
	#spoof header for sites like Amazon that make it more dfficult to scrape 
	req = urllib.request.Request(page_url, headers={ 'User-Agent': 'Mozilla/5.0' })
	html = urllib.request.urlopen(req).read()
	return html


def analyze_page(page_url):
	"""Analyzes the content at page_url and returns a that best describe the contents of that page"""
	
	html = fetch_html(page_url)
	soup = BeautifulSoup(html, "html.parser")
	#print(soup.prettify())
	#titleTag = soup.html.head.title
	#print(titleTag.string)
	print(soup.title.string)
	


def main():
    
    if len(sys.argv) != 2:
    	print("Please enter a single argument")
    	return

    analyze_page(sys.argv[1])


if __name__ == "__main__":
    main()