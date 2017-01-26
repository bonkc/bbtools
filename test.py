import socket
import dns.resolver
import requests
import sys


import os
import sys
import requests
import json
import socket
import dns.resolver



def getRealHost(domain):
	print ("Attempting to resolve: " + str(domain.strip()))
	try:
		for res in dns.resolver.query(domain.strip(), 'CNAME'):
			return res.target
	except:
		print ("Failed to resolve.\n")
		return False

def doRequest(host,protocol):
	try:
		url = protocol+str(host).strip(".")+"/test.html"
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
		return "Not SaaS"



def checkIfService(host):
	r = doRequest(host,"http://")
	if r is False:
		r = doRequest(host,"https://")
	if r is False:
		return "Connection Failed"
	return r
	
	



CNAME = "localhost:8000"
#CNAME = getRealHost(name)
if CNAME:
	print ("Got CNAME:" +str(CNAME))
	# Check if they are hijackable
	result = checkIfService(CNAME)
	print ("Saving Results")
	print (CNAME + "," + str(CNAME).strip() + "," + str(result).strip() + "\n")