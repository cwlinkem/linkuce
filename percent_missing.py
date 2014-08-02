#! usr/bin/python

import re
import sys
import subprocess

def in_phy(inp):
	head=''
	lines=0
	dict={}
	for line in inp:
		lines += 1
		if lines == 1:
			head=line
		else:
			if line.split()[0] not in dict.keys():
				dict[line.split()[0]]=line.split()[1]

	return dict

def missing_count(dict):
	for k,v in dict.iteritems():
		missing=v.count('-')
		denom=len(v)+0.0
		percent=int(missing)/denom
		print k, percent

file_name=sys.argv[1]

inp=file(file_name)

missing_count(in_phy(inp))