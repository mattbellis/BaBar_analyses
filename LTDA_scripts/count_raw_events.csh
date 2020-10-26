foreach sp ('1235' '1237' '1005' '998' '3429' '3981' '2400')

	echo "SP-""$sp"
	BbkDatasetTcl --notcl "SP-$sp-R24" --dbname bbkr24 --dbsite slac 
	#set num = `BbkDatasetTcl --notcl "SP-$sp-R24" --dbname bbkr24 --dbsite slac | awk '{print $4}'  | awk -F'/' '{print $1}'`
	#echo $sp $num

end

foreach run ('1' '2' '3' '4' '5' '6' )

	echo "Run "$run
	BbkDatasetTcl --notcl "AllEvents-Run$run-OnPeak-R24" --dbname bbkr24 --dbsite slac 
	#set num = `BbkDatasetTcl --notcl "AllEvents-Run$run-OnPeak-R24" --dbname bbkr24 --dbsite slac | awk '{print $4}'  | awk -F'/' '{print $1}'`
	#echo $run $num

end
