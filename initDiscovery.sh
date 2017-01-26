#!/bin/bash
# first parameter is the domain to search

mkdir ./$1
git init
python /opt/wfuzz/wfuzz.py -w /opt/SecLists/Discovery/Web_Content/SVNDigger/all.txt --hc 404 https://$1/FUZZ > files
git add files
git commit -m "initial profile"

