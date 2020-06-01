import numpy as np
import subprocess as sp

import os
import sys

###############################################################################
def write_output_file(inputfiles, tag, batchfilename, kinvars=None, decay='plot'):

    output = ""
    output += "#!/bin/bash -l\n"
    output += "#$ -cwd\n"
    output += "#$ -V\n"
    output += "#$ -N bellis_%s\n" % (tag)
    output += "#$ -j y\n"
    output += "#$ -o hpc_script_logs/bellis_$JOB_ID_{0}_{1}.log\n".format(tag,decay)
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
    if kinvars=='plot':
        files_string = " ".join(inputfiles)
        output += "cd /home/mbellis/BaBar_analyses/BNV_search/ \n"
        output += "python plot_KINVAR_files_missing_particle.py \\\n"
        output += "\t{0} --decay {1}\n".format(files_string,decay)
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
        #if file.find('SKIMMED.root')>=0:
        if file.find('SKIMMED')>=0:
            file = "{0}/{1}".format(topdir,file)
            infiles.append(file)
            #print("REMOVING: ",file)
            #infiles.remove(file)
    #print(infiles)
    #exit()
    #infiles = sys.argv[1:]

    mastertag = "babar"

    nfiles_at_a_time = 10

    tot_files = 0

    for i in range(0,len(infiles),nfiles_at_a_time):
        
        subset = infiles[i:i+nfiles_at_a_time]
        tot_files += len(subset) # Maybe bail at some point
        print(subset)

        infile_tag = subset[0].split('/')[-1].split(',root')[0]

        tag = "{0}_{1}".format(mastertag,infile_tag)

        batchfilename = "hpc_scripts/batch_%s.sh" % (tag)

        ########################################
        # Yes plot the kinvars, or at least build the pickle files
        ########################################
        #'''
        for d in ['pmu', 'pe', 'pnu', 'nmu', 'ne']:
        #for d in ['ne']:
            if subset[0].find(d)<0:
                continue
            print(d)
            tag = "{0}_{1}_{2}".format(mastertag,infile_tag,d)
            batchfilename = "hpc_scripts/batch_{0}.sh".format(tag)
            write_output_file(subset,tag,batchfilename,kinvars='plot',decay=d)
            print(batchfilename)
            cmd = ['qsub', batchfilename]
            print(cmd)
            print(subset)
            sp.Popen(cmd,0).wait()

        if tot_files>=100:
            break
        #'''

################################################################################
################################################################################
if __name__=='__main__':
	main()
