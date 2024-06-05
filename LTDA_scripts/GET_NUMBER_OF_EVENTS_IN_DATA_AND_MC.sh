echo "Data -------------------------------------"
#for tag in "AllEvents" "LambdaVeryVeryLoose";
for tag in "LambdaVeryVeryLoose";
do
	tag2=""
	if [[ $tag == "-LambdaVeryVeryLoose" ]] 
	then
		tag2="a2-v03"
	fi

	for run in $(seq 1 6);
	do
		echo "Run ""${run}"
		BbkDatasetTcl --notcl "${tag}-Run$run-OnPeak-R24${tag2}" --dbname bbkr24
	done
done

exit

echo "MC -------------------------------------"
for tag in "" "-LambdaVeryVeryLoose";
#for tag in "-LambdaVeryVeryLoose";
do
	tag2=""
	if [[ $tag == "-LambdaVeryVeryLoose" ]] 
	then
		tag2="a2-v03"
	fi

	for sp in 1235 1237 998 1005 3429 3981 2400 991;
	do	
		for run in $(seq 1 6);
		do
			echo "SP-""${sp}${tag}"
			BbkDatasetTcl --notcl "SP-${sp}${tag}-Run${run}-R24${tag2}" --dbname bbkr24 
			echo
		done
	done
	echo
	echo
done
