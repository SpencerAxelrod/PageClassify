import sys
import urllib.request	#python3
import requests
from bs4 import BeautifulSoup

def fetch_html(page_url):
	"""Returns the HTML of the page at page_url"""

	html = ""
	#spoof header for sites like Amazon that make it more dfficult to scrape 
	try:
		req = urllib.request.Request(page_url, headers={ 'User-Agent': 'Mozilla/5.0' })
		html = urllib.request.urlopen(req).read()
	except urllib.error.URLError as e:
		print("page request failed: " + repr(e))
		return

	return html


def analyze_page(page_url):
	"""Analyzes the content at page_url and returns a that best describe the contents of that page"""
	
	html = fetch_html(page_url)
	if not html:
		return

	soup = BeautifulSoup(html, "html.parser")
	#print(soup.prettify())
	#titleTag = soup.html.head.title
	#print(titleTag.string)
	#print(soup.find_all())

	word_counts = {}
	ignore_tags = ["script", "div", "img", "meta", "span"]
	for tag in soup.find_all():
		#if tag.name == "span":
			#print()
			#print(tag.name + " \" " + " ".join(tag.text.strip().split()) +" \" ")

		words = tag.text.split()
		for word in words:
			word_lower = word.lower()
			if word_lower in word_counts:
				word_counts[word_lower] = word_counts[word_lower] + 1
			else:
				word_counts[word_lower] = 1
		#print(words)
	print(sorted(word_counts.items(), key=lambda x:x[1]))




def main():
    
    if len(sys.argv) != 2:
    	print("Please enter a single argument")
    	return

    analyze_page(sys.argv[1])


if __name__ == "__main__":
    main()