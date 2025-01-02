for filename in log/SP-*LambdaVeryVeryLoose*v03/bnv_analysis/*tcl.sh.log log/SP-991*/bnv_analysis/*tcl.sh.log log/LambdaVeryVeryLoose-Run*/bnv_analysis/*tcl.sh.log ; do

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
		grep -h $job submission_scripts/bnv_analysis/*sh
	fi

done



