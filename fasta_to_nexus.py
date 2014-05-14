#! 

import sys


def parse_sequence_fasta(inp):
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





if len(sys.argv) != 3:
	sys.exit(sys.argv[0] + ": Expecting two command line arguments -- a fasta file and a nexus output file")
fasta_file = sys.argv[1]
nexus_file = sys.argv[2]

inp = open(fasta_file, 'rU')
outp = open(nexus_file, 'w')

read_fasta = parse_sequence_fasta(inp)

seq_list = []
for i in read_fasta[1][0]:
	seq_list.append(i)


outp.write("#NEXUS\n Begin data;\n dimensions ntax = " + str(len(read_fasta[0])) + " nchar = " + str(len(seq_list)) + ";\n Format datatype = DNA gap = - missing = ?;\nMatrix\n")
for n, element in enumerate(read_fasta[0]):
	outp.write(element + '\t' + read_fasta[1][n] + '\n')
outp.write(';\n end;')


