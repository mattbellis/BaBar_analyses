#!/bin/bash

# Assigning input arguments to variables
output_directory=$1
submission_script=$2

# Loop through each job command in the submission script
while IFS= read -r line; do
 
    # Check if it is the 'sleep' line
    if [[ $line != *"sleep"* ]]; then

	    # Extracting job number from the command
	    # bsub -o log/SP-1005-LambdaVeryVeryLoose-Run5-R24a2-v03/bnv_analysis/SP-1005-LambdaVeryVeryLoose-Run5-R24a2-v03-31.tcl.sh.log -j oe shell_scripts/SP-1005-LambdaVeryVeryLoose-Run5-R24a2-v03/bnv_analysis/SP-1005-LambdaVeryVeryLoose-Run5-R24a2-v03-31.tcl.sh
	    #job_number=$(echo "$line" | grep -oP '\d+')
	    job_number=$(echo "$line" | awk -F"-" '{print $13}' | awk -F"." '{print $1}') 
	    #echo "job number   " ${job_number}

	    # rootfiles/SP-1005-LambdaVeryVeryLoose-Run4-R24a2-v03/bnv_analysis/SP-1005-LambdaVeryVeryLoose-Run4-R24a2-v03-100.root
	    tempname=$(basename $output_directory)
	    #echo "tempname  ", ${tempname}
	    output_file="${output_directory}/bnv_analysis/${tempname}-${job_number}.root"
	    #echo "Output"
	    #echo ${output_file}
	    
	    # Check if the output file does not exist
	    if [ ! -f "$output_file" ]; then
		echo "Missing!"
		echo "$line" # Print the job command that needs to be rerun
	    fi
    fi
done < "$submission_script"
