#python random_sample_from_dataframe.py CUT_SUMMARY_SP-998_pnu.h5 20000
#python random_sample_from_dataframe.py CUT_SUMMARY_SP-998_pnu_B.h5 20000
#python random_sample_from_dataframe.py CUT_SUMMARY_SP-1005_pnu.h5 20000

#python merge_training_samples.py MC_TRAINING_2_SP-998_1_SP-1005_N_60000_pnu.h5 CUT_SUMMARY_SP-998_pnu_SAMPLE_N_20000.h5 CUT_SUMMARY_SP-998_pnu_B_SAMPLE_N_20000.h5 CUT_SUMMARY_SP-1005_pnu_SAMPLE_N_20000.h5

#python merge_training_samples.py MC_TRAINING_SP-998_N_40000_pnu.h5 CUT_SUMMARY_SP-998_pnu_SAMPLE_N_20000.h5 CUT_SUMMARY_SP-998_pnu_B_SAMPLE_N_20000.h5 

# nmu
python random_sample_from_dataframe.py CUT_SUMMARY_SP-998_nmu.h5 100000
python random_sample_from_dataframe.py CUT_SUMMARY_SP-1005_nmu.h5 100000
python merge_training_samples.py MC_TRAINING_SP-998_N_100000_nmu_SP-1005_nmu_SAMPLE_N_100000.h5 CUT_SUMMARY_SP-998_nmu_SAMPLE_N_100000.h5 CUT_SUMMARY_SP-1005_nmu_SAMPLE_N_100000.h5 

# ne
#python random_sample_from_dataframe.py CUT_SUMMARY_SP-998_ne.h5 50000
#python random_sample_from_dataframe.py CUT_SUMMARY_SP-1005_ne.h5 25000
#python merge_training_samples.py MC_TRAINING_SP-998_N_50000_ne_SP-1005_ne_SAMPLE_N_25000.h5 CUT_SUMMARY_SP-998_ne_SAMPLE_N_50000.h5 CUT_SUMMARY_SP-1005_ne_SAMPLE_N_25000.h5 

