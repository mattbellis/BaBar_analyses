# First do this in a window
ssh -L 22000:grawp.siena.edu:22 mbellis@olsen.cs.siena.edu
# Then do this in another window
#scp -r -P 22000 mbellis@localhost:/qnap/mbellis/bellis/BaBar/rootfiles/cut_summary_files/SP-980/ .

#scp -r -P 22000 mbellis@localhost:/qnap/mbellis/bellis/BaBar/rootfiles/SP-9456-R24/basicPID_pi0_R24/PID_assignment/kinematic_distributions_pmu/ .

#scp -r -P 22000 "mbellis@localhost:/qnap/mbellis/bellis/BaBar/rootfiles//SP-9456-R24/basicPID_pi0_R24/*.root"
#scp -r -P 22000 "mbellis@localhost:/qnap/mbellis/bellis/BaBar/rootfiles//SP-9456-R24/basicPID_pi0_R24/SP-9456-R24-100_SKIMMED.root"

#scp -r -P 22000 "mbellis@localhost:/qnap/mbellis/bellis/BaBar/rootfiles/cut_summary_files_pickle/SP-9456/pmu" .

scp -r -P 22000 "mbellis@localhost:/qnap/mbellis/bellis/BaBar/rootfiles/cut_summary_files_pickle/SP-9456/pmu" cut_summary_files_pickle/SP-9456/.
scp -r -P 22000 "mbellis@localhost:/qnap/mbellis/bellis/BaBar/rootfiles/cut_summary_files_pickle/SP-9457/pe" cut_summary_files_pickle/SP-9457/.
scp -r -P 22000 "mbellis@localhost:/qnap/mbellis/bellis/BaBar/rootfiles/cut_summary_files_pickle/SP-11975/pnu" cut_summary_files_pickle/SP-11975/.
scp -r -P 22000 "mbellis@localhost:/qnap/mbellis/bellis/BaBar/rootfiles/cut_summary_files_pickle/SP-11976/nmu" cut_summary_files_pickle/SP-11976/.
scp -r -P 22000 "mbellis@localhost:/qnap/mbellis/bellis/BaBar/rootfiles/cut_summary_files_pickle/SP-11977/ne" cut_summary_files_pickle/SP-11977/.

scp -r -P 22000 "mbellis@localhost:/qnap/mbellis/bellis/BaBar/rootfiles/cut_summary_files_df/SP-998" cut_summary_files_pickle/.


#scp -r -P 22000 mbellis@localhost:/qnap/mbellis/bellis/BaBar/rootfiles/SP-11975-R24/basicPID_pi0_R24/PID_assignment/kinematic_distributions_pnu/ SP-11975-R24/
scp -r -P 22000 mbellis@localhost:/qnap/mbellis/bellis/BaBar/rootfiles/SP-998-R24/basicPID_pi0_R24/PID_assignment/kinematic_distributions_pnu/ SP-998-R24/
scp -r -P 22000 mbellis@localhost:/qnap/mbellis/bellis/BaBar/rootfiles/SP-998-R24/basicPID_pi0_R24/PID_assignment/kinematic_distributions_nmu/ SP-998-R24/
scp -r -P 22000 mbellis@localhost:/qnap/mbellis/bellis/BaBar/rootfiles/SP-998-R24/basicPID_pi0_R24/PID_assignment/kinematic_distributions_pmu/ SP-998-R24/



# Direct from grawp
rsync -avh -e "ssh -p 22000" mbellis@localhost:/qnap/mbellis/bellis/BaBar/rootfiles/cut_summary_files_df /home/bellis/babar_data/

rsync -avh -e "ssh -p 22000" mbellis@localhost:BaBar_analyses/BNV_search/CUT_SUM*.h5 /home/bellis/BaBar_analyses/BNV_search/.
