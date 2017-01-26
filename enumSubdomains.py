import requests, json
import os
import sys
from optparse import OptionParser

def makeDir(domain):
	if not os.path.exists(str(os.getcwd()+"/domains")):
		os.makedirs(str(os.getcwd()+"/domains/"))
	dir = str(os.getcwd()+"/domains/"+domain)
	if not os.path.exists(dir):
		os.makedirs(str(os.getcwd()+"/domains/"+domain))
		print ("making directory" + dir)
	else:
		print ("directory exists " + dir)

def storeJsonDomains(result, domain):
	makeDir(domain.strip())
	json_data = json.loads(result)
	file = open(str(os.getcwd())+"/domains/"+domain.strip()+"/subdomains.txt", 'w')
	#print (json_data["subdomains"])
	for s in json_data["subdomains"]:
		file.write(s+'\n')


if __name__ == "__main__":
	
	parser = OptionParser()
	parser.add_option("-f", "--file", action="store", dest="filename",
					  help="newline delimited file containing domains.", metavar="FILE")
	parser.add_option("-d", "--domains", action="store", dest="domains",
					  help="comma separated string of domain(s)", metavar="DOMAINS")
	parser.add_option("-v", action='store_true', dest="verbose",
					  help='Adds some verbosity when running.')

	(options, args) = parser.parse_args()
	verbose = options.verbose
	domain_list = []
	if options.filename:
		with open(options.filename, 'r') as inputFile:
			if verbose:
				print ("Using " +options.filename)
			domain_list = inputFile.read().splitlines()
			

	if options.domains:
		domain_list.extend(options.domains.split(","))
			
	
	for domains in domain_list:
		try:
			url = "https://www.threatcrowd.org/searchApi/v2/domain/report/?domain=" + str(domains)
			print (url)
			result =  requests.get(url)
			#put in directory
			storeJsonDomains(result.text, domains)
		except:
			print("Failed on " + domains)
		pass