# From within workdir
#mkdir /awg/bellis/scratch
#mkdir /awg/bellis/scratch/bellis
#ln -s /awg/bellis/scratch/ .


# Build the smp_task file

# Need to make sure this is in `smp_decfile` directory as a softlink
#decfile="B+B-_lambdaproton_BNV.dec"
#prod_run_name="bnv_plam3"
#nevents="100000"

# BNC
# Need to make sure this is in `smp_decfile` directory as a softlink
decfile="B+B-_lambdaproton.dec"
prod_run_name="bnc_plam"
nevents="100000"

# Need to make our directory first
# OR NOT?
#mkdir ${prod_run_name}


SMP_CFG_FILE=smp_task_"${prod_run_name}".cfg

cat SMP_TASK_TEMPLATE.cfg  | sed "s/PRODUCTION_RUN_NAME/${prod_run_name}/" > temp.cfg
cat temp.cfg  | sed "s/NEVENTS/${nevents}/" > temp2.cfg
cat temp2.cfg  | sed "s/DEC_FILE/${decfile}/" > $SMP_CFG_FILE

echo "SMP_CFG_FILE"
echo $SMP_CFG_FILE

smp prepare $SMP_CFG_FILE

ALL_SUBMISSION_COMMANDS=all_submission_commands_"${prod_run_name}".sh
rm ${ALL_SUBMISSION_COMMANDS}
touch ${ALL_SUBMISSION_COMMANDS}

# Do stuff
for count in {0000..0069};
do
	JDL_FILE=moose_condor_submission_"${prod_run_name}"_"${count}".jdl

	#SINGLE_DIGIT=$(echo $count | sed 's/00//' | sed 's/0//')
	SINGLE_DIGIT=$(expr $count + 0)
	echo $count $SINGLE_DIGIT
	cat MOOSE_JDL_TEMPLATE.jdl  | sed "s/JOB_NAME/${prod_run_name}/g" > temp.jdl
	cat temp.jdl  | sed "s/SINGLE_DIGIT/${SINGLE_DIGIT}/g" > temp2.jdl
	cat temp2.jdl  | sed "s/LEADING_ZEROS/${count}/g" > $JDL_FILE

	chmod +x $JDL_FILE

	echo condor_submit $JDL_FILE >> ${ALL_SUBMISSION_COMMANDS}
	echo sleep 1 >> ${ALL_SUBMISSION_COMMANDS}
	
done

chmod +x ${ALL_SUBMISSION_COMMANDS}


# All the output rootfiles are copied to 
# workdir/scratch/bellis/$prod_run_name
