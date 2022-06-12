for sp in 'pmu' 'pe' 'nmu' 'ne' 'pnu'  
do
    echo "${sp} -------"
    python count_events_simplified.py CUT_SUMMARY_SP-*"${sp}".h5
done
