for dir in $@; do
    echo $dir
    outname=$dir"_COMBINED.root"
    echo $outname
    ls $dir/bnv_analysis/*.root
    hadd $outname $dir/bnv_analysis/*.root
done
