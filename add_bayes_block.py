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

def bayes_block(model):
	block_start="Begin mrbayes;\n set autoclose = yes;\n\n"
	model_block=''
	if model == 'JC':
		model_block="Lset nst=1 rates=equal;\nPrset statefreqpr=fixed(equal);\n"
	elif model == 'JC+G':
		model_block="Lset nst=1 rates=gamma;\nPrset statefreqpr=fixed(equal);\n"
	elif model == 'JC+I':
		model_block="Lset nst=1 rates=propinv;\nPrset statefreqpr=fixed(equal);\n"
	elif model == 'JC+I+G':
		model_block="Lset nst=1 rates=invgamma;\nPrset statefreqpr=fixed(equal);\n"
	elif model == 'F81':
		model_block="Lset nst=1 rates=equal;\n"
	elif model == 'F81+G':
		model_block="Lset nst=1 rates=gamma;\n"
	elif model == 'F81+I':
		model_block="Lset nst=1 rates=propinv;\n"
	elif model == 'F81+I+G':
		model_block="Lset nst=1 rates=invgamma;\n"
	elif model == 'K80':
		model_block="Lset nst=2 rates=equal;\nPrset statefreqpr=fixed(equal);\n"
	elif model == 'K80+G':
		model_block="Lset nst=2 rates=gamma;\nPrset statefreqpr=fixed(equal);\n"
	elif model == 'K80+I':
		model_block="Lset nst=2 rates=propinv;\nPrset statefreqpr=fixed(equal);\n"
	elif model == 'K80+I+G':
		model_block="Lset nst=2 rates=invgamma;\nPrset statefreqpr=fixed(equal);\n"
	elif model == 'HKY':
		model_block="Lset nst=2 rates=equal;\n"
	elif model == 'HKY+G':
		model_block="Lset nst=2 rates=gamma;\n"
	elif model == 'HKY+I':
		model_block="Lset nst=2 rates=propinv;\n"
	elif model == 'HKY+I+G':
		model_block="Lset nst=2 rates=invgamma;\n"
	elif model == 'SYM':
		model_block="Lset nst=6 rates=equal;\nPrset statefreqpr=fixed(equal);\n"
	elif model == 'SYM+G':
		model_block="Lset nst=6 rates=gamma;\nPrset statefreqpr=fixed(equal);\n"
	elif model == 'SYM+I':
		model_block="Lset nst=6 rates=propinv;\nPrset statefreqpr=fixed(equal);\n"
	elif model == 'SYM+I+G':
		model_block="Lset nst=6 rates=invgamma;\nPrset statefreqpr=fixed(equal);\n"
	elif model == 'GTR':
		model_block="Lset nst=6 rates=equal;\n"
	elif model == 'GTR+G':
		model_block="Lset nst=6 rates=gamma;\n"
	elif model == 'GTR+I':
		model_block="Lset nst=6 rates=propinv;\n"
	elif model == 'GTR+I+G':
		model_block="Lset nst=6 rates=invgamma;\n"
	else:
		print model
	block_end="mcmc stoprule=yes ngen=100000000 stopval=0.01 samplefreq=1000 printfreq=1000 diagnfreq=10000 nrun=4 nchain=2;\n sump nruns=4;\nsumt nruns=4;\nquit;\nend;\n"		
	block_list=[block_start,model_block,block_end]
	block=''.join(block_list)
	return block
	
def find_model(model_table, root):
	f=file(model_table)
	model=''
	for line in f:
		line=line.strip()
		if root in line:
			model=line.split('\t')[5]	
	return model
		
def out_nex(dict, root,b_block): 
	outfile=str(root)+".mb.nex"
	outp = open(outfile, 'w')
	outp.write("#NEXUS\n Begin data;\n dimensions ntax = " + str(len(dict)) + " nchar = " + str(len(dict.values()[0][0])) + ";\n Format datatype = DNA gap = - missing = ?;\nMatrix\n")
	dict = collections.OrderedDict(sorted(dict.items()))	
	for k, v in dict.iteritems():
		outp.write(str(k) + '\t' + str(v[0]) + '\n')
	outp.write(';\n end;\n\n')
	outp.write(str(b_block)+'\n')
	outp.close()

model_table=sys.argv[1]

for f_name in glob.glob('*.nex'):
	root=f_name.split('.nex')[0]
	data_dict=in_nex(f_name)
	b_block=bayes_block(find_model(model_table,root))
	out_nex(data_dict,root,b_block)
