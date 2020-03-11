#python plot_KINVAR_files_missing_particle.py  --decay pmu BaBar_data/rootfiles/SP-9456-R24/basicPID_pi0_R24/PID_assignment/kinematic_distributions_pmu/SP-9456-R24-*1[0-2][0-9]*.root
#python plot_KINVAR_files_missing_particle.py  --decay pe BaBar_data/rootfiles/SP-9457-R24/basicPID_pi0_R24/PID_assignment/kinematic_distributions_pe/SP-9457-R24-*1[0-2][0-9]*.root

#python plot_KINVAR_files_missing_particle.py  --decay pnu BaBar_data/rootfiles/SP-11975-R24/basicPID_pi0_R24/PID_assignment/kinematic_distributions_pnu/SP-11975-R24-*1[0-2][0-9]*.root
#python plot_KINVAR_files_missing_particle.py  --decay nmu BaBar_data/rootfiles/SP-11976-R24/basicPID_pi0_R24/PID_assignment/kinematic_distributions_nmu/SP-11976-R24-*1[0-2][0-9]*.root
#python plot_KINVAR_files_missing_particle.py  --decay ne BaBar_data/rootfiles/SP-11977-R24/basicPID_pi0_R24/PID_assignment/kinematic_distributions_ne/SP-11977-R24-*1[0-2][0-9]*.root

#foreach sp ( SP-11975-R24 SP-11976-R24 SP-11977-R24 SP-9456-R24 SP-9457-R24 SP-1235-R24 SP-1237-R24 SP-1005-R24 SP-998-R24 SP-3429-R24 )
foreach sp ( SP-1235-R24 SP-1237-R24 SP-1005-R24 SP-998-R24 SP-3429-R24 )
    foreach decay(pmu pe pnu  nmu ne)
        echo $sp $decay
#echo python plot_KINVAR_files_missing_particle.py  --decay "$decay" #BaBar_data/rootfiles/SP-"$sp"-R24/basicPID_pi0_R24/PID_assignment/kinematic_distributions_"$decay"/SP-"$sp"-R24-*1[0-1][0-1]*.root
            python plot_KINVAR_files_missing_particle.py  --decay "$decay" BaBar_data/rootfiles/"$sp"/basicPID_pi0_R24/PID_assignment/kinematic_distributions_"$decay"/"$sp"-*1[0-1][0-1]*.root

    end
end

