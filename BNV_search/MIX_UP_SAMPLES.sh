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

# Do this for data for Run 1 to apply the cuts
python random_sample_from_dataframe.py CUT_SUMMARY_AllEvents-Run1_nmu.h5 100000000



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

# Data
python load_in_ML_model.py  KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.h5 CUT_SUMMARY_AllEvents-Run1_nmu_SAMPLE_N_11131.h5





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



# Try to determine the parameters
python fit_ML_output_SIGNAL_ONLY_THREE_ARGUS.py PREDICTIONS_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_653139_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy

python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1005_nmu_SAMPLE_N_266178_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1235_nmu_SAMPLE_N_37928_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1237_nmu_SAMPLE_N_31606_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-998_nmu_SAMPLE_N_106200_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-3429_nmu_SAMPLE_N_11616_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-3981_nmu_SAMPLE_N_49_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy
python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-980_nmu_SAMPLE_N_557_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy


# Do some sample studies
# Estimate 3000 events between 0.2 and 1 for Run 1
# Run 2-6 has ~20x Run 1?

python read_in_two_workspaces.py workspace_PREDICTIONS_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_653139_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy.root workspace_PREDICTIONS_CUT_SUMMARY_SP-1005_nmu_SAMPLE_N_266178_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy.root 500 100


# Trying to fit the Run 1 data
python read_in_two_workspaces_and_fit_dataset_that_is_read_in.py workspace_PREDICTIONS_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_653139_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy.root workspace_PREDICTIONS_CUT_SUMMARY_SP-998_nmu_SAMPLE_N_106200_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy.root PREDICTIONS_CUT_SUMMARY_AllEvents-Run1_nmu_SAMPLE_N_11131_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy


# For some embedded tests
python random_sample_from_dataframe.py CUT_SUMMARY_SP-11976_nmu.h5 500
















################################################################################
# For pe
################################################################################
######## FIX THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Just train against 998
# There are 105783 entries 
#python random_sample_from_dataframe.py CUT_SUMMARY_SP-998_pmu.h5 50000

# There are 1030079 entries in the signal
#python random_sample_from_dataframe.py CUT_SUMMARY_SP-9456_pmu.h5 50000



################################################################################
# For ne
################################################################################
#   12574889
python random_sample_from_dataframe.py CUT_SUMMARY_SP-1005_ne.h5     30000 # 
python random_sample_from_dataframe.py CUT_SUMMARY_SP-1235_ne.h5     20000 #   ???
python random_sample_from_dataframe.py CUT_SUMMARY_SP-1237_ne.h5     20000 #   ???
python random_sample_from_dataframe.py CUT_SUMMARY_SP-2400_ne.h5     50000 #   ???
python random_sample_from_dataframe.py CUT_SUMMARY_SP-3429_ne.h5     50000 #   ???
python random_sample_from_dataframe.py CUT_SUMMARY_SP-3981_ne.h5     50000 #   ???
python random_sample_from_dataframe.py CUT_SUMMARY_SP-980_ne.h5      50000 #   ???
python random_sample_from_dataframe.py CUT_SUMMARY_SP-998_ne.h5      15000 #   ???

# There are 1230535 entries in the signal
python random_sample_from_dataframe.py CUT_SUMMARY_SP-11977_ne.h5 50000

# Do this for data for Run 1 to apply the cuts
python random_sample_from_dataframe.py CUT_SUMMARY_AllEvents-Run1_ne.h5 100000000



# Now merge them
python merge_training_samples.py MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5  CUT_SUMMARY_SP-1005_ne_SAMPLE_N_30000.h5 CUT_SUMMARY_SP-1235_ne_SAMPLE_N_20000.h5 CUT_SUMMARY_SP-1237_ne_SAMPLE_N_20000.h5 CUT_SUMMARY_SP-998_ne_SAMPLE_N_15000.h5 

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
python keras_example.py CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000.h5 MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5


# Look at the effect of the training on other datasets
python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_SP-11977_ne_SAMPLE_N_481991_OPPOSITE.h5

python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_SP-1005_ne_SAMPLE_N_83676_OPPOSITE.h5
python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_SP-1235_ne_SAMPLE_N_7149_OPPOSITE.h5
python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_SP-1237_ne_SAMPLE_N_4719_OPPOSITE.h5
python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_SP-998_ne_SAMPLE_N_42427_OPPOSITE.h5
python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_SP-3429_ne_SAMPLE_N_19773.h5

#python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_SP-3981_ne_SAMPLE_N_1.h5 # No events to work with after dropping values?
#python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_SP-980_ne_SAMPLE_N_12.h5 # No events to work with after dropping values?


# Data
# ???
python load_in_ML_model.py KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.h5 CUT_SUMMARY_AllEvents-Run1_ne_SAMPLE_N_5148.h5





# Plot them
python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_481991_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy

python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-1005_ne_SAMPLE_N_83676_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy
python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-1235_ne_SAMPLE_N_7149_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy
python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-1237_ne_SAMPLE_N_4719_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy
python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-998_ne_SAMPLE_N_42427_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy
python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_SP-3429_ne_SAMPLE_N_19773_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy


# Data
# Need to change
python plot_ML_output.py PREDICTIONS_CUT_SUMMARY_AllEvents-Run1_ne_SAMPLE_N_5148_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy



# Try to determine the parameters
python fit_ML_output_SIGNAL_ONLY_THREE_ARGUS.py PREDICTIONS_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_481991_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy

python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1005_ne_SAMPLE_N_83676_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy
python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1235_ne_SAMPLE_N_7149_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy
python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-1237_ne_SAMPLE_N_4719_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy
python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-998_ne_SAMPLE_N_42427_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy
python fit_ML_output_BACKGROUND_ONLY_TWO_ARGUS_AND_EXPONENTIAL.py PREDICTIONS_CUT_SUMMARY_SP-3429_ne_SAMPLE_N_19773_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy


# Do some sample studies
# Estimate 3000 events between 0.2 and 1 for Run 1
# Run 2-6 has ~20x Run 1?

# NOT SURE IF THE 500 / 100 are good numbers
python read_in_two_workspaces.py workspace_PREDICTIONS_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_481991_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy.root workspace_PREDICTIONS_CUT_SUMMARY_SP-1005_ne_SAMPLE_N_83676_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11977_ne_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_ne.npy.root 500 100




# Trying to fit the Run 1 data
python read_in_two_workspaces_and_fit_dataset_that_is_read_in.py workspace_PREDICTIONS_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_653139_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy.root workspace_PREDICTIONS_CUT_SUMMARY_SP-998_nmu_SAMPLE_N_106200_OPPOSITE_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy.root PREDICTIONS_CUT_SUMMARY_AllEvents-Run1_nmu_SAMPLE_N_11131_KERAS_TRAINING_CUT_SUMMARY_SP-11976_nmu_SAMPLE_N_50000_MC_TRAINING_WEIGHTED_1005_1235_1237_998_nmu.npy


# For some embedded tests
python random_sample_from_dataframe.py CUT_SUMMARY_SP-11976_nmu.h5 500
