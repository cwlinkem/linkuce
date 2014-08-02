import os
import glob
import subprocess

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

def run_jmodeltest(name):
	jmodel_proc=subprocess.Popen('java -jar ~/phylo_tools/jmodeltest-2.1.5/jModelTest.jar -d '+str(name)+' -s 3 -f -i -g 4 -BIC -c 0.95 > '+str(name)+'.results.txt', shell=True, executable='/bin/bash')
	jmodel_proc.wait()

def get_models(f, gene_name, out):
	fl=file(f)
	for line in fl:
		line=line.strip()
		if "the 95% confidence interval" in line:
			model=line.split(': ')[1]
			out.write(str(gene_name)+'\t'+str(model)+'\n')


def main():
	for f in glob.glob('*.nex'):
		run_jmodeltest(f)

	out=open('models.txt','w')
	for f in glob.glob('*.results.txt'):
		gene_name=f.split('.')[0]
		get_models(f, gene_name,out)


'''	description = ('This program will run jModelTest on a single file or set '
					'of files in nexus format. User can choose the set of models'
					'and type of summary using flags. The standard 24 models used'
					'in MrBayes and BIC summary with 95% credible set are defaults.')
	FILE_FORMATS = ['nex']
	parser = argparse.ArgumentParser(description = description)
	parser.add_argument('input_files', metavar='INPUT-SEQ-FILE',
		nargs = '+',
		type = arg_is_file,
		help = ('Input sequence file(s) name '))
	parser.add_argument('-o', '--out-format',
		type = str,
		choices = ['nex', 'fasta', 'phy'],
		help = ('The format of the output sequence file(s). Valid options '))
	parser.add_argument('-j', '--path-to-jModelTest',
		type = str,
		help=('The full path to the jModelTest executable'))
	parser.add_argument('-s', '--substitution-models',
		type = str,
		choices = ['3','5','7','11']
		default = ['3']
		help = ('Number of substitution schemes to test. Default is all GTR models "-s 3".'))
	parser.add_argument('-g', '--gamma',
		type = str,
		default = ['4']
		help = ('Include models with rate variation among sites and number of categories (e.g., -g 8)'))
	parser.add_argument('-i', '--invar',
		type = str,
		default = ['false']
		help = ('include models with a proportion invariable sites (e.g., -i)')) 

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
			out_phy(dict, filename)'''
			
			

if __name__ == '__main__':
	main()