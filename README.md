# PageClassify
Given any page (URL), this program classifies the page, and return a list of relevant topics.

Dependencies:

Install BeautifulSoup4 HTML parser for python3:
	python3 -m pip install beautifulsoup4

Intall Requests module:
	python3 -m pip install requests

Run from command line: 
	~$ python3 Analyze.py <WEB PAGE URL IN QUOTES>


This implementation fetches the HTML and subsequently the word count for each word via Beautiful Soup. Common stop words and single character words are ignored. Weights are assigned to words based on the HTML tag (ignoring certain tags, e.g.'script'). Further weight is given to words in the page URL string. 

The implementation is sufficient for finding single words. For phrases, I started keeping track of strings of up to 5 words in a row. If phrases like these are repeated, the longer the phrase the more weight they will have overall. The top 25 highest weighted words/phrases are then checked with each other to see if one is a substring of another, then returned.

After playing with the weights, I found that the weights in the final implementation gave the most accurate results over a range of web pages. The rationale is that, in general, the URL and 'title' tags hold high importance in terms of relevancy. Additionally, if a multi-word phrase is repeated, it is likely to hold value as a relevant phrase.


Examples, with output (ensure arguments in quotations):

	~$ python3 Analyze.py "http://www.cbsnews.com/news/seoul-says-north-korea-launch-of-a-missile-appears-to-have-failed/"
	north
	korea
	missile
	news
	launch
	failed
	appears
	cbs
	north korea missile launch appears
	korea missile launch appears failed
	launch appears failed cbs news
	

	~$ python3 Analyze.py "http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/""
	snowden
	edward
	2013
	nsa
	man behind nsa leak say
	nsa leak say safeguard privacy,
	behind nsa leak say safeguard
	leak say safeguard privacy, liberty
	

	~$ python3 Analyze.py http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/
	friend
	outdoors
	introduce
	indoorsy
	introduce your indoorsy friend outdoors
	camp
	indoorsy friend outdoors rei blog
	rei
	blog
	take
	keep
	might
	great
	

	~$ python3 Analyze.py "http://www.amazon.com/Cuisinart-CPT-122-Compact-2-Slice-Toaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster"
	toaster
	cuisinart
	2-slice
	star
	conair cuisinart cpt-122 2-slice compact
	cpt-122 2-slice compact plastic toaster
	cuisinart cpt-122 2-slice compact plastic
	compact
	kitchen dining
	plastic
	

Some sites HTML response may not cooperate with being scraped
