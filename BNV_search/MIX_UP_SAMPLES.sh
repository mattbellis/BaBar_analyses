################################################################################
# For pmu
################################################################################
# Just train against 998
# There are 105783 entries 
#python random_sample_from_dataframe.py CUT_SUMMARY_SP-998_pmu.h5 50000

# There are 1030079 entries in the signal
#python random_sample_from_dataframe.py CUT_SUMMARY_SP-9456_pmu.h5 50000



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


# Now merge them
python merge_training_samples.py MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-1005_nmu_SAMPLE_N_30000.h5 CUT_SUMMARY_SP-1235_nmu_SAMPLE_N_20000.h5 CUT_SUMMARY_SP-1237_nmu_SAMPLE_N_20000.h5 CUT_SUMMARY_SP-998_nmu_SAMPLE_N_15000.h5 

# Now train
'''
toberemoved.append('bnvbcandmass')
toberemoved.append('nbnvbcand')
toberemoved.append('nhighmom')
toberemoved.append('bnvlepp3')
toberemoved.append('pp')
toberemoved.append('ep')
toberemoved.append('mup')
'''
python keras_example.py CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000.h5 MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5


# Look at the effect of the training on other datasets
python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_653139_OPPOSITE.h5
python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-1005_nmu_SAMPLE_N_266178_OPPOSITE.h5
python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-1235_nmu_SAMPLE_N_37928_OPPOSITE.h5
python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-1237_nmu_SAMPLE_N_31606_OPPOSITE.h5
python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-998_nmu_SAMPLE_N_106200_OPPOSITE.h5

python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-3429_nmu_SAMPLE_N_11616.h5
python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-3981_nmu_SAMPLE_N_49.h5
python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5  CUT_SUMMARY_SP-980_nmu_SAMPLE_N_557.h5




# Plot them
python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_653139_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy

python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-1005_nmu_SAMPLE_N_266178_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-1235_nmu_SAMPLE_N_37928_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-1237_nmu_SAMPLE_N_31606_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-998_nmu_SAMPLE_N_106200_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-3429_nmu_SAMPLE_N_11616_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-3981_nmu_SAMPLE_N_49_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-980_nmu_SAMPLE_N_557_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy


# Try to determine the parameters
python fit_ML_output_SIGNAL_ONLY_THREE_ARGUS.py PREDICTIONS_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_653139_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy

python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1005_nmu_SAMPLE_N_266178_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1235_nmu_SAMPLE_N_37928_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1237_nmu_SAMPLE_N_31606_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-998_nmu_SAMPLE_N_106200_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-3429_nmu_SAMPLE_N_11616_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-3981_nmu_SAMPLE_N_49_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-980_nmu_SAMPLE_N_557_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy




