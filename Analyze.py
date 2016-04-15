import sys
import urllib.request	#python3
import requests
import nltk
#from stemming.porter2 import stem
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from stop_words import get_stop_words
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
	#html = """<html><head><title>The Dormouse's story</title></head><body><p class="title"><b>The Dormouse's story</b></p><p class="story">Once upon a time there were three little sisters; and their names were<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;and they lived at the bottom of a well.</p><p class="story">...</p>"""
	if not html:
		return

	soup = BeautifulSoup(html, "html.parser")
	#print(soup.prettify())
	#titleTag = soup.html.head.title
	#print(titleTag.string)
	#print(soup.find_all())

	word_counts = {}
	#nltk.download('all')
	#stop_words =  stopwords.words("english")
	stop_words = get_stop_words('english')
	words_to_add = ['like', '...']
	stop_words = stop_words + words_to_add
	#print(stop_words)


	#ignore_tags = ["script", "img", "meta", "link" "style"]
	ignore_tags = ["script", "img", "meta", "style"]

	#print(soup.find_all())

	"""for tag in soup.find_all():
		words = tag.find(text=True, recursive=False)
		if words:
			words = words.split()
			for word in words:
				word_lower = word.lower()
				#print()
				#print(word_lower, tag.name)
				if word_lower not in stop_words:
					if word_lower == "outdoors":
						print(word_lower, tag)"""
						

	weights = {'title': 20, 'span': .5, "link": .2}
	lemma = WordNetLemmatizer()
	for tag in soup.find_all():
		#if tag.name == "span":
			#print()
			#print(tag.name + " \" " + " ".join(tag.text.strip().split()) +" \" ")
		if tag.name not in ignore_tags:
			#print()
			#print(tag.name, tag, tag.find_all())
			words = tag.find(text=True, recursive=False)
			if words:
				words = words.split()
				for word in words:
					word_lower = lemma.lemmatize(word.lower())
					#print()
					#print(word_lower, tag.name)
					if word_lower not in stop_words and len(word_lower) > 1:

						#if word_lower == "nsa":
							#print(tag.name)
						multiplier = 1
						if tag.name in weights:
							multiplier = weights[tag.name] 
						if word_lower in word_counts:
							word_counts[word_lower] = word_counts[word_lower] + (1 * multiplier)
						else:
							word_counts[word_lower] = 1 * multiplier
				#print(words)
	#print(sorted(word_counts.items(), key=lambda x:x[1])[-50:])
	#print(word_counts["cpt-122"])

	for x in reversed(sorted(word_counts.items(), key=lambda x:x[1])[-20:]):
		print(x)




def main():
    
    if len(sys.argv) != 2:
    	print("Please enter a single argument")
    	return

    analyze_page(sys.argv[1])


if __name__ == "__main__":
    main()