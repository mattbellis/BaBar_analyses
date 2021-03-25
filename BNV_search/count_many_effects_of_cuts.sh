#TMPFILE="COUNTS_TEMP.tmp"
#date > $TMPFILE
#
#
##for decay in  'pmu' 
#for decay in 'pmu' 'pe' 'pnu' 'nmu' 'ne'
#do
#
    #echo $decay 
#
    #if [[ $decay == 'nmu' || $decay == 'pnu' ]]
    #then
        #python count_number_remaining_after_some_cuts.py CUT_SUMMARY_*"$decay".h5 CUT_SUMMARY_*"$decay"*B*.h5 >> $TMPFILE
    #else
        #python count_number_remaining_after_some_cuts.py CUT_SUMMARY_*"$decay".h5  >> $TMPFILE
    #fi
#done


python count_number_remaining_after_some_cuts.py CUT_SUMMARY_*pmu.h5 CUT_SUMMARY_*pe.h5 CUT_SUMMARY_*ne.h5 CUT_SUMMARY_*nmu.h5 CUT_SUMMARY_*nmu*B*.h5 CUT_SUMMARY_*pnu.h5 CUT_SUMMARY_*pnu*B*.h5
