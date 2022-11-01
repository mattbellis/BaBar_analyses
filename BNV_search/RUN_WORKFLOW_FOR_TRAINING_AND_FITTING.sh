channel=$1
step=$2

if [[ $channel -eq "nmu" ]] 
then

    if [[ $step -eq "prepare_samples" ]] 
    then

    ################################################################################
    # For nmu
    ################################################################################
    #   12574889
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-1005_nmu.h5     30000 # 
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-1235_nmu.h5     20000 #   7501598
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-1237_nmu.h5     20000 #   6544351
    #python random_sample_from_dataframe.py CUT_SUMMARY_SP-2400_nmu.h5     50000 #   163
    #python random_sample_from_dataframe.py CUT_SUMMARY_SP-3429_nmu.h5     50000 #   10003071
    #python random_sample_from_dataframe.py CUT_SUMMARY_SP-3981_nmu.h5     50000 #   44506
    #python random_sample_from_dataframe.py CUT_SUMMARY_SP-980_nmu.h5      50000 #   14350
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-998_nmu.h5      15000 #   10005650

    # There are 1230535 entries in the signal
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-11976_nmu.h5 50000

    # Do this for data for Run 1 to apply the cuts
    python random_sample_from_dataframe.py CUT_SUMMARY_AllEvents-Run1_nmu.h5 100000000



    # Now merge them
    python merge_training_samples.py MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-1005_nmu_SAMPLE_N_30000.h5 CUT_SUMMARY_SP-1235_nmu_SAMPLE_N_20000.h5 CUT_SUMMARY_SP-1237_nmu_SAMPLE_N_20000.h5 CUT_SUMMARY_SP-998_nmu_SAMPLE_N_15000.h5 

    fi
fi

