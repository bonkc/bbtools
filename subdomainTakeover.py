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
	#parser.add_option("-d", "--debug", action="store", dest = "debug", help="adds more verbose output.")

	(options, args) = parser.parse_args()
	if options.verbose:
		verbose = True
	else:
		verbose = False
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
if verbose:
	print("cwd:" + cwd)
workerScript = cwd+"/worker.py"
if verbose:
	print("Worker script location" + workerScript)
for domains in (os.listdir(str(os.getcwd()+"/domains/"))):


	subdomainLists = str(cwd+"/domains/"+domains.strip())
	if verbose:
		print("subdomainLists:" + subdomainLists)
	input = subdomainLists + "/subdomains.txt" 
	output = subdomainLists + "/resolvedSubdomains.txt"
	if verbose:
		v = "t"
	else:
		v = "f"

	cmd = ["python", workerScript, input,output,v, "2>/dev/null"]
	if verbose:
		print (cmd)
	subprocess.Popen(cmd)

		
	



