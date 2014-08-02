import sys
import csv
import re
import subprocess
import glob


def combine_rax_trees(filename):
	f=file(filename)
	first_line=f.readline()
	line=first_line.strip()
	return line


def parse_trees():
#read in file of raxml trees and remove branch lengths
	file_name="1phrynosomatids_raxtrees.tre"
	f=file(file_name)
	out_file = '1phrynosomatids_rax_nobr.tre' #Create file for output
	outp = open(out_file, 'w')
	for lines in f:
		lines=lines.strip()
		min_tree=re.sub('\:\d\.\d*','',lines)
		outp.write(str(min_tree)+"\n")
	outp.close()
	

def run_stells():
	stells=subprocess.Popen('stells-v1-6-mac -g agama_rax_nobr.tre', shell=True, executable='/bin/bash')
	stells.wait()





########################################################################################################################################################
file_name="1phrynosomatids_raxtrees.tre"
outp=open(file_name, 'w')

for filename in glob.glob("RAxML_bestTree*"):
	rax_tree=combine_rax_trees(filename)
	outp.write(str(rax_tree)+"\n")
	

outp.close()

rax_nobr=parse_trees()

#run_stells()
	
print "Program has completed"
