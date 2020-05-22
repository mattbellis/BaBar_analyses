foreach sp ( SP-11975-R24 SP-11976-R24 SP-11977-R24 SP-9456-R24 SP-9457-R24 SP-1235-R24 SP-1237-R24 SP-1005-R24 SP-998-R24 SP-3429-R24 )
#foreach sp ( AllEvents-Run1-OnPeak-R24 AllEvents-Run2-OnPeak-R24 AllEvents-Run3-OnPeak-R24 AllEvents-Run4-OnPeak-R24 AllEvents-Run5-OnPeak-R24 AllEvents-Run6-OnPeak-R24 )

#echo "-------------------"
#echo ls "rootfiles/"$sp"/basicPID_pi0_R24/"
                                    set num = `ls "BaBar_data/rootfiles/"$sp"/basicPID_pi0_R24/" | wc -l`
                                    set num2 = `ls "BaBar_data/rootfiles/"$sp"/basicPID_pi0_R24/PID_assignment/" | wc -l`
                                    set num3 = `ls "BaBar_data/rootfiles/"$sp"/basicPID_pi0_R24/PID_assignment/kinematic_distributions_pmu" | wc -l`
                                    set num4 = `ls "BaBar_data/rootfiles/"$sp"/basicPID_pi0_R24/PID_assignment/kinematic_distributions_pe" | wc -l`
                                    set num5 = `ls "BaBar_data/rootfiles/"$sp"/basicPID_pi0_R24/PID_assignment/kinematic_distributions_pnu" | wc -l`
                                    set num6 = `ls "BaBar_data/rootfiles/"$sp"/basicPID_pi0_R24/PID_assignment/kinematic_distributions_nmu" | wc -l`
                                    set num7 = `ls "BaBar_data/rootfiles/"$sp"/basicPID_pi0_R24/PID_assignment/kinematic_distributions_ne" | wc -l`
                                            #python resubmit.py "submission_scripts/basicPID_pi0_R24/sub_"$sp"-basicPID_pi0_R24.sh"


   echo $num $num2 $num3 $num4 $num5 $num6 $num7   $sp

   du -smch BaBar_data/rootfiles/"$sp"/basicPID_pi0_R24/ | grep total
   du -smch BaBar_data/rootfiles/"$sp"/basicPID_pi0_R24/PID_assignment/ | grep total
   du -smch BaBar_data/rootfiles/"$sp"/basicPID_pi0_R24/PID_assignment/kinematic_distributions_pmu | grep total
   du -smch BaBar_data/rootfiles/"$sp"/basicPID_pi0_R24/PID_assignment/kinematic_distributions_pe | grep total
   du -smch BaBar_data/rootfiles/"$sp"/basicPID_pi0_R24/PID_assignment/kinematic_distributions_pnu | grep total
   du -smch BaBar_data/rootfiles/"$sp"/basicPID_pi0_R24/PID_assignment/kinematic_distributions_nmu | grep total
   du -smch BaBar_data/rootfiles/"$sp"/basicPID_pi0_R24/PID_assignment/kinematic_distributions_ne | grep total
end

