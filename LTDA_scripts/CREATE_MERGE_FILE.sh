#jobname="bnc_plam2"
jobname="bnv_lam0lam0_00"
ls /home/bellis/ana54/workdir/scratch/bellis/${jobname}/*/Moose.01.root | sed 's/\.01\.root//' > mypath_${jobname}.merge
