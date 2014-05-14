#!/usr/local/bin python
import subprocess
import sys
import re

file_name=sys.argv[1]
f=file(file_name)

charset_list=[]
for line in f:
	line=line.strip()
	if 'CHARSET' in line:
		l_split=line.split(' ')
		charset_name=l_split[1]
		charset_list.append(charset_name)
print charset_list	

for element in charset_list:
	paup_proc = subprocess.Popen(['paup'], 
                            stdout=subprocess.PIPE,
                           	stderr=subprocess.PIPE,
                          	stdin=subprocess.PIPE)
	paup_proc.communicate("execute "+str(file_name)+"; exclude all; include "+str(element)+"; export file="+str(element)+".nex format=nex; quit;")
	paup_proc.wait()
print "Your files are now ready."