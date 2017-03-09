
import os
import sys
import requests
import json
import codecs
from BeautifulSoup import BeautifulSoup

programsUrl = "https://hackerone.com/programs/search?query=bounties%3Ayes&sort=published_at%3Adescending&page=1"
h1url = "https://hackerone.com"

programs = []
scopes = []

def getHTML(url):
	
	try:
		#
		headers = {"X-Requested-With":"XMLHttpRequest", "accept": "application/json"}
		html = requests.get(url, headers=headers)
		safe_html = (html.text).encode('cp850',errors='replace')
		return (safe_html)
	except:
		pass

def getPrograms(pages):
	for x in range(1,pages):
		try:
			res = getHTML("https://hackerone.com/programs/search?query=bounties%3Ayes&sort=published_at%3Adescending&page=" + str(x))
			split = res.split(",")
			#jhtml = json.loads(safe_html)
			for parts in split:
				if '"url"' in parts:
					programs.append((parts).split(":")[1].strip('"'))
		except:
			pass

def cleanURL(url):
	if url.startswith("http:"):
		url = url[6:]
	if url.startswith("https:"):
		url = url[7:]
	if url[0] == "*":
		return url[2:]
	else:
		return url.strip("\\")

def getRootDomain(url):
	url = url.split(".")
	return (url[-2]+"."+url[-1])

if __name__ == "__main__":

	saveFile = "domains.txt"
	file = open(saveFile, "w")

	getPrograms(4)

	for program in programs:
		x = h1url + program
		print("Program: " + str(x))
		res = getHTML(h1url + program)
		#Best effort to decode the JSON atm. Could manage to ASCII but would probably point to the wrong domains.
		try:
			j = json.loads(res)
		except:
			print("Failed to load JSON data for " + str(program))
			print("Unexpected error: ", sys.exc_info()[0])
			pass

		for domains in j['scopes']:
			try:
				print ("Domain:")
				d = (cleanURL(domains.encode('cp850',errors='replace')))
				print (d)
				print ("root domain: " + getRootDomain(d))
				scopes.append(d)
				scopes.append(getRootDomain(d))
			except:
				print ("Failed to read for: " + str(program))
				pass
	#remove duplicates
	scopes = list(set(scopes))
	for programs in scopes:
		file.write(programs + "\n")

	#parsed_html = BeautifulSoup(html.text)
	#print (parsed_html.text)
	#programs = parsed_html.body.find('table', attrs={"class":"leaderboard"})

	#print(programs)

