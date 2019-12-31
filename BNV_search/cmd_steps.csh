#python dump_ROOT_files_based_on_PID_assignments.py /home/bellis/babar_data/basicPID_pi0_R24/SP-11976-R24-1_SKIMMED.root
#python look_at_kinematic_distributions.py /home/bellis/babar_data/basicPID_pi0_R24/SP-11976-R24-1_SKIMMED_PID_skim.root
#python make_plots_for_talk.py /home/bellis/babar_data/basicPID_R24-SP-11975-R24-1_PID_skim_KINVARS_pnu.root

#python dump_ROOT_files_based_on_PID_assignments.py /home/bellis/babar_data/basicPID_pi0_R24/SP-1237-R24-1_SKIMMED.root
#python look_at_kinematic_distributions.py /home/bellis/babar_data/basicPID_pi0_R24/SP-1237-R24-1_SKIMMED_PID_skim.root

#python plot_KINVAR_files_missing_particle.py ~/babar_data/basicPID_pi0_R24/SP-11975-R24-1_SKIMMED_PID_skim_KINVARS_pnu.root

#python dump_ROOT_files_based_on_PID_assignments.py /home/bellis/babar_data/basicPID_pi0_R24/SP-11976-R24-1_SKIMMED.root
#python look_at_kinematic_distributions.py /home/bellis/babar_data/basicPID_pi0_R24/SP-11976-R24-1_SKIMMED_PID_skim.root --decay nmu

#python dump_ROOT_files_based_on_PID_assignments.py /home/bellis/babar_data/basicPID_pi0_R24/SP-11977-R24-1_SKIMMED.root
#python look_at_kinematic_distributions.py /home/bellis/babar_data/basicPID_pi0_R24/SP-11977-R24-1_SKIMMED_PID_skim.root --decay ne

python dump_ROOT_files_based_on_PID_assignments.py /home/bellis/babar_data/basicPID_pi0_R24/SP-9456-R24-1_SKIMMED.root
python look_at_kinematic_distributions.py /home/bellis/babar_data/basicPID_pi0_R24/SP-9456-R24-1_SKIMMED_PID_skim.root --decay pmu

python dump_ROOT_files_based_on_PID_assignments.py /home/bellis/babar_data/basicPID_pi0_R24/SP-9457-R24-1_SKIMMED.root
python look_at_kinematic_distributions.py /home/bellis/babar_data/basicPID_pi0_R24/SP-9457-R24-1_SKIMMED_PID_skim.root --decay pe

foreach sp('1235' '1237' '998' '1005')
python dump_ROOT_files_based_on_PID_assignments.py /home/bellis/babar_data/basicPID_pi0_R24/SP-"$sp"-R24-1_SKIMMED.root
    python look_at_kinematic_distributions.py /home/bellis/babar_data/basicPID_pi0_R24/SP-"$sp"-R24-1_SKIMMED_PID_skim.root --decay pnu
    python look_at_kinematic_distributions.py /home/bellis/babar_data/basicPID_pi0_R24/SP-"$sp"-R24-1_SKIMMED_PID_skim.root --decay nmu
    python look_at_kinematic_distributions.py /home/bellis/babar_data/basicPID_pi0_R24/SP-"$sp"-R24-1_SKIMMED_PID_skim.root --decay ne

    python look_at_kinematic_distributions.py /home/bellis/babar_data/basicPID_pi0_R24/SP-"$sp"-R24-1_SKIMMED_PID_skim.root --decay pmu
    python look_at_kinematic_distributions.py /home/bellis/babar_data/basicPID_pi0_R24/SP-"$sp"-R24-1_SKIMMED_PID_skim.root --decay pe
end
