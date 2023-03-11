channel=$1
step=$2

if [[ $channel = "nmu" ]] 
then
    echo $channel
    echo $step

    if [[ $step = "prepare_samples" ]] 
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

    elif [[ $step = "train" ]] 
    then
        #toberemoved.append('bnvbcandmass')
        #toberemoved.append('nbnvbcand')
        #toberemoved.append('nhighmom')
        #toberemoved.append('bnvlepp3')
        #toberemoved.append('pp')
        #toberemoved.append('ep')
        #toberemoved.append('mup')

        python keras_example.py CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000.h5 MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5

    elif [[ $step = "apply_training" ]] 
    then

        #Look at the effect of the training on other datasets
        python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_653139_OPPOSITE.h5
        python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-1005_nmu_SAMPLE_N_266178_OPPOSITE.h5
        python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-1235_nmu_SAMPLE_N_37928_OPPOSITE.h5
        python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-1237_nmu_SAMPLE_N_31606_OPPOSITE.h5
        python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-998_nmu_SAMPLE_N_106200_OPPOSITE.h5

        python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-3429_nmu_SAMPLE_N_11616.h5
        python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-3981_nmu_SAMPLE_N_49.h5
        python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-980_nmu_SAMPLE_N_557.h5

        # Data
        python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5 CUT_SUMMARY_AllEvents-Run1_nmu_SAMPLE_N_11131.h5

    elif [[ $step = "plot_after_training" ]] 
    then
        # Plot them
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_653139_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy

        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-1005_nmu_SAMPLE_N_266178_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-1235_nmu_SAMPLE_N_37928_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-1237_nmu_SAMPLE_N_31606_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-998_nmu_SAMPLE_N_106200_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-3429_nmu_SAMPLE_N_11616_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-3981_nmu_SAMPLE_N_49_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-980_nmu_SAMPLE_N_557_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy

        # Data
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_AllEvents-Run1_nmu_SAMPLE_N_11131_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy

    elif [[ $step = "determine_parameters" ]]
    then
        # Fit the signal and background separately
        # Signal
        python fit_ML_output_SIGNAL_ONLY_THREE_ARGUS.py PREDICTIONS_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_653139_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy batch

        # Background
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1005_nmu_SAMPLE_N_266178_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy batch
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1235_nmu_SAMPLE_N_37928_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy batch
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1237_nmu_SAMPLE_N_31606_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy batch
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-998_nmu_SAMPLE_N_106200_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy batch
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-3429_nmu_SAMPLE_N_11616_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy batch
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-3981_nmu_SAMPLE_N_49_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy batch
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-980_nmu_SAMPLE_N_557_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy batch


    elif [[ $step = "toy_study" ]]
    then
        # Do some sample studies
        # Estimate 3000 events between 0.2 and 1 for Run 1
        # Run 2-6 has ~20x Run 1?
        python read_in_two_workspaces.py \
            workspace_PREDICTIONS_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_653139_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy.root \
            workspace_PREDICTIONS_CUT_SUMMARY_SP-1005_nmu_SAMPLE_N_266178_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy.root \
                    500 1000 # nsig ntrials 


        # Trying to fit the Run 1 data
    elif [[ $step = "fit_run1" ]]
    then
        python read_in_two_workspaces_and_fit_dataset_that_is_read_in.py workspace_PREDICTIONS_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_653139_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy.root workspace_PREDICTIONS_CUT_SUMMARY_SP-998_nmu_SAMPLE_N_106200_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy.root PREDICTIONS_CUT_SUMMARY_AllEvents-Run1_nmu_SAMPLE_N_11131_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
        

    elif [[ $step = "gen_random_embedded" ]]
    then
        # For some embedded tests
        python random_sample_from_dataframe.py CUT_SUMMARY_SP-11976_nmu.h5 500


    fi

################################################################################
elif [[ $channel = "ne" ]] 
then
    echo $channel
    echo $step

    if [[ $step = "prepare_samples" ]] 
    then

    ################################################################################
    # For ne
    ################################################################################
    #   ????
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-1005_ne.h5     30000 #
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-1235_ne.h5     20000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-1237_ne.h5     20000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-2400_ne.h5     50000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-3429_ne.h5     50000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-3981_ne.h5     50000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-980_ne.h5      50000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-998_ne.h5      15000 #   ???


    # There are ???? entries in the signal
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-11977_ne.h5 50000


    # Do this for data for Run 1 to apply the cuts
    python random_sample_from_dataframe.py CUT_SUMMARY_AllEvents-Run1_ne.h5 100000000

    # Now merge them
    python merge_training_samples.py MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5  CUT_SUMMARY_SP-1005_ne_SAMPLE_N_30000.h5 CUT_SUMMARY_SP-1235_ne_SAMPLE_N_20000.h5 CUT_SUMMARY_SP-1237_ne_SAMPLE_N_20000.h5 CUT_SUMMARY_SP-998_ne_SAMPLE_N_15000.h5

    elif [[ $step = "train" ]] 
    then
    #toberemoved.append('bnvbcandmass')
    #toberemoved.append('nbnvbcand')
    #toberemoved.append('nhighmom')
    #toberemoved.append('bnvlepp3')
    #toberemoved.append('pp')
    #toberemoved.append('ep')
    #toberemoved.append('mup')

    python keras_example.py CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000.h5 MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5

    elif [[ $step = "apply_training" ]] 
    then

        #Look at the effect of the training on other datasets
        python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_SP-11977_ne_SAMPLE_N_481991_OPPOSITE.h5

        python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_SP-1005_ne_SAMPLE_N_83676_OPPOSITE.h5
        python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_SP-1235_ne_SAMPLE_N_7149_OPPOSITE.h5
        python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_SP-1237_ne_SAMPLE_N_4719_OPPOSITE.h5
        python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_SP-998_ne_SAMPLE_N_42427_OPPOSITE.h5
        python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_SP-3429_ne_SAMPLE_N_19773.h5

        #python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_SP-3981_ne_SAMPLE_N_1.h5 # No events to work with after dropping values?
        #python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_SP-980_ne_SAMPLE_N_12.h5 # No events to work with after dropping values?

        # Data
        python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_AllEvents-Run1_ne_SAMPLE_N_5148.h5


    elif [[ $step = "plot_after_training" ]] 
    then
        # Plot them
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_481991_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy

        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-1005_ne_SAMPLE_N_83676_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-1235_ne_SAMPLE_N_7149_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-1237_ne_SAMPLE_N_4719_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-998_ne_SAMPLE_N_42427_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-3429_ne_SAMPLE_N_19773_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy

        # Data
        # Need to change, do we????
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_AllEvents-Run1_ne_SAMPLE_N_5148_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy


    elif [[ $step = "determine_parameters" ]]
    then
        # Fit the signal and background separately
        # Signal
        python fit_ML_output_SIGNAL_ONLY_THREE_ARGUS.py PREDICTIONS_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_481991_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy batch

        # Background
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1005_ne_SAMPLE_N_83676_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy batch
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1235_ne_SAMPLE_N_7149_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy batch
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1237_ne_SAMPLE_N_4719_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy batch
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-998_ne_SAMPLE_N_42427_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy batch
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-3429_ne_SAMPLE_N_19773_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy batch




    elif [[ $step = "toy_study" ]]
    then
        # Do some sample studies
        # Estimate 3000 events between 0.2 and 1 for Run 1
        # Run 2-6 has ~20x Run 1?
        python read_in_two_workspaces.py \
            workspace_PREDICTIONS_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_481991_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy.root \
            workspace_PREDICTIONS_CUT_SUMMARY_SP-1005_ne_SAMPLE_N_83676_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy.root \
            100 1000 # nsig ntrials


        # Trying to fit the Run 1 data
    elif [[ $step = "fit_run1" ]]
    then
        echo
        # 998 background shape
        #python read_in_two_workspaces_and_fit_dataset_that_is_read_in.py workspace_PREDICTIONS_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_481991_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy.root workspace_PREDICTIONS_CUT_SUMMARY_SP-998_ne_SAMPLE_N_42427_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy.root PREDICTIONS_CUT_SUMMARY_AllEvents-Run1_ne_SAMPLE_N_5148_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy
        # 1005 background shape
        python read_in_two_workspaces_and_fit_dataset_that_is_read_in.py workspace_PREDICTIONS_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_481991_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy.root workspace_PREDICTIONS_CUT_SUMMARY_SP-1005_ne_SAMPLE_N_83676_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy.root PREDICTIONS_CUT_SUMMARY_AllEvents-Run1_ne_SAMPLE_N_5148_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy

        

    elif [[ $step = "gen_random_embedded" ]]
    then
        echo
        # For some embedded tests
        python random_sample_from_dataframe.py CUT_SUMMARY_SP-11977_ne.h5 500



    fi


################################################################################
elif [[ $channel = "pnu" ]] 
then
    echo $channel
    echo $step

    if [[ $step = "prepare_samples" ]] 
    then

    ################################################################################
    # For ne
    ################################################################################
    #   ????
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-1005_pnu.h5     30000 #
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-1235_pnu.h5     20000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-1237_pnu.h5     20000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-2400_pnu.h5     50000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-3429_pnu.h5     50000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-3981_pnu.h5     50000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-980_pnu.h5      50000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-998_pnu.h5      15000 #   ???


    # There are ???? entries in the signal
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-11975_pnu.h5 50000


    # Do this for data for Run 1 to apply the cuts
    python random_sample_from_dataframe.py CUT_SUMMARY_AllEvents-Run1_pnu.h5 100000000

    # Now merge them
    python merge_training_samples.py MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.h5  CUT_SUMMARY_SP-1005_pnu_SAMPLE_N_30000.h5 CUT_SUMMARY_SP-1237_pnu_SAMPLE_N_1015.h5 CUT_SUMMARY_SP-1235_pnu_SAMPLE_N_994.h5 CUT_SUMMARY_SP-998_pnu_SAMPLE_N_15000.h5

    elif [[ $step = "train" ]] 
    then
        # Maybe
        #toberemoved.append('ne')
        #toberemoved.append('np')
        #toberemoved.append('nmu')
        #toberemoved.append('bnvbcandmass')
        #toberemoved.append('nbnvbcand')
        #toberemoved.append('nhighmom')
        #toberemoved.append('bnvlepp3')
        #toberemoved.append('bnvprotp3')
        #toberemoved.append('pp')

        python keras_example.py CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000.h5 MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.h5

    elif [[ $step = "apply_training" ]] 
    then

        #Look at the effect of the training on other datasets
        python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.h5 CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_495315_OPPOSITE.h5

        python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.h5 CUT_SUMMARY_SP-1005_pnu_SAMPLE_N_4854_OPPOSITE.h5
        python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.h5 CUT_SUMMARY_SP-998_pnu_SAMPLE_N_8265_OPPOSITE.h5

        #python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.h5 CUT_SUMMARY_SP-3981_pnu_SAMPLE_N_1.h5 # No events to work with after dropping values?
        #python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.h5 CUT_SUMMARY_SP-980_pnu_SAMPLE_N_12.h5 # No events to work with after dropping values?

        # Data
        python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.h5 CUT_SUMMARY_AllEvents-Run1_pnu_SAMPLE_N_3289.h5


    elif [[ $step = "plot_after_training" ]] 
    then
        # Plot them
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_495315_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy

        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-1005_pnu_SAMPLE_N_4854_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-998_pnu_SAMPLE_N_8265_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy

        # Data
        # Need to change, do we????
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_AllEvents-Run1_pnu_SAMPLE_N_3289_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy


    elif [[ $step = "determine_parameters" ]]
    then
        # Fit the signal and background separately
        # Signal
        python fit_ML_output_SIGNAL_ONLY_THREE_ARGUS.py PREDICTIONS_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_495315_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy batch

        # Background
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1005_pnu_SAMPLE_N_4854_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy batch
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-998_pnu_SAMPLE_N_8265_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy batch




    elif [[ $step = "toy_study" ]]
    then
        # Do some sample studies
        # Estimate 3000 events between 0.2 and 1 for Run 1
        # Run 2-6 has ~20x Run 1?
        python read_in_two_workspaces.py \
            workspace_PREDICTIONS_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_495315_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root \
            workspace_PREDICTIONS_CUT_SUMMARY_SP-1005_pnu_SAMPLE_N_4854_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root \
            100 100 # nsig ntrials



        # Trying to fit the Run 1 data
    elif [[ $step = "fit_run1" ]]
    then
        echo
        # 998 background shape
        #python read_in_two_workspaces_and_fit_dataset_that_is_read_in.py workspace_PREDICTIONS_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_495315_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root workspace_PREDICTIONS_CUT_SUMMARY_SP-998_pnu_SAMPLE_N_8265_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root PREDICTIONS_CUT_SUMMARY_AllEvents-Run1_pnu_SAMPLE_N_3289_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy
        # 1005 background shape
        python read_in_two_workspaces_and_fit_dataset_that_is_read_in.py workspace_PREDICTIONS_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_495315_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root workspace_PREDICTIONS_CUT_SUMMARY_SP-1005_pnu_SAMPLE_N_4854_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root PREDICTIONS_CUT_SUMMARY_AllEvents-Run1_pnu_SAMPLE_N_3289_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy

        

    elif [[ $step = "gen_random_embedded" ]]
    then
        echo
        # For some embedded tests
        python random_sample_from_dataframe.py CUT_SUMMARY_SP-11975_pnu.h5 500



    fi

################################################################################
elif [[ $channel = "pmu" ]] 
then
    echo $channel
    echo $step

    if [[ $step = "prepare_samples" ]] 
    then

    ################################################################################
    # For ne
    ################################################################################
    #   ????
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-1005_pmu.h5     30000 #
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-1235_pmu.h5     20000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-1237_pmu.h5     20000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-2400_pmu.h5     50000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-3429_pmu.h5     50000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-3981_pmu.h5     50000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-980_pmu.h5      50000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-998_pmu.h5      15000 #   ???


    # There are ???? entries in the signal
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-9456_pmu.h5 50000


    # Do this for data for Run 1 to apply the cuts
    python random_sample_from_dataframe.py CUT_SUMMARY_AllEvents-Run1_pmu.h5 100000000
    python random_sample_from_dataframe.py CUT_SUMMARY_AllEvents-Run2_pmu.h5 100000000
    python random_sample_from_dataframe.py CUT_SUMMARY_AllEvents-Run3_pmu.h5 100000000
    python random_sample_from_dataframe.py CUT_SUMMARY_AllEvents-Run4_pmu.h5 100000000
    python random_sample_from_dataframe.py CUT_SUMMARY_AllEvents-Run5_pmu.h5 100000000
    python random_sample_from_dataframe.py CUT_SUMMARY_AllEvents-Run6_pmu.h5 100000000

    # Now merge them
    python merge_training_samples.py MC_TRAINING_WEIGHTED_1005_1235_1237_998_pmu.h5  CUT_SUMMARY_SP-1005_pmu_SAMPLE_N_231.h5 CUT_SUMMARY_SP-998_pmu_SAMPLE_N_2103.h5

    # Dump mES but edit plot_many_variables_to give it the correct tag
    python plot_many_variables.py CUT_SUMMARY_AllEvents-Run1_pmu.h5

    python plot_mes_deltaE.py PREDICTIONS_MES_Run_1_pmu.npy
    python plot_mes_deltaE.py PREDICTIONS_MES_SP-9456_pmu.npy # Signal
    python plot_mes_deltaE.py PREDICTIONS_MES_MC-bkg_pmu.npy # MC bkg from cocktail

    # Fit the terms to determine parameters
    python fit_MES_output_SIGNAL_CRYSTAL_BALL.py PREDICTIONS_MES_SP-9456_pmu.npy
    python fit_MES_output_BACKGROUND_TWO_ARGUS.py PREDICTIONS_MES_MC-bkg_pmu.npy # This is probably a bit better
    #python fit_MES_output_BACKGROUND_ARGUS.py PREDICTIONS_MES_MC-bkg_pmu.npy

    # Trying some toy fits
    python read_in_two_workspaces.py workspace_PREDICTIONS_MES_SP-9456_pmu.root workspace_PREDICTIONS_MES_MC-bkg_pmu.root 20 1000


    elif [[ $step = "plot_after_training" ]] 
    then
        # Plot them
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_495315_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy

        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-1005_pnu_SAMPLE_N_4854_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-998_pnu_SAMPLE_N_8265_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy

        # Data
        # Need to change, do we????
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_AllEvents-Run1_pnu_SAMPLE_N_3289_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy


    elif [[ $step = "determine_parameters" ]]
    then
        # Fit the signal and background separately
        # Signal
        python fit_ML_output_SIGNAL_ONLY_THREE_ARGUS.py PREDICTIONS_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_495315_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy batch

        # Background
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1005_pnu_SAMPLE_N_4854_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy batch
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-998_pnu_SAMPLE_N_8265_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy batch




    elif [[ $step = "toy_study" ]]
    then
        # Do some sample studies
        # Estimate 3000 events between 0.2 and 1 for Run 1
        # Run 2-6 has ~20x Run 1?
        python read_in_two_workspaces.py \
            workspace_PREDICTIONS_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_495315_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root \
            workspace_PREDICTIONS_CUT_SUMMARY_SP-1005_pnu_SAMPLE_N_4854_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root \
            100 100 # nsig ntrials



        # Trying to fit the Run 1 data
    elif [[ $step = "fit_run1" ]]
    then
        echo
        # 998 background shape
        #python read_in_two_workspaces_and_fit_dataset_that_is_read_in.py workspace_PREDICTIONS_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_495315_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root workspace_PREDICTIONS_CUT_SUMMARY_SP-998_pnu_SAMPLE_N_8265_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root PREDICTIONS_CUT_SUMMARY_AllEvents-Run1_pnu_SAMPLE_N_3289_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy
        # 1005 background shape
        python read_in_two_workspaces_and_fit_dataset_that_is_read_in.py workspace_PREDICTIONS_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_495315_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root workspace_PREDICTIONS_CUT_SUMMARY_SP-1005_pnu_SAMPLE_N_4854_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root PREDICTIONS_CUT_SUMMARY_AllEvents-Run1_pnu_SAMPLE_N_3289_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy

        

    elif [[ $step = "gen_random_embedded" ]]
    then
        echo
        # For some embedded tests
        python random_sample_from_dataframe.py CUT_SUMMARY_SP-11975_pnu.h5 500



    fi

################################################################################
elif [[ $channel = "pe" ]] 
then
    echo $channel
    echo $step

    if [[ $step = "prepare_samples" ]] 
    then

    ################################################################################
    # For ne
    ################################################################################
    #   ????
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-1005_pe.h5     30000 #
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-1235_pe.h5     20000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-1237_pe.h5     20000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-2400_pe.h5     50000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-3429_pe.h5     50000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-3981_pe.h5     50000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-980_pe.h5      50000 #   ???
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-998_pe.h5      15000 #   ???


    # There are ???? entries in the signal
    python random_sample_from_dataframe.py CUT_SUMMARY_SP-9457_pe.h5 50000


    # Do this for data for Run 1 to apply the cuts
    python random_sample_from_dataframe.py CUT_SUMMARY_AllEvents-Run1_pe.h5 100000000
    python random_sample_from_dataframe.py CUT_SUMMARY_AllEvents-Run2_pe.h5 100000000
    python random_sample_from_dataframe.py CUT_SUMMARY_AllEvents-Run3_pe.h5 100000000
    python random_sample_from_dataframe.py CUT_SUMMARY_AllEvents-Run4_pe.h5 100000000
    python random_sample_from_dataframe.py CUT_SUMMARY_AllEvents-Run5_pe.h5 100000000
    python random_sample_from_dataframe.py CUT_SUMMARY_AllEvents-Run6_pe.h5 100000000

    # Now merge them
    python merge_training_samples.py MC_TRAINING_WEIGHTED_1005_1235_1237_998_pe.h5  CUT_SUMMARY_SP-1005_pe_SAMPLE_N_99.h5 CUT_SUMMARY_SP-998_pe_SAMPLE_N_162.h5

    # Dump mES but edit plot_many_variables_to give it the correct tag
    # Edit plot_many_variables to change the output file name
    python plot_many_variables.py CUT_SUMMARY_AllEvents-Run1_pe.h5
    python plot_many_variables.py CUT_SUMMARY_SP-9457_pe_SAMPLE_N_50000.h5
    python plot_many_variables.py MC_TRAINING_WEIGHTED_1005_1235_1237_998_pe.h5


    python plot_mes_deltaE.py PREDICTIONS_MES_Run_1_pe.npy
    python plot_mes_deltaE.py PREDICTIONS_MES_SP-9457_pe.npy # Signal
    python plot_mes_deltaE.py PREDICTIONS_MES_MC-bkg_pe.npy # MC bkg from cocktail

    # Fit the terms to determine parameters
    python fit_MES_output_SIGNAL_CRYSTAL_BALL.py PREDICTIONS_MES_SP-9457_pe.npy
    #python fit_MES_output_BACKGROUND_TWO_ARGUS.py PREDICTIONS_MES_MC-bkg_pe.npy 
    python fit_MES_output_BACKGROUND_ARGUS.py PREDICTIONS_MES_MC-bkg_pe.npy # This is probably a bit better

    # Trying some toy fits
    python read_in_two_workspaces.py workspace_PREDICTIONS_MES_SP-9456_pmu.root workspace_PREDICTIONS_MES_MC-bkg_pmu.root 20 1000


    elif [[ $step = "plot_after_training" ]] 
    then
        # Plot them
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_495315_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy

        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-1005_pnu_SAMPLE_N_4854_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-998_pnu_SAMPLE_N_8265_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy

        # Data
        # Need to change, do we????
        python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_AllEvents-Run1_pnu_SAMPLE_N_3289_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy


    elif [[ $step = "determine_parameters" ]]
    then
        # Fit the signal and background separately
        # Signal
        python fit_ML_output_SIGNAL_ONLY_THREE_ARGUS.py PREDICTIONS_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_495315_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy batch

        # Background
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1005_pnu_SAMPLE_N_4854_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy batch
        python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-998_pnu_SAMPLE_N_8265_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy batch




    elif [[ $step = "toy_study" ]]
    then
        # Do some sample studies
        # Estimate 3000 events between 0.2 and 1 for Run 1
        # Run 2-6 has ~20x Run 1?
        python read_in_two_workspaces.py \
            workspace_PREDICTIONS_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_495315_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root \
            workspace_PREDICTIONS_CUT_SUMMARY_SP-1005_pnu_SAMPLE_N_4854_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root \
            100 100 # nsig ntrials



        # Trying to fit the Run 1 data
    elif [[ $step = "fit_run1" ]]
    then
        echo
        # 998 background shape
        #python read_in_two_workspaces_and_fit_dataset_that_is_read_in.py workspace_PREDICTIONS_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_495315_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root workspace_PREDICTIONS_CUT_SUMMARY_SP-998_pnu_SAMPLE_N_8265_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root PREDICTIONS_CUT_SUMMARY_AllEvents-Run1_pnu_SAMPLE_N_3289_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy
        # 1005 background shape
        python read_in_two_workspaces_and_fit_dataset_that_is_read_in.py workspace_PREDICTIONS_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_495315_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root workspace_PREDICTIONS_CUT_SUMMARY_SP-1005_pnu_SAMPLE_N_4854_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root PREDICTIONS_CUT_SUMMARY_AllEvents-Run1_pnu_SAMPLE_N_3289_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy

        

    elif [[ $step = "gen_random_embedded" ]]
    then
        echo
        # For some embedded tests
        python random_sample_from_dataframe.py CUT_SUMMARY_SP-11975_pnu.h5 500



    fi
fi
fi
