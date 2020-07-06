foreach sp("SP-1005" "SP-11975" "SP-11976" "SP-11977" "SP-1235" "SP-1237" "SP-3429" "SP-9456" "SP-9457" "SP-980" "SP-998")
    #foreach decay ("pmu" "pe" "pnu" "nmu" "ne")
    foreach decay ("pmu" "pe" )
        echo $sp $decay
        python merge_a_bunch_of_dataframes.py $sp"_"$decay"_df.h5" ~/babar_data/cut_summary_files_df/$sp/$decay/*.h5
    end
end
