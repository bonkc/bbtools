#!/bin/bash

python /opt/wfuzz/wfuzz.py -w /opt/SecLists/Discovery/Web_Content/SVNDigger/all.txt -o csv --hc 404 https://$1/FUZZ > $2
git add files
if git commit -m "scan"; then
	git diff HEAD^ HEAD files
