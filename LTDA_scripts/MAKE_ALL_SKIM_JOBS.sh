for run in $(seq 1 6);
do
	for sp in 1235 1237 998 1005 3429 3981 2400;
	#for sp in 998;
	do
	    echo $run $sp
	    #echo python set_up_everything_to_run_BtaTupleMaker.py -c SP-${sp}-Run${run}-R24 -t tclfiles/bnv_analysis.tcl --mc -l /awg/bellis/bnv_analysis/
	    #echo python set_up_everything_to_run_BtaTupleMaker.py -c SP-${sp}-LambdaVeryVeryLoose-Run${run}-R24a2 -t tclfiles/bnv_analysis.tcl --mc -l /awg/bellis/bnv_analysis/
	    #python set_up_everything_to_run_BtaTupleMaker.py -c SP-${sp}-LambdaVeryVeryLoose-Run${run}-R24a2 -t tclfiles/bnv_analysis.tcl --mc -l /awg/bellis/bnv_analysis/
	    echo python set_up_everything_to_run_BtaTupleMaker.py -c SP-${sp}-LambdaVeryVeryLoose-Run${run}-R24a2-v03 -t tclfiles/bnv_analysis.tcl --mc -l /awg/bellis/bnv_analysis/
	    python set_up_everything_to_run_BtaTupleMaker.py -c SP-${sp}-LambdaVeryVeryLoose-Run${run}-R24a2-v03 -t tclfiles/bnv_analysis.tcl --mc -l /awg/bellis/bnv_analysis/
	done
done
