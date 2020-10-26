#!/usr/bin/env python

# set_up_everything_to_run_BtaTupleMaker.py
# M. Bellis, Aug. 2009

#..Generates tcl snippets for specified tcl files by BbkDatasetTcl. 
#  Modified from perl script written by Chris Hearty

#..For usage, type set_up_everything_to_run_BtaTupleMaker.py -h

import sys
import os
import subprocess
from optparse import OptionParser

################################################################################
# Parse the command line options
################################################################################
myusage = "\n%prog <--data or --mc> --collection <collection name> --tcl-config <tcl config file for BtaTupleMaker> [options] "
parser = OptionParser(usage = myusage)
parser.add_option("-c", "--collection", dest="collection", \
                  help="Collection name (e.g. SP-1235-Run6-R24, LambdaVeryVeryLoose-Run3-OffPeak-R24a2-v03, etc.")
parser.add_option("-t", "--tcl-config",  dest="tcl_config", \
                   help=".tcl file to configure BtaTupleMaker. Note that this MUST be in another directory and will\
                   have a soft link to it created in the workdir.")
parser.add_option("--mc",  dest="mc", action="store_true", default=False, help="Collection which is being processed is Monte Carlo.")
parser.add_option("--data",  dest="data", action="store_true", default=False, help="Collection which is being processed is data.")
"""
parser.add_option("--tcl-dir",  dest="tcl_dir", \
                   help="Separate directory where .tcl files for BtaTupleMaker are kept. If this is set, \
                   a soft link is created to the .tcl file in the workdir. If this is not set, the .tcl file \
                   is assumed to be in the workdir.")
"""
parser.add_option("-l", "--link-directory",  dest="link_directory", \
                   help="For output directories, when they are created, \
                   link them to this directory (e.g. /scratch/myname, /nfs/farm/myAWG/myname/, etc.")

# Parse the options.
(options, args) = parser.parse_args()

# Make sure there are the necessary command line options.
"""
if options.tcl_dir == None:
  parser.print_help()
  parser.error("\nIt is assumed that your BtaTupleMaker .tcl file exists in another directory.\n \
      Please provide that directory name with the --tcl-dir option!\n")
"""

dataset = ""
btm_tclfile = ""
tclfile = ""
tcl_dir = ""
if options.collection == None or options.tcl_config == None:
  parser.print_help()
  parser.error("\nMissing either collection name or tcl-config file!\n")
else:
  dataset = options.collection
  # Grab the name of the .tcl file only from the full path
  btm_tclfile = options.tcl_config.split('/')[-1]
  # Grab the directory in which the .tcl file lives
  tcl_dir = options.tcl_config.partition(btm_tclfile)[0]
  # Check the format of the files.
  if btm_tclfile.rfind('.tcl') < 0:
    print "\nAre you sure your config file for BtaTupleMaker is a .tcl file?\n \
    I can't find the .tcl extension!\n"
    exit(-1)
  else:
    tclfile = btm_tclfile.partition('.tcl')[0]


if (options.mc==True and options.data==True ) or (options.mc==False and options.data==False ):
  parser.print_help()
  parser.error("\nNeed to declare either --data or --mc but not both!\n")

# Check if some of the directories exist
if options.link_directory != None:
  if not os.access(options.link_directory, os.W_OK):
    print "%s does not exist or is not writeable!\n"
    exit(-1)
################################################################################
# Finished with the command line options.
# Should be good to go!
################################################################################


################################################
#..Check working directory
################################################
pwd = os.getcwd().split('/')[-1]
if pwd != "workdir":
  print "Not in a workdir!!!!\n"
  exit(-1)

# Remember our present working directory
pwd = os.getcwd()

# Get username 
username = os.environ["USER"]

################################################
# Hard code a few things
################################################
# Make some top level directories, and link them if necessary.
dirs_to_make = []
dirs_to_make.append("tcl_collections")
dirs_to_make.append("log")
dirs_to_make.append("test_tcl_run_btm")
dirs_to_make.append("tcl_run_btm")
dirs_to_make.append("shell_scripts")
dirs_to_make.append("submission_scripts")
dirs_to_make.append("rootfiles")
dirs_to_make.append("testrootfiles")

for dir in dirs_to_make:
  # Check if directory exists and if not...
  if not os.access( dir, os.W_OK ):
    # ....either make in link directory...
    if options.link_directory != None:
      print "%s does not exist! Will make and link this directory\n" % (dir)
      newlinkdir = "%s/%s" % (options.link_directory,dir)
      if not os.path.exists(newlinkdir):
          os.mkdir(newlinkdir, 0744)
      if not os.path.exists(dir):
          os.symlink(newlinkdir, dir)
    #......or make right in the workdir.
    else:
      print "%s does not exist! Will make this directory\n" % (dir)
      os.mkdir(dir, 0744)

#tcldir = "tcl_collections/" + dataset
#logdir = "log/" + dataset
#testrundir = "test_tcl_run_btm/" + dataset
#rundir = "tcl_run_btm/" + dataset
#shellscriptsdir = "shell_scripts/"  + dataset
#submissiondir = "submission_scripts/" 
#rootfiledir = "rootfiles/" + dataset
#testrootfiledir = "testrootfiles/" + dataset

tcldir = "tcl_collections/" + dataset + "/" + tclfile
logdir = "log/" + dataset + "/" + tclfile
testrundir = "test_tcl_run_btm/" + dataset + "/" + tclfile
rundir = "tcl_run_btm/" + dataset + "/" + tclfile
shellscriptsdir = "shell_scripts/"  + dataset + "/" + tclfile
submissiondir = "submission_scripts/"  + "/" + tclfile
rootfiledir = "rootfiles/" + dataset + "/" + tclfile
testrootfiledir = "testrootfiles/" + dataset + "/" + tclfile

# For running on the farm
#batchworkdir = "/scratch/%s_%s_%s" % ( username, tclfile , dataset )
# Don't need the scratch for LTDA
batchworkdir = "%s_%s_%s" % ( username, tclfile , dataset )

################################################
# Check to see if all the directories are writable
################################################
if not os.access(tcldir,os.W_OK):
  print tcldir + " does not exist!\n"
  print "Will make directory.\n"
  idx = tcldir.rfind('/')
  os.mkdir(tcldir[0:idx], 0744)
  os.mkdir(tcldir, 0744)
if not os.access(logdir,os.W_OK):
  print logdir + " does not exist!\n"
  print "Will make directory.\n"
  idx = logdir.rfind('/')
  os.mkdir(logdir[0:idx], 0744)
  os.mkdir(logdir, 0744)
if not os.access(rundir,os.W_OK):
  print rundir + " does not exist!\n"
  print "Will make directory.\n"
  idx = rundir.rfind('/')
  os.mkdir(rundir[0:idx], 0744)
  os.mkdir(rundir, 0744)
if not os.access(testrundir,os.W_OK):
  print testrundir + " does not exist!\n"
  print "Will make directory.\n"
  idx = testrundir.rfind('/')
  os.mkdir(testrundir[0:idx], 0744)
  os.mkdir(testrundir, 0744)
if not os.access(shellscriptsdir,os.W_OK):
  print shellscriptsdir + " does not exist!\n"
  print "Will make directory.\n"
  idx = shellscriptsdir.rfind('/')
  os.mkdir(shellscriptsdir[0:idx], 0744)
  os.mkdir(shellscriptsdir, 0744)
if not os.access(submissiondir,os.W_OK):
  print submissiondir + " does not exist!\n"
  print "Will make directory.\n"
  idx = submissiondir.rfind('/')
  os.mkdir(submissiondir[0:idx], 0744)
  os.mkdir(submissiondir, 0744)
if not os.access(rootfiledir,os.W_OK):
  print rootfiledir + " does not exist!\n"
  print "Will make directory.\n"
  idx = rootfiledir.rfind('/')
  os.mkdir(rootfiledir[0:idx], 0744)
  os.mkdir(rootfiledir, 0744)
if not os.access(testrootfiledir,os.W_OK):
  print testrootfiledir + " does not exist!\n"
  print "Will make directory.\n"
  idx = testrootfiledir.rfind('/')
  os.mkdir(testrootfiledir[0:idx], 0744)
  os.mkdir(testrootfiledir, 0744)

################################################
# Some options for the tcl snippets
################################################
ConfigPatch = "Run2"
if options.mc == True:
  ConfigPatch = "MC"
elif options.data == True:
  ConfigPatch = "Run2"
else:
  print "Something is messed up with the data/mc options!!!\n"
  exit(-1)

################################################
# Set up the .tcl file for BtaTupleMaker with 
# the proper links.
################################################
# Make sure directory with .tcl files and the file exists.
if not os.access(options.tcl_config, os.F_OK):
  print "%s doesn't exist!\n" % (options.tcl_config)
  sys.exit(-1)

# Remove the old file
if os.access(btm_tclfile, os.F_OK):
  os.remove(btm_tclfile)

# Create a soft link to the .tcl file
os.symlink(options.tcl_config, btm_tclfile)


"""
if os.access(home + "/tclFiles/"+btm_tclfile, os.F_OK):
  os.symlink(home + "/tclFiles/"+btm_tclfile, btm_tclfile)
else: 
  print home + "/tclFiles/"+btm_tclfile + " doesn't exist!\n"
  sys.exit(-1)
"""

################################################
# Make the tcl files with the collection information
################################################
os.chdir('tcl_collections')
os.chdir(dataset)
# Bellis addition!!!!
os.chdir(tclfile)

# Run the commands to grab the collection information.
cmd = ['BbkDatasetTcl', '-t', '-ds', dataset, '--dbname', 'bbkr24', '--dbsite','slac','--basename',  'info-'+dataset]
subprocess.Popen(cmd,0).wait()
if options.collection.find("1197")>=0 or options.collection.find("945")>=0:
	cmd = ['BbkDatasetTcl', '-t', '10k', '-ds', dataset, '--dbname', 'bbkr24', '--dbsite','slac','--splitruns']
else:
	cmd = ['BbkDatasetTcl', '-t', '100k', '-ds', dataset, '--dbname', 'bbkr24', '--dbsite','slac','--splitruns']
	#cmd = ['BbkDatasetTcl', '-t', '1M', '-ds', dataset, '--dbname', 'bbkr24', '--dbsite','slac','--splitruns']
subprocess.Popen(cmd,0).wait()

print "\n"

################################################################################
#..Make the tcl snippets and write a line per file to the batch submit 
#  script. Skip any input files that don't end in .tcl
################################################################################
print "About to make the tcl snippets for the batch system..."
list_of_runfiles = []
list_of_rootfiles = []
os.chdir(pwd)
#print os.getcwd()
input_files = os.listdir(tcldir)
# Get list of collections
collection_files = os.listdir(tcldir)
# If there is an "info-XXX" in the list then delete it
for file in collection_files:
  if file.find("info") > -1:
    collection_files.remove(file)


print "Hi==========================="
print collection_files
for file in collection_files:
  if file.startswith(dataset) and file.endswith('.tcl'):
    tempname = tcldir + "/" + file
    print tempname
    #runfilename = rundir+"/"+"run_"+tclfile+ "-" + file
    runfilename = rundir+"/"+"run_"+file
    print runfilename
    runfile = open(runfilename, "w+")
    runfile.write("#..See Analysis.tcl for description of FwkCfgVars.\n")
    runfile.write("sourceFoundFile " + tempname + "\n")
    runfile.write("set ConfigPatch \"" + ConfigPatch + "\"\n")
    runfile.write("set FilterOnTag \"false\"\n") 
    runfile.write("set BetaMiniTuple \"root\"\n")
    rootfile = "default.root"
    if file.endswith('.tcl'):
        #rootfile =   tclfile+ "-" + file[:-len('.tcl')] + ".root"
        rootfile =   file[:-len('.tcl')] + ".root"
    list_of_rootfiles.append(rootfile)
    #runfile.write("set histFileName " + rootfiledir + "/" + rootfile + "\n")
    runfile.write("set histFileName " + batchworkdir + "/" + rootfile + "\n")
    runfile.write("set NEvents 0\n")
    runfile.write("sourceFoundFile " + tclfile + ".tcl\n")
    runfile.close()
    os.chmod(runfilename, 0744)
    list_of_runfiles.append(runfilename)

print "\n"

################################################################################
# Make the one tcl snippet to run BtaTupleMaker interactively.
################################################################################
one_test_file_name = ""
print "About to make a test file for this setup to run interactively..."
for file in collection_files:
  if file.startswith(dataset) and file.endswith('.tcl'):
    tempname = tcldir + "/" + file
    #print tempname
    #testrunfilename = testrundir+"/"+"run_"+tclfile+ "-" + file
    testrunfilename = testrundir+"/"+"run_"+ file
    one_test_file_name = testrunfilename
    testrunfile = open(testrunfilename, "w+")
    testrunfile.write("#..See Analysis.tcl for description of FwkCfgVars.\n")
    testrunfile.write("sourceFoundFile " + tempname + "\n")
    testrunfile.write("set ConfigPatch \"" + ConfigPatch + "\"\n")
    testrunfile.write("set FilterOnTag \"false\"\n") 
    testrunfile.write("set BetaMiniTuple \"root\"\n")
    rootfile = "default.root"
    if file.endswith('.tcl'):
        #rootfile =   tclfile+ "-" + file[:-len('.tcl')] + ".root"
        rootfile =   file[:-len('.tcl')] + ".root"
    list_of_rootfiles.append(rootfile)
    #testrunfile.write("set histFileName " + rootfiledir + "/" + rootfile + "\n")
    testrunfile.write("set histFileName " + testrootfiledir + "/" + rootfile + "\n")
    testrunfile.write("set NEvents 1000\n")
    testrunfile.write("sourceFoundFile " + tclfile + ".tcl\n")
    testrunfile.close()
    os.chmod(testrunfilename, 0744)
    break

print one_test_file_name


print "\n"

################################################
#..Make the shell scripts and write a line per file to the batch submit 
#  script. Skip any input files that don't end in .tcl
################################################
print "About to make the shell scripts for the batch system..."
list_of_shellscripts = []
os.chdir(pwd)
#print os.getcwd()
#list_of_runfiles = os.listdir(rundir)
print "HERE ---------------------------------"
print list_of_runfiles
for i,file in enumerate(list_of_runfiles):
  #tcl_run_btm/SP-11975-R24/basicPID_pi0_R24/run_basicPID_pi0_R24-SP-11975-R24-24.tcl
  #if file.startswith("tcl_run_btm/" + dataset + '/' + tclfile + "/run_" + tclfile) and file.endswith('.tcl'):
  if file.startswith("tcl_run_btm/" + dataset + '/' + tclfile + "/run_") and file.endswith('.tcl'):
    #tempname = tcldir + "/" + file
    #print tempname
    #filename = shellscriptsdir+"/" + tclfile+ "-" + collection_files[i] + ".sh"
    filename = shellscriptsdir+"/" + collection_files[i] + ".sh"
    print filename
    shellscript = open(filename, "w+")
    shellscript.write("#!/bin/csh\n\n")
    shellscript.write("date\n")
    shellscript.write("mkdir -p " + batchworkdir + "\n")
    shellscript.write("ls -l " + batchworkdir + "\n")
    shellscript.write("which BtaTupleApp\n")
    #shellscript.write("../bin/$BFARCH/BtaTupleApp " + file + "\n")
    # Just need this for running on LTDA
    shellscript.write("BtaTupleApp " + file + "\n")
    shellscript.write("echo Ran to completion\n")
    shellscript.write("# What's in the directory\n")
    shellscript.write("ls -ltr " + batchworkdir + "\n")

    # Skimming scripts
    shellscript.write("bbrroot -l -q -b \'copytree3_modified.C(\"" + batchworkdir + "/" + list_of_rootfiles[i] + "\")\'\n")
    # SP-11975
    #shellscript.write("bbrroot -l -q -b \'copytree3_require_proton.C(\"" + batchworkdir + "/" + list_of_rootfiles[i] + "\")\'\n")
    # SP-11976
    #shellscript.write("bbrroot -l -q -b \'copytree3_require_muon.C(\"" + batchworkdir + "/" + list_of_rootfiles[i] + "\")\'\n")
    # SP-11977
    #shellscript.write("bbrroot -l -q -b \'copytree3_require_electron.C(\"" + batchworkdir + "/" + list_of_rootfiles[i] + "\")\'\n")

    shellscript.write("# Copy over the files\n")
    #shellscript.write("cp -p " + batchworkdir + "/" + list_of_rootfiles[i] + " " + rootfiledir + "/.\n")
    shellscript.write("cp -p " + batchworkdir + "/" + list_of_rootfiles[i].split(".root")[0] + "_SKIMMED.root " + rootfiledir + "/.\n")
    #shellscript.write("cp -p " + batchworkdir + "/*.root " + rootfiledir + "/.\n")
    #shellscript.write("ls -l " + rootfiledir + "/" + list_of_rootfiles[i] + "\n")
    #shellscript.write("ls -l " + rootfiledir + "/*.root" + "\n")
    shellscript.write("# Clean up the files\n")
    #shellscript.write("rm -r " + batchworkdir + "/" + list_of_rootfiles[i].split(".root")[0] + "*.root\n")
    #shellscript.write("rm -r " + batchworkdir + "/*.root" + "\n")

    shellscript.close()
    os.chmod(filename, 0744)
    list_of_shellscripts.append(filename)

print "\n"

################################################
#..Create the script name to submit all the jobs.
################################################
script_name = submissiondir + "/sub_" + dataset + "-" + tclfile + ".sh"
script = open(script_name, "w+")
script.write('#!/bin/sh -f\n')
for file in list_of_shellscripts:
  #output = "bsub -W 06:00 -q long -o " + logdir + "/" + file.split('/')[-1] + ".log" + " " + file + "\n"
  # Need this part to run on LTDA with SL5
  output = "bsub -W 06:00  -l other=SL5 -o " + logdir + "/" + file.split('/')[-1] + ".log" + " " + file + "\n"
  #output = "bsub -q long -o " + logdir + "/" + file.split('/')[-1] + ".log" + " ../bin/$BFARCH/BtaTupleApp " + file + "\n"
  script.write(output)

script.close()
os.chmod(script_name, 0744)

print script_name


#############################################################
# Give the user a sample command
#############################################################
print "\n-------------------------------------\n"
print "Sweet!\n"
print "This script ran to completion and hopefully set you up to do an awesome analysis."
print "To test it out, you can run BtaTupleMaker interactively."
print "\n[yakunoric13] \x1b[32m%s %s\x1b[0m \n" % ("BtaTupleApp", one_test_file_name)
print "This will run over only 1000 events from this collection and put the output in \x1b[32m%s\x1b[0m\n" % (testrootfiledir)
print "Have fun and do good science.\n"
