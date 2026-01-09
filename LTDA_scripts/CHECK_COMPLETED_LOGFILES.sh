#subdir="bnv_analysis"
#subdir="bnv_analysis_bnc_mode"
subdir="bnv_analysis_lam0lam0"

for filename in log/SP-*LambdaVeryVeryLoose*v03/${subdir}/*tcl.sh.log log/SP-991*/${subdir}/*tcl.sh.log log/LambdaVeryVeryLoose-Run*/${subdir}/*tcl.sh.log ; do

	#echo $filename

#	if grep -q "Ran to completion" $filename
#	then
#		:
#	else
#		echo $filename
#	fi

	if grep -q "Abort" $filename
	then
		# For debugging
		#echo $filename

		job=$(basename $filename .log)
		# -h for grep supresses the filename that it finds it in
		grep -h $job submission_scripts/${subdir}/*sh
	fi

done



