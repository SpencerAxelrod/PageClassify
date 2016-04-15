import re
import sys
import urllib.request	#python3
import requests
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from stop_words import get_stop_words
from bs4 import BeautifulSoup

def fetch_html(page_url):
	""" Returns the HTML of the page at page_url """
	html = ""
	try:
		#spoof header for sites like Amazon that make it more dfficult to scrape 
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
	""" Analyzes the content at page_url and returns a list of the highes weighted
	 words/phrases and their weights """
	html = fetch_html(page_url)
	if not html:
		return

	soup = BeautifulSoup(html, "html.parser")
	word_counts = {}
	url_words = words_in_url(page_url)
	stop_words = get_stop_words('english')
	words_to_add = ['like', '...']
	stop_words = stop_words + words_to_add
	ignore_tags = ["script", "img", "meta", "style"]    #html tags to ignore
	weights = {'title': 15, 'div': .5, 'a': .3, 'span': .5, "link": .2, 'url': 22, \
				'two': 3, 'three': 3, 'four': 5, 'five': 5}    #adjust weights here
	lemma = WordNetLemmatizer()

	for tag in soup.find_all():

		if tag.name not in ignore_tags:
			words = tag.find(text=True, recursive=False)    #with bs4, recursive = False means we will not be double counting tags

			if words:
				words = words.split()
				words = [w for w in words if w not in stop_words]    #remove common stop words
				words = [w for w in words if len(w) > 1]    #ignore single character words
				
				for index, word in enumerate(words):
					word_lower = lemma.lemmatize(word.lower())	#lemmatize/stem words

					multiplier = 1

					if tag.name in weights:    #assign weight based on HTML tag
						multiplier = weights[tag.name] 
					
					if word_lower in word_counts:
						word_counts[word_lower] = word_counts[word_lower] + (1 * multiplier)

					else:
						word_counts[word_lower] = 1 * multiplier

					
					if index < (len(words) - 1):    #two word phrase
						two_word = word_lower + ' ' + lemma.lemmatize((words[index + 1]).lower()).strip()
						two_word = two_word.strip()
						if two_word != word_lower:

							if two_word in word_counts:
								word_counts[two_word] = word_counts[two_word] + (weights['two'] * multiplier)

							else:
								word_counts[two_word] = 1 * multiplier

					if index < (len(words) - 2):    #three word phrase
						two_word = word_lower + ' ' + lemma.lemmatize((words[index + 1]).lower()).strip() \
									 + ' ' + lemma.lemmatize((words[index + 2]).lower()).strip()
						two_word = two_word.strip()

						if two_word != word_lower:

							if two_word in word_counts:
								word_counts[two_word] = word_counts[two_word] + (weights['three'] * multiplier)

							else:
								word_counts[two_word] = 1 * multiplier

					if index < (len(words) - 3):    #four word phrase
						two_word = word_lower + ' ' + lemma.lemmatize((words[index + 1]).lower()).strip() \
										 + ' ' + lemma.lemmatize((words[index + 2]).lower()).strip() \
										 + ' ' + lemma.lemmatize((words[index + 3]).lower()).strip()
						two_word = two_word.strip()

						if two_word != word_lower:

							if two_word in word_counts:
								word_counts[two_word] = word_counts[two_word] + (weights['four'] * multiplier)

							else:
								word_counts[two_word] = 1 * multiplier

					if index < (len(words) - 4):    #five word phrase
						two_word = word_lower + ' ' + lemma.lemmatize((words[index + 1]).lower()).strip() \
										+ ' ' + lemma.lemmatize((words[index + 2]).lower()).strip() \
										+ ' ' + lemma.lemmatize((words[index + 3]).lower()).strip() \
										+ ' ' + lemma.lemmatize((words[index + 4]).lower()).strip()
						two_word = two_word.strip()

						if two_word != word_lower:

							if two_word in word_counts:
								word_counts[two_word] = word_counts[two_word] + (weights['five'] * multiplier)

							else:
								word_counts[two_word] = 1 * multiplier
										


	for word in url_words:    #add weight for words in the url string
		if word in word_counts:
			word_counts[word] = word_counts[word] + weights['url']

	def determine(x, top_25):
		""" Helper function for removing phrases that are substrings of other phrases """
		if len(x[0].split()) > 1:
			#print(x[0])
			for i in top_25:
				if x[0] in i[0] and x[0] != i[0]:
					return False
				
		return True

	top_25 = list(reversed(sorted(word_counts.items(), key=lambda x:x[1])[-25:]))    #grab highest 25 weighted items
	final_list = [x for x in top_25 if determine(x, top_25)]    #remove phrases that are substrings of other phrases

	return final_list



def main():
   
    if len(sys.argv) != 2:
    	print("Please enter a single argument")
    	return

    results = analyze_page(sys.argv[1])
    if results:
	    for r in results:
	    	print(r[0])

if __name__ == "__main__":
    main()