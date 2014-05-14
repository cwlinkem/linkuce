#! 

import sys
import csv
import glob
import collections

def parse_sequence_fasta(inp):
	"""Takes a fasta file, separates label and sequence."""
	identifiers = []
	sequences = []
	current_seq = []
	data_dict = {}
	
	for line in inp:
		stripped = line.strip()
		if line.startswith('>'):
			if current_seq:
				sequences.append(''.join(current_seq))
			identifiers.append(stripped[1:])
			current_seq = []
		else:
			if stripped:
				current_seq.append(stripped)

	if current_seq:
		sequences.append(''.join(current_seq))
 	
	assert(len(identifiers) == len(sequences))

	for n, name in enumerate(identifiers):
		if name in data_dict:
			data_dict[name].append(sequences[n])
		else:
			data_dict[name] = [sequences[n]]
	return data_dict
	


def seq_length_counter(dict):
	value = dict.values()
	current_seq_length = len(value[0][0])
	return current_seq_length


def master_combiner(combined_dict):
	master_dict = {}
	gene_len = []
	total_len = 0
	missing_previous_data = []
	missing_current_data = []
	for gene, data in enumerate(combined_dict):
#		print gene, data
		seq_length = seq_length_counter(data)
		gene_len.append(seq_length)
		missing = '?'*seq_length
		missing_prev = '?'*total_len
		for name, seq in data.iteritems():
#			print name
			if name not in master_dict:
#				print "new"
				master_dict[name] = missing_prev
			master_dict[name] = master_dict[name] + seq[0]
		for name, seq in master_dict.iteritems():
#			print name
			if name not in data:
#				print "missing"
				master_dict[name] = master_dict[name] + missing
		total_len += seq_length
	master_dict = collections.OrderedDict(sorted(master_dict.items()))	
	return master_dict, gene_len


def fasta_to_nexus(inp):
	"""Takes a fasta file, pulls out GI and TI numbers and sequence."""
	identifiers = []
	sequences = []
	current_seq = []
	x = {}
	for line in inp:
		stripped = line.strip()
		if line.startswith('>'):
			if current_seq:
				sequences.append(''.join(current_seq))
			identifiers.append(stripped[1:])
			current_seq = []
		else:
			if stripped:
				current_seq.append(stripped)

	if current_seq:
		sequences.append(''.join(current_seq))
 	
	assert(len(identifiers) == len(sequences))


	return identifiers, sequences

if len(sys.argv) != 2:
	sys.exit(sys.argv[0] + ": Expecting one command line argument -- name of output file root")
list_of_files = sys.argv[1]




combined_dict = []
file_list = []
output_file = str(sys.argv[1]) + '.concat.fa'
output_stream = open(output_file, 'w')

for name in glob.glob("*.fasta"):
	fasta_file = file(name)
	file_list.append(name)
	read_fasta = parse_sequence_fasta(fasta_file)
	combined_dict.append(read_fasta)

combine = master_combiner(combined_dict)

concat_dict = combine[0]
charset_len = combine[1]

"""Output fasta file"""
for k, v in concat_dict.iteritems():
	name_string = '>' + str(k)
	output_stream.write(name_string + '\n' + v + '\n')
output_stream.close()


"""output nexus file"""
nexus_file = str(sys.argv[1]) + '.concat.nex'
outp = open(nexus_file, 'w')
fasta_inp = open(output_file, 'rU')
read_fasta = fasta_to_nexus(fasta_inp)
seq_list = []
for i in read_fasta[1][0]:
	seq_list.append(i)
outp.write("#NEXUS\n Begin data;\n dimensions ntax = " + str(len(read_fasta[0])) + " nchar = " + str(len(seq_list)) + ";\n Format datatype = DNA gap = - missing = ?;\nMatrix\n")
for n, element in enumerate(read_fasta[0]):
	outp.write(element + '\t' + read_fasta[1][n] + '\n')
outp.write(';\n end;\n\n')

outp.write("Begin Assumptions;\n")

previous_len = 1
total_len = 0
for n, seq in enumerate(charset_len):
	total_len += seq
	outp.write('CHARSET ' + str(file_list[n]) + ' = ' + str(previous_len) + '-' + str(total_len) + ';\n')
	previous_len += seq 
outp.write('end;\n\n')