# Data --------------------------------------------------------------
tclfile="bnv_analysis_bnc_mode.tcl"
outputdir="bnv_analysis_bnc_mode"
tag1="LambdaVeryVeryLoose"
tag2="a2-v03"

#tag1="AllEvents"
#tag2=""

#for run in $(seq 1 6);
##for run in $(seq 2 6);
#do
	    #echo $run 
	    #echo python set_up_everything_to_run_BtaTupleMaker.py -c ${tag1}-Run$run-OnPeak-R24${tag2} -t tclfiles/${tclfile} --data -l /awg/bellis/${outputdir}/
	    #python set_up_everything_to_run_BtaTupleMaker.py -c ${tag1}-Run$run-OnPeak-R24${tag2} -t tclfiles/${tclfile} --data -l /awg/bellis/${outputdir}/
#done
#
#exit




# MC ------------------------------------------------------------------
tag1="LambdaVeryVeryLoose-"
#tag1=""

tag2="a2-v03"
#tag2=""

for run in $(seq 1 2);
#for run in $(seq 1 6);
#for run in $(seq 2 6);
do
	#for sp in 1235 1237 998 1005 3429 3981 2400 991;
	for sp in 1005;
	#for sp in 991;
	do
	    echo $run $sp
	    #echo python set_up_everything_to_run_BtaTupleMaker.py -c SP-${sp}-Run${run}-R24 -t tclfiles/${tclfile} --mc -l /awg/bellis/${outputdir}/
	    #echo python set_up_everything_to_run_BtaTupleMaker.py -c SP-${sp}-${tag1}Run${run}-R24${tag2} -t tclfiles/${tclfile} --mc -l /awg/bellis/${outputdir}/
	    #python set_up_everything_to_run_BtaTupleMaker.py -c SP-${sp}-${tag1}Run${run}-R24${tag2} -t tclfiles/${tclfile} --mc -l /awg/bellis/${outputdir}/
	    echo python set_up_everything_to_run_BtaTupleMaker.py -c SP-${sp}-${tag1}Run${run}-R24${tag2} -t tclfiles/${tclfile} --mc -l /awg/bellis/${outputdir}/
	    python set_up_everything_to_run_BtaTupleMaker.py -c SP-${sp}-${tag1}Run${run}-R24${tag2} -t tclfiles/${tclfile} --mc -l /awg/bellis/${outputdir}/
	done
done
