import re
import glob

def parse_fasta(inp):
	"""Takes a fasta file, separates label and sequence."""
	identifiers = []
	sequences = []
	current_seq = []
	dict = {}
	
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
		if name in dict:
			dict[name].append(sequences[n])
		else:
			dict[name] = [sequences[n]]
	return dict
			
def output_phy(dict, root):
	outfile=str(root)+".phy"	#Create a new file to be written to. 
	outp=open(outfile, 'w')		#Open new file
	keys=dict.keys()			
	keys.sort()					#Organize sequences names alphabetically
	values=dict.values()	
	ntax=len(keys)				#Capture the number of taxa
	seq_length=len(values[0][0])	#Capture the length of the sequences
	outp.write(str(ntax)+' '+str(seq_length)+'\n')	#Write ntax and seq length to phylip file
	for element in keys:
		for k, v in dict.iteritems():
			if k==element:
				outp.write(str(k)+'\t'+str(v[0])+'\n')	#Write taxon names and sequences to file


for element in glob.glob("*.fasta"):  #Read in all files in folder with .fasta ending
	filename=element					#Assign filename to variable filename
	file_split=filename.split('.')		#Split the filename by "."
	root_name=file_split[0]				#Use the first part of the filename as the root_name
	f=file(filename)					#Open the file
	output_phy(parse_fasta(f),root_name)	#Send file info to function parse_fasta and then run that dictionary through output_phy
