#foreach sp("SP-1005" "SP-11975" "SP-11976" "SP-11977" "SP-1235" "SP-1237" "SP-3429" "SP-9456" "SP-9457" "SP-980" "SP-998" "SP-2400" "SP-3981")
#foreach sp("SP-2400" "SP-3981")
#foreach sp("SP-998")
#foreach sp("SP-11975" "SP-11976" "SP-11977" "SP-9456" "SP-9457" "SP-980" )
#foreach sp("SP-9456"  )
foreach sp( AllEvents-Run1-OnPeak-R24 AllEvents-Run2-OnPeak-R24 AllEvents-Run3-OnPeak-R24 AllEvents-Run4-OnPeak-R24 AllEvents-Run5-OnPeak-R24 AllEvents-Run6-OnPeak-R24 )
    foreach decay ("pmu" "pe" "pnu" "nmu" "ne")
    #foreach decay ("pmu" )
        echo $sp $decay
#python merge_a_bunch_of_dataframes.py $sp"_"$decay"_df.h5" ~/babar_data/cut_summary_files_df/$sp/$decay/*.h5
        python merge_a_bunch_of_dataframes.py /qnap/mbellis/bellis/BaBar/rootfiles/cut_summary_files_df/$sp/$decay/*.h5
    end
end
