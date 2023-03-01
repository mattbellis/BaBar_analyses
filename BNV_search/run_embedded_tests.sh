nsig=50

conda activate base

# Gen random sample
python random_sample_from_dataframe.py CUT_SUMMARY_SP-11975_pnu.h5 $nsig


# Embed
python merge_training_samples.py \
    TEMP_test_sample.h5 \
    CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_"$nsig".h5  \
    CUT_SUMMARY_AllEvents-Run1_pnu_SAMPLE_N_3289.h5 

#exit

# Produce output variable
python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.h5 TEMP_test_sample.h5

conda activate pyhep

python read_in_two_workspaces_and_fit_dataset_that_is_read_in.py \
    workspace_PREDICTIONS_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_495315_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root \
    workspace_PREDICTIONS_CUT_SUMMARY_SP-1005_pnu_SAMPLE_N_4854_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy.root \
    PREDICTIONS_TEMP_test_sample_KERAS_TRAINING_CUT_SUMMARY_SP-11975_pnu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_pnu.npy
