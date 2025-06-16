subdir='bnv_analysis'
#subdir='bnv_analysis_bnc_mode'
for dir in $@; do
    echo $dir
    # BNV
    outname=$dir"_COMBINED.root"
    # Do this for BNC
    #outname=$dir"_""$subdir""_COMBINED.root"
    echo $outname
    #ls $dir/${subdir}/*.root
    # -k means skip corrupted files. There might be a couple
    # -f forces recreation of the output file
    hadd -f -k $outname $dir/${subdir}/*.root
done
