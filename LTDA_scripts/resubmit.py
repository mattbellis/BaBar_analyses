import sys
import os
import subprocess

infilename = sys.argv[1]
infile = open(infilename)

count = 0

for line in infile:
	vals = line.split()
	if len(vals)==8:
		#print(line)
		#print(vals)
		stub = vals[-1].split('shell_scripts/')[-1].split('.tcl.sh')[0]
		#print(stub)
		rootfile = 'rootfiles/{0}_SKIMMED.root'.format(stub)
		flag = os.path.isfile(rootfile)
		#print(flag)
		#exit()
		if not flag:
			cmd = vals
			if vals[0][0] == "#":
				vals[0] = vals[0][1:]
			#print(cmd)
			print(line)
			if count>=0:
				#1
				subprocess.Popen(cmd,0).wait()
			count += 1
	if count>=10000:
		exit()

print("count: ",count)
			
