#!/usr/bin/python

import os
import re
import sys
import glob
import argparse
import collections

def find_best(rep): #Will find the line in mpest output that is the best tree (Last tree in file)
	f=file(rep)
	for line in f:
		if 'tree mpest' in line:
			tree=line.split(' = ')[1]
	return tree

n=0 
out_con=open('mpest_boots.tre', 'w')					#Open file for best trees to be written to
out_con.write('#nexus\nBegin trees;\n\ttranslate\n')    #Tree block, could also be captured from one tree file
out_con.write('1 brachymeles_bonitae,\n')
out_con.write('2 chalcides_ocellatus,\n')
out_con.write('3 emoia_caeruleocauda,\n')
out_con.write('4 eurylepis_taeniolatus,\n')
out_con.write('5 lobulia_elegans,\n')
out_con.write('6 lygosoma_brevicaudis,\n')
out_con.write('7 mabuya_unimarginata,\n')
out_con.write('8 mesoscincus_manguae,\n')
out_con.write('9 ophiomorus_raithmai,\n')
out_con.write('10 plestiodon_fasciatus,\n')
out_con.write('11 scincus_scincus,\n')
out_con.write('12 sphenomorphus_tridigitus,\n')
out_con.write('13 sphenomorphus_variegatus,\n')
out_con.write('14 typhlosaurus_sp,\n')
out_con.write('15 tytthoscincus_parvus,\n')
out_con.write('16 xantusia_vigilis;\n')
for rep in glob.glob('*.trees.tre'):           #reads across the mpest output files labeled with trees.tre 
	n += 1									   #Keeps track of tree number
	tree=find_best(rep)						   #Calls find_best function and finds tree
	out_con.write('tree '+str(n)+' = '+str(tree)) #Write tree to file
out_con.write('end;')
out_con.close()
