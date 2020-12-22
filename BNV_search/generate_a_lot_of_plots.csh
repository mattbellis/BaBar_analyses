# Make plots for documentation
#python plot_many_variables.py CUT_SUMMARY_SP-998_pmu.h5 CUT_SUMMARY_SP-1005_pmu.h5 CUT_SUMMARY_SP-123[57]_pmu.h5  CUT_SUMMARY_SP-3429_pmu.h5 CUT_SUMMARY_SP-3981_pmu.h5 CUT_SUMMARY_SP-2400_pmu.h5 CUT_SUMMARY_SP-9456_pmu.h5 CUT_SUMMARY_AllEvents-MERGED_AllRuns_WITHBNVCHILDRENPCUT_pmu.h5

#python plot_many_variables.py CUT_SUMMARY_SP-998_pe.h5 CUT_SUMMARY_SP-1005_pe.h5 CUT_SUMMARY_SP-123[57]_pe.h5 CUT_SUMMARY_SP-3429_pe.h5 CUT_SUMMARY_SP-2400_pe.h5 CUT_SUMMARY_SP-3981_pe.h5  CUT_SUMMARY_SP-9457_pe.h5 CUT_SUMMARY_AllEvents-MERGED_AllRuns_WITHBNVCHILDRENPCUT_pe.h5

python plot_many_variables.py CUT_SUMMARY_SP-998_pnu.h5 CUT_SUMMARY_SP-1005_pnu.h5 CUT_SUMMARY_SP-123[57]_pnu.h5  CUT_SUMMARY_SP-3429_pnu.h5 CUT_SUMMARY_SP-3981_pnu.h5 CUT_SUMMARY_SP-2400_pnu.h5 CUT_SUMMARY_SP-11975_pnu.h5 CUT_SUMMARY_AllEvents-MERGED_AllRuns_WITHBNVCHILDRENPCUT_pnu.h5

#python plot_many_variables.py CUT_SUMMARY_SP-998_nmu.h5 CUT_SUMMARY_SP-1005_nmu.h5 CUT_SUMMARY_SP-123[57]_nmu.h5  CUT_SUMMARY_SP-3429_nmu.h5 CUT_SUMMARY_SP-3981_nmu.h5 CUT_SUMMARY_SP-2400_nmu.h5 CUT_SUMMARY_SP-11976_nmu.h5 CUT_SUMMARY_AllEvents-MERGED_AllRuns_WITHBNVCHILDRENPCUT_nmu.h5

#python plot_many_variables.py CUT_SUMMARY_SP-998_ne.h5 CUT_SUMMARY_SP-1005_ne.h5 CUT_SUMMARY_SP-123[57]_ne.h5  CUT_SUMMARY_SP-3429_ne.h5 CUT_SUMMARY_SP-3981_ne.h5 CUT_SUMMARY_SP-2400_ne.h5 CUT_SUMMARY_SP-11977_ne.h5 CUT_SUMMARY_AllEvents-MERGED_AllRuns_WITHBNVCHILDRENPCUT_ne.h5







#python plot_many_variables.py CUT_SUMMARY_SP-998_ne.h5 CUT_SUMMARY_SP-1005_ne.h5 CUT_SUMMARY_SP-123[57]_ne.h5  CUT_SUMMARY_SP-3429_ne.h5 CUT_SUMMARY_AllEvents-MERGED_AllRuns_WITHBNVCHILDRENPCUT_ne.h5
#python plot_many_variables.py CUT_SUMMARY_SP-998_nmu.h5 CUT_SUMMARY_SP-1005_nmu.h5 CUT_SUMMARY_SP-123[57]_nmu.h5  CUT_SUMMARY_SP-3429_nmu.h5 CUT_SUMMARY_AllEvents-MERGED_AllRuns_WITHBNVCHILDRENPCUT_nmu.h5
#python plot_many_variables.py CUT_SUMMARY_SP-998_pnu.h5 CUT_SUMMARY_SP-1005_pnu.h5 CUT_SUMMARY_SP-123[57]_pnu.h5  CUT_SUMMARY_SP-3429_pnu.h5 CUT_SUMMARY_AllEvents-MERGED_AllRuns_WITHBNVCHILDRENPCUT_pnu.h5
#python plot_many_variables.py CUT_SUMMARY_SP-998_pe.h5 CUT_SUMMARY_SP-1005_pe.h5 CUT_SUMMARY_SP-123[57]_pe.h5  CUT_SUMMARY_SP-3429_pe.h5 CUT_SUMMARY_AllEvents-MERGED_AllRuns_WITHBNVCHILDRENPCUT_pe.h5

#python plot_many_variables.py CUT_SUMMARY_SP-998_nmu.h5 CUT_SUMMARY_SP-1005_nmu.h5 CUT_SUMMARY_SP-123[57]_nmu.h5  CUT_SUMMARY_SP-3429_nmu.h5

#python plot_many_variables.py CUT_SUMMARY_SP-11976_nmu.h5


################################################################################
# For 2D DeltaE vs mES
#foreach decay('pe' 'pmu')
#foreach sp("SP-1005" "SP-11975" "SP-11976" "SP-11977" "SP-1235" "SP-1237" "SP-3429" "SP-9456" "SP-9457" "SP-980" "SP-998")
#python plot_many_variables.py CUT_SUMMARY_"$sp"_"$decay".h5
#end
#end

#python plot_many_variables.py CUT_SUMMARY_AllEvents-MERGED_AllRuns_WITHBNVCHILDRENPCUT_pmu.h5
#python plot_many_variables.py CUT_SUMMARY_AllEvents-MERGED_AllRuns_WITHBNVCHILDRENPCUT_pe.h5
