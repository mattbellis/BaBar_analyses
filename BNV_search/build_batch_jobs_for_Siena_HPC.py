import numpy as np
import subprocess as sp

import os
import sys

###############################################################################
def write_output_file(infile, tag, batchfilename):

    output = ""
    output += "#!/bin/bash -l\n"
    output += "#$ -cwd\n"
    output += "#$ -V\n"
    output += "#$ -N bellis_%s\n" % (tag)
    output += "#$ -j y\n"
    output += "#$ -o hpc_script_logs/bellis_$JOB_ID_%s.log\n"% (tag)
    output += "#$ -q sos.q\n"
    #output += "#$ -q allsmp.q\n"
    output += "\n"
    output += "# To run the simulation do from the command line:\n"
    output += "# qsub <thisfilename>\n"
    output += "\n"
    #output += "source /etc/profile.d/modules.sh\n"
    output += "\n"
    output += "module load modules GNUStack/cmake\n"
    output += "module load GNUCompiler\n"
    output += "module load Python3\n"
    output += "export PYTHONPATH=/usr/local/anaconda3/lib:$PYTHONPATH\n"
    output += "export LD_LIBRARY_PATH=/usr/local/anaconda3/lib:/usr/local/gcc-6.3.0/lib64/:$LD_LIBRARY_PATH\n"
    output += "\n"
    output += "# REMINDER! This is all in bash\n"
    output += "\n"
    output += "date\n"
    output += "echo $SHELL\n"
    output += "\n"
    output += "pwd\n"
    output += "\n"
    output += "tag=\"%s\"\n" % (tag)
    output += "\n"
    #output += "outputfilename=$tag\"_\"$infile1_tag\"_\"$infile2_tag\"_ranges_\"$range1\"_\"$range2\".dat\"\n"
    output += "\n"
    #output += "echo \"outputfile: \" $outputfilename\n"
    output += "\n"
    output += "cd /home/mbellis/BaBar_analyses/BNV_search/ \n"
    output += "python dump_ROOT_files_based_on_PID_assignments.py \\\n"
    output += "\t{0}\n".format(infile)
    output += "\n"
    output += "date \n"
    output += " \n"
    output += "echo \"Job $JOB_ID is complete.\" | sendmail mbellis@siena.edu \n"

    #print output

    outfile = open(batchfilename,'w')
    outfile.write(output)
    outfile.close()



################################################################################
# Main function
################################################################################
def main():

    topdir = sys.argv[1]
    infiles = []
    infilestemp = os.listdir(topdir)
    for file in infilestemp:
        if file.find('SKIMMED.root')>=0:
            file = "{0}/{1}".format(topdir,file)
            infiles.append(file)
            #print("REMOVING: ",file)
            #infiles.remove(file)
    print(infiles)
    #exit()
    #infiles = sys.argv[1:]

    mastertag = "babar"

    for infile in infiles:

        infile_tag = infile.split('/')[-1].split(',root')[0]

        tag = "{0}_{1}".format(mastertag,infile_tag)

        batchfilename = "hpc_scripts/batch_%s.sh" % (tag)

        write_output_file(infile,tag,batchfilename)
        
        print(batchfilename)

        cmd = ['qsub', batchfilename]
        print(cmd)

        sp.Popen(cmd,0).wait()

################################################################################
################################################################################
if __name__=='__main__':
	main()
