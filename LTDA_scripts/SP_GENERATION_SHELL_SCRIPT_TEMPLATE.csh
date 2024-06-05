#!/bin/csh

date
srtpath 24.5.12 Linux26SL6_i386_gcc446

which MooseApp
mkdir JOB_DIR
mkdir JOB_DIR/SINGLE_DIGIT
MooseApp JOB_DIR/prepared/JOB_DIR-LEADING_ZEROS.tcl

cp -pr bellis/JOB_DIR/SINGLE_DIGIT /home/bellis/ana54/workdir/scratch/bellis/JOB_DIR/.

rm -r bellis/JOB_DIR/SINGLE_DIGIT
