
#Convert Nexus to fasta

import glob
import sys

for name in glob.glob('*.nex'):
	name_root=name.split('.nex')
	out_file=str(name_root[0])+'.fasta'
	outp=open(out_file, 'w')
	data=[]
	f=file(name)
	for line in f:
		data.append(line)
	data=''.join(data)
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
	for element in matrix_list:
		new_element=element.split()
		outp.write('>'+str(new_element[0])+'\n'+str(new_element[1])+'\n')