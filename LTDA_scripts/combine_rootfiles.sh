for dir in $@; do
    echo $dir
    outname=$dir"_COMBINED.root"
    echo $outname
    ls $dir/bnv_analysis/*.root
    # -k means skip corrupted files. There might be a couple
    hadd -k $outname $dir/bnv_analysis/*.root
done
