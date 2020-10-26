#foreach sp ( SP-11975-R24 SP-11976-R24 SP-11977-R24 SP-9456-R24 SP-9457-R24 SP-1235-R24 SP-1237-R24 SP-1005-R24 SP-998-R24 SP-3429-R24 )
foreach sp ( AllEvents-Run1-OnPeak-R24 AllEvents-Run2-OnPeak-R24 AllEvents-Run3-OnPeak-R24 AllEvents-Run4-OnPeak-R24 AllEvents-Run5-OnPeak-R24 AllEvents-Run6-OnPeak-R24 )
	
	echo "-------------------"
	echo $sp

	wc -l "submission_scripts/basicPID_pi0_R24/sub_"$sp"-basicPID_pi0_R24.sh"
	ls "rootfiles/"$sp"/basicPID_pi0_R24/" | wc -l 
	#python resubmit.py "submission_scripts/basicPID_pi0_R24/sub_"$sp"-basicPID_pi0_R24.sh"

	echo 

end

