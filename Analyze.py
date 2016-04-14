import sys
import urllib.request	#python3
from bs4 import BeautifulSoup


def AnalyzePage(page_url):

	#Fetch HTML
	response = urllib.request.urlopen(page_url)
	html = response.read()
	soup = BeautifulSoup(html)
	print(soup.prettify())

def main():
    
    if len(sys.argv) != 2:
    	print("Please enter a single argument")
    	return

    AnalyzePage(sys.argv[1])


if __name__ == "__main__":
    main()