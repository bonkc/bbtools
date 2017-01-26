import os
import sys
import subprocess
from optparse import OptionParser

#Spawn works, one for each domain

if __name__ == "__main__":
	
	parser = OptionParser()
	parser.add_option("-f", "--file", action="store", dest="filename",
					  help="newline delimited file containing subdomains.", metavar="FILE")
	parser.add_option("-d", "--domains", action="store", dest="domains",
					  help="comma separated string of subdomain(s)", metavar="DOMAINS")
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
cwd = os.getcwd()
workerScript = cwd+"/worker.py"
for domains in (os.listdir(str(os.getcwd()+"/domains/"))):

	subdomainLists = str(cwd+"/domains/"+domains.strip())
	input = subdomainLists + "/subdomains.txt" 
	output = subdomainLists + "/resolvedSubdomains.txt"

	cmd = ["python", workerScript, input,output]
	
	print (cmd)
	subprocess.Popen(cmd)

		
	



