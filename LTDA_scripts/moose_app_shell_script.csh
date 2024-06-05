#!/bin/csh

date
srtpath 24.5.12 Linux26SL6_i386_gcc446

which MooseApp

mkdir bellis
mkdir bellis/"$1"
rm -rf bellis/"$1"/$2
mkdir bellis/"$1"/$2

MooseApp /home/bellis/ana54/workdir/"$1"/prepared/"$1"-"$3".tcl

ls -ltr bellis
echo
ls -ltr bellis/"$1"
echo
ls -ltr bellis/"$1"/$2
echo

rm -rf /home/bellis/ana54/workdir/scratch/bellis/"$1"/$2
mkdir /home/bellis/ana54/workdir/scratch/bellis
mkdir /home/bellis/ana54/workdir/scratch/bellis/"$1"
cp -pr bellis/"$1"/$2 /home/bellis/ana54/workdir/scratch/bellis/"$1"/.

rm -r bellis/"$1"/$2
