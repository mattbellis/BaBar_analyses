#python random_sample_from_dataframe.py CUT_SUMMARY_SP-998_pnu.h5 20000
#python random_sample_from_dataframe.py CUT_SUMMARY_SP-998_pnu_B.h5 20000
#python random_sample_from_dataframe.py CUT_SUMMARY_SP-1005_pnu.h5 20000

python merge_training_samples.py MC_TRAINING_2_SP-998_1_SP-1005_N_60000_pnu.h5 CUT_SUMMARY_SP-998_pnu_SAMPLE_N_20000.h5 CUT_SUMMARY_SP-998_pnu_B_SAMPLE_N_20000.h5 CUT_SUMMARY_SP-1005_pnu_SAMPLE_N_20000.h5


