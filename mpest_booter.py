#!/usr/bin/python

import os
import re
import sys
import glob
import argparse
import collections


def grab_tree(nrep,locus): #Will grab the tree on the line number for the current rep
	f=open(locus)
	for i, line in enumerate(f):
		if i == nrep:
			return line
	f.close()
	
def write_file(nrep,locus,outp): #Calls the tree grab and writes tree to file
	tree=grab_tree(nrep,locus)
	outp.write(str(tree))
	

def control_file(nrep): # Will write the same control file info with different tree filenames. Another way to do this would be to read in a template and write out to file with the one line changed.
	outf=open(str(nrep)+'.ctr', 'w')
	outf.write(str(nrep)+'.trees\n0\n-1\n429 16\n')
	outf.write('brachymeles_bonitae 1 brachymeles_bonitae\n')
	outf.write('chalcides_ocellatus 1 chalcides_ocellatus\n')
	outf.write('emoia_caeruleocauda 1 emoia_caeruleocauda\n')
	outf.write('eurylepis_taeniolatus 1 eurylepis_taeniolatus\n')
	outf.write('lobulia_elegans 1 lobulia_elegans\n')
	outf.write('lygosoma_brevicaudis 1 lygosoma_brevicaudis\n')
	outf.write('mabuya_unimarginata 1 mabuya_unimarginata\n')
	outf.write('mesoscincus_manguae 1 mesoscincus_manguae\n')
	outf.write('ophiomorus_raithmai 1 ophiomorus_raithmai\n')
	outf.write('plestiodon_fasciatus 1 plestiodon_fasciatus\n')
	outf.write('scincus_scincus 1 scincus_scincus\n')
	outf.write('sphenomorphus_tridigitus 1 sphenomorphus_tridigitus\n')
	outf.write('sphenomorphus_variegatus 1 sphenomorphus_variegatus\n')
	outf.write('typhlosaurus_sp 1 typhlosaurus_sp\n')
	outf.write('tytthoscincus_parvus 1 tytthoscincus_parvus\n')
	outf.write('xantusia_vigilis 1 xantusia_vigilis\n')
	outf.write('0\n')
	outf.close()



for nrep in range(0,1000):
	control_file(nrep)	#Write control file for current boot rep
	outp=open(str(nrep)+'.trees', 'w') #open a file for the current boot rep
	for locus in glob.glob('*.tre'):  # Within each boot rep, open all gene files
		write_file(nrep,locus,outp)	#Call write_file for each locus within the boot rep. The result should be a file with num trees = num loci
