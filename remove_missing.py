import re
import glob
import sys
import fileinput


def get_nchar(name):
	word=re.compile(r'nchar\=\d*')
	for nchar in word.findall(open(name).read()):
		nchar=nchar.split('=')
		nchar=nchar[1]
	return nchar

def get_ntax(name):
	word=re.compile(r'ntax\=\d*')
	for ntax in word.findall(open(name).read()):
		ntax=ntax.split('=')
		ntax=ntax[1]
	return ntax

def remove_seqs(name, missing_string, ntax):		
	ntax=int(ntax)
	for line in fileinput.input(name, inplace=1):
		if missing_string in line:
			ntax = ntax-1 
		if missing_string not in line:
			sys.stdout.write(line)
	return ntax
	
def change_ntax(name, new_ntax):
	word=re.compile(r'ntax\=\d*')
	f=open(name).read()
	new_f=word.sub('ntax='+str(new_ntax),f)
	new_out=open(name,'w')
	new_out.write(new_f)


for name in glob.glob('*.nex'):
	nchar=get_nchar(name)
	ntax=get_ntax(name)
	missing_string='-'*int(nchar)
	new_ntax=remove_seqs(name, missing_string, ntax)
	change_ntax(name, new_ntax)	
	
