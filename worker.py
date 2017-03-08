import os
import sys
import requests
import json
import socket
import dns.resolver

VERBOSE = False

def getRealHost(domain):
	#print ("Attempting to resolve: " + str(domain.strip()))
	try:
		for res in dns.resolver.query(domain.strip(), 'CNAME'):
			return res.target
	except:
	#	print ("Failed to resolve.\n")
		return False

def doRequest(host,protocol):
	try:
		url = protocol+str(host).strip(".")
		r = requests.get(str(url), verify=False)
		return checkService(r)
	except:
		#print "Unexpected Requests Error:", sys.exc_info()[0]
		return False

def checkService(r):
	#This is where we fingerprint a Request Body
	#TODO Cloudflare
	#error codes to search for

	heroku_error = "there is no app configured at that hostname"
	amazonAWS_error = "NoSuchBucket"
	squarespace_error = "No Such Account"
	squarespace_error2 = "You're Almost There"
	github_error = "There isn't a GitHub Pages site here"
	shopify_error = "Sorry, this shop is currently unavailable"
	tumblr_error = "There's nothing here"
	wpengine_error = "The site you were looking for couldn't be found"

	if heroku_error in r.text:
		return "unclaimed Heroku"
	elif amazonAWS_error in r.text:
		return "unclaimed S3 Bucket"
	elif squarespace_error in r.text:
		return "unclaimed squarespace"
	elif squarespace_error2 in r.text:
		return "unclaimed squarespace"
	elif github_error in r.text:
		return "unclaimed github"
	elif shopify_error in r.text:
		return "unclaimed shopify"
	elif tumblr_error in r.text:
		return "unclaimed tumblr"
	elif wpengine_error in r.text:
		return "unclaimed wp"
	else:
		return "Connection Success"

		#print "Error parsing request body", sys.exc_info()[0]


def checkIfService(host):
	r = doRequest(host,"http://")
	if r is False:
		r = doRequest(host,"https://")
	if r is False:
		return "Connection Failed"
	return r
	
def checkCNAME(cname):
	heroku_error = ["herokuapp"]
	aws_error = ["aws"]
	squarespace_error = ["squarespace","sqsp","sqsp", "sqspcdn"]
	github_error = ["github", "gist"]
	shopify_error = ["shopify"]
	tumblr_error = ["tumblr"]
	wpengine_error = ["wpengine"]
	cname = str(cname)
	for h in heroku_error:
		if h in cname:
			return "heroku cname"
	for h in aws_error:
		if h in cname:
			return "aws cname"
	for h in squarespace_error:
		if h in cname:
			return "ss cname"
	for h in github_error:
		if h in cname:
			return "github cname"
	for h in shopify_error:
		if h in cname:
			return "shopify cname"
	for h in tumblr_error:
		if h in cname:
			return "tumblr cname"
	for h in wpengine_error:
		if h in cname:
			return "wpengine cname"
	return "False"


subdomainList = open(sys.argv[1],'r')
output = open(sys.argv[2],"w")
VERBOSE = sys.argv[3]
if VERBOSE == "t":
	VERBOSE = True
else:
	VERBOSE = False

print ("Starting: " + str(subdomainList))
for name in subdomainList:
	if VERBOSE:
		print ("------")
	name = name.strip()
	CNAME = getRealHost(name)
	if CNAME:
		if VERBOSE:
			print ("Got CNAME:" +str(CNAME))
		# Check if they are hijackable
		result = checkIfService(CNAME)
		result2 = checkCNAME(CNAME)
		if "unclaimed" in result:
			print("FOUND UNCLAIMED SAAS")
			print(name + "," + str(CNAME).strip() + "," + str(result).strip() + "\n")
		if VERBOSE:
			print ("Saving Results")
		#if we connected and had positive cname signature detection
		if "Failed" not in result:
			if "False" not in result2:
				output.write(name + "," + str(CNAME).strip() + "," + str(result).strip() + "\n")
				output.flush()

print ("Finished:" + str(subdomainList))

