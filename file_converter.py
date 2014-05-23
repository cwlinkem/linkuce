#!/usr/bin/python

import os
import re
import sys
import glob
import argparse
import collections

def expand_path(path):
	return os.path.abspath(os.path.expandvars(os.path.expanduser(path)))

def is_file(path):
	if not path:
		return False
	if not os.path.isfile(path):
		return False
	return True

def arg_is_file(path):
   try:
       if not is_file(path):
           raise
   except:
       msg = '{0!r} is not a file'.format(path)
       raise argparse.ArgumentTypeError(msg)
   return expand_path(path)
   
def in_nex(inp): 
	f=file(inp)
	data=[]
	dict={}
	matrix=''
	for line in f:
		data.append(line)
	data=''.join(data)
#	break_match=re.compile(
	if 'matrix' in data:
		data_split=data.split('matrix')
		only_taxa=data_split[1].split(';')
		matrix=only_taxa[0]
	if 'Matrix' in data:
		data_split=data.split('Matrix')
		only_taxa=data_split[1].split(';')
		matrix=only_taxa[0]
	matrix=matrix.strip()
	matrix_list=matrix.split('\n')
	for line in matrix_list:
#		print line
		if line.strip() == '':
			False
		elif line.split()[0] not in dict.keys():
			dict[line.split()[0]]=[line.split()[1]]
		elif line.split()[0] in dict.keys():		
			dict[line.split()[0]].append(line.split()[1])
			for key, value in dict.items():
				dict[key]=[''.join(value)] 
	return dict

def in_fasta(inp):
	f=file(inp)
	identifiers = []
	sequences = []
	current_seq = []
	dict = {}	
	for line in f:
		line = line.strip()
		if line.startswith('>'):
			if current_seq:
				sequences.append(''.join(current_seq))
			identifiers.append(line[1:])
			current_seq = []
		else:
			if line:
				current_seq.append(line)
	if current_seq:
		sequences.append(''.join(current_seq))
	assert(len(identifiers) == len(sequences))
	for n, name in enumerate(identifiers):
		if name in dict:
			dict[name].append(sequences[n])
		else:
			dict[name] = [sequences[n]]
	return dict


def in_phy(inp): 
	f=file(inp)
	lines=0
	dict={}
	for line in f:
		if line == '\n':
			False
		else:
			lines += 1
			if lines > 1:
				if line.split()[0] not in dict.keys():
					dict[line.split()[0]]=[line.split()[1]]
				elif line.split()[0] in dict.keys():		
					dict[line.split()[0]].append(line.split()[1])
					for key, value in dict.items():
						dict[key]=[''.join(value)] 
	return dict

def out_nex(dict, root): 
	outfile=str(root)+".nex"
	outp = open(outfile, 'w')
	outp.write("#NEXUS\n Begin data;\n dimensions ntax = " + str(len(dict)) + " nchar = " + str(len(dict.values()[0][0])) + ";\n Format datatype = DNA gap = - missing = ?;\nMatrix\n")
	dict = collections.OrderedDict(sorted(dict.items()))	
	for k, v in dict.iteritems():
		outp.write(str(k) + '\t' + str(v[0]) + '\n')
	outp.write(';\n end;')
	outp.close()
	
def out_fasta(dict, root): 
	outfile=str(root)+".fasta"
	outp = open(outfile, 'w')
	dict = collections.OrderedDict(sorted(dict.items()))	
	for k, v in dict.iteritems():
		outp.write('>'+str(k)+'\n'+str(v[0])+'\n')
	outp.close()

def out_phy(dict, root): 
	outfile=str(root)+".phy"	
	outp=open(outfile, 'w')		
	outp.write(str(len(dict))+' '+str(len(dict.values()[0][0]))+'\n')	
	dict = collections.OrderedDict(sorted(dict.items()))	
	for k, v in dict.iteritems():
		outp.write(str(k)+'\t'+str(v[0])+'\n')	
	outp.close()
	
def main():
	description = ('This program can be used to convert sequence files from one type '
					'to another by specifying an output format.')
	FILE_FORMATS = ['fasta','nex', 'phy']
	parser = argparse.ArgumentParser(description = description)
	parser.add_argument('input_files', metavar='INPUT-SEQ-FILE',
		nargs = '+',
		type = arg_is_file,
		help = ('Input sequence file(s) name '))
	parser.add_argument('-o', '--out-format',
		type = str,
		choices = ['nex', 'fasta', 'phy'],
		help = ('The format of the output sequence file(s). Valid options '))

	args = parser.parse_args()

	for f in args.input_files:
		in_type=os.path.splitext(f)[1]
		filename=os.path.splitext(f)[0]
		if  in_type == '.nex' or in_type == '.nexus':
			dict=in_nex(f)
		elif in_type == '.fa' or in_type == '.fas' or in_type == '.fasta':
			dict=in_fasta(f)
		elif in_type == '.phy' or in_type == '.phylip':
			dict=in_phy(f)
		if args.out_format == 'nex':
			out_nex(dict, filename)
		elif args.out_format == 'fasta':
			out_fasta(dict, filename)
		elif args.out_format == 'phy':
			out_phy(dict, filename)

if __name__ == '__main__':
	main()