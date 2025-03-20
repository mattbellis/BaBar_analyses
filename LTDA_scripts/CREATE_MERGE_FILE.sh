jobname="bnc_plam"
ls /home/bellis/ana54/workdir/scratch/bellis/${jobname}/*/Moose.01.root | sed 's/\.01\.root//' > mypath_${jobname}.merge
