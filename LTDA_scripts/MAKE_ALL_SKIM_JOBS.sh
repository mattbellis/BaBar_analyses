# Data --------------------------------------------------------------
tag1="LambdaVeryVeryLoose"
tag2="a2-v03"

#tag1="AllEvents"
#tag2=""

for run in $(seq 1 6);
#for run in $(seq 2 6);
do
	    echo $run 
	    echo python set_up_everything_to_run_BtaTupleMaker.py -c ${tag1}-Run$run-OnPeak-R24${tag2} -t tclfiles/bnv_analysis.tcl --data -l /awg/bellis/bnv_analysis/
	    python set_up_everything_to_run_BtaTupleMaker.py -c ${tag1}-Run$run-OnPeak-R24${tag2} -t tclfiles/bnv_analysis.tcl --data -l /awg/bellis/bnv_analysis/
done

exit




# MC ------------------------------------------------------------------
#tag1="LambdaVeryVeryLoose-"
tag1=""

#tag2="a2-v03"
tag2=""

#for run in $(seq 1 6);
for run in $(seq 2 6);
do
	for sp in 1235 1237 998 1005 3429 3981 2400 991;
	#for sp in 991;
	do
	    echo $run $sp
	    #echo python set_up_everything_to_run_BtaTupleMaker.py -c SP-${sp}-Run${run}-R24 -t tclfiles/bnv_analysis.tcl --mc -l /awg/bellis/bnv_analysis/
	    #echo python set_up_everything_to_run_BtaTupleMaker.py -c SP-${sp}-${tag1}Run${run}-R24${tag2} -t tclfiles/bnv_analysis.tcl --mc -l /awg/bellis/bnv_analysis/
	    #python set_up_everything_to_run_BtaTupleMaker.py -c SP-${sp}-${tag1}Run${run}-R24${tag2} -t tclfiles/bnv_analysis.tcl --mc -l /awg/bellis/bnv_analysis/
	    echo python set_up_everything_to_run_BtaTupleMaker.py -c SP-${sp}-${tag1}Run${run}-R24${tag2} -t tclfiles/bnv_analysis.tcl --mc -l /awg/bellis/bnv_analysis/
	    python set_up_everything_to_run_BtaTupleMaker.py -c SP-${sp}-${tag1}Run${run}-R24${tag2} -t tclfiles/bnv_analysis.tcl --mc -l /awg/bellis/bnv_analysis/
	done
done
