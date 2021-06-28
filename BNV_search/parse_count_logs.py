import numpy as np
import sys

infilename = sys.argv[1]

infile = open(infilename,'r')

counts = {}
decays = ['pmu', 'pe', 'pnu', 'nmu', 'ne']
for decay in decays:
    counts[decay] = {}

for line in infile:
    if line.find('Total')>=0:

        #print(line)
        vals = line.split()
        decay = vals[1].split('/')[1]
        sp = vals[0]
        num = int(vals[3])
        #print(decay)

        counts[decay][sp] = num

#print(counts)


output = ""
for decay in decays:
    output += "# {0}\n".format(decay)
    for sp in counts[decay].keys():

        datatype = 'MC'
        if sp.find('Run')>=0:
            datatype = 'DATA'

        num = counts[decay][sp]

        output += 'event_numbers["{3}"]["{0}"]["{1}"]["cuts1"] = {2:d}\n'.format(decay,sp,num,datatype)
        ##print(decay,sp,)
print(output)
