import re
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
	""" Returns the HTML of the page at page_url """
	html = ""
	#spoof header for sites like Amazon that make it more dfficult to scrape 
	try:
		req = urllib.request.Request(page_url, headers={ 'User-Agent': 'Mozilla/5.0' })
		html = urllib.request.urlopen(req).read()
	except urllib.error.URLError as e:
		print("page request failed: " + repr(e))
		return

	return html

def words_in_url(page_url):
	""" Delimits a url string by '/' and '-' """
	words = re.split('; |, |\-|\/',page_url)
	return words


def analyze_page(page_url):
	""" Analyzes the content at page_url and returns a that best describe the contents of that page """
	html = fetch_html(page_url)
	#html = """<html><head><title>The Dormouse's story</title></head><body><p class="title"><b>The Dormouse's story</b></p><p class="story">Once upon a time there were three little sisters; and their names were<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;and they lived at the bottom of a well.</p><p class="story">...</p>"""
	if not html:
		return

	soup = BeautifulSoup(html, "html.parser")
	word_counts = {}
	url_words = words_in_url(page_url)
	stop_words = get_stop_words('english')
	words_to_add = ['like', '...']
	stop_words = stop_words + words_to_add
	ignore_tags = ["script", "img", "meta", "style"]		
	weights = {'title': 20, 'span': .5, "link": .2, 'url': 20}
	lemma = WordNetLemmatizer()

	for tag in soup.find_all():

		if tag.name not in ignore_tags:
			words = tag.find(text=True, recursive=False)

			if words:
				words = words.split()
				words = [' '.join(w for w in word.split() if w.lower() not in stop_words) for word in words]
				words = [' '.join(w for w in word.split() if len(w.lower()) > 1) for word in words]		
				
				for index, word in enumerate(words):
					word_lower = lemma.lemmatize(word.lower())

					if word_lower not in stop_words:

						if len(word_lower) > 1:
							multiplier = 1

							if tag.name in weights:
								multiplier = weights[tag.name] 
							
							if word_lower in word_counts:
								word_counts[word_lower] = word_counts[word_lower] + (1 * multiplier)

							else:
								word_counts[word_lower] = 1 * multiplier

							multiplier = 1
							if index < (len(words) - 1):
								two_word = word_lower + ' ' + lemma.lemmatize((words[index + 1]).lower()).strip()
								two_word = two_word.strip()
								if two_word != word_lower:

									if two_word in word_counts:
										word_counts[two_word] = word_counts[two_word] + (2 * multiplier)

									else:
										word_counts[two_word] = 1 * multiplier

							multiplier = 1
							if index < (len(words) - 2):
								two_word = word_lower + ' ' + lemma.lemmatize((words[index + 1]).lower()).strip() + ' ' + lemma.lemmatize((words[index + 2]).lower()).strip()
								two_word = two_word.strip()

								if two_word != word_lower:

									if two_word in word_counts:
										word_counts[two_word] = word_counts[two_word] + (50 * multiplier)

									else:
										word_counts[two_word] = 1 * multiplier


	for word in url_words:
		if word in word_counts:
			word_counts[word] = word_counts[word] + 20



	for x in reversed(sorted(word_counts.items(), key=lambda x:x[1])[-20:]):
		print(x)



def main():
   
    if len(sys.argv) != 2:
    	print("Please enter a single argument")
    	return

    analyze_page(sys.argv[1])


if __name__ == "__main__":
    main()