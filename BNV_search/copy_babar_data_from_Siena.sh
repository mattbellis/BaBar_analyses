# FROM SLAC
#scp "rhel6-64.slac.stanford.edu:ltda_staging/*.root" .
#scp "rhel6-64.slac.stanford.edu:ltda_staging/*945[67]*.root" .
#scp "rhel6-64.slac.stanford.edu:ltda_staging/*comp*.root" .
#scp bellis@bbrltda.slac.stanford.edu:/awg/breco/bellis/analysis52/workdir/rootfiles/SP-998-R24/basicPID_R24-SP-998-R24-[0-9]_SKIMMED.root .
#scp "bellis@bbrltda.slac.stanford.edu:/awg/breco/bellis/analysis52/workdir/rootfiles/SP-1197[567]-R24/basicPID_R24-*1.root" .
#scp "bellis@bbrltda.slac.stanford.edu:/awg/breco/bellis/analysis52/workdir/bellis_basicPID_R24_SP-998-R24/basicPID_R24-SP-998-R24-21491.root" .
#scp "bellis@bbrltda.slac.stanford.edu:/awg/breco/bellis/analysis52/workdir/bellis_basicPID_R24_SP-1235-R24/basicPID_R24-SP-1235-R24-3228.root" .

#scp "bellis@bbrltda.slac.stanford.edu:/awg/breco/bellis/analysis52/workdir/rootfiles/SP-1197[567]-R24/basicPID_pi0_R24/SP-1197[567]-R24-1_SKIMMED.root" basicPID_pi0_R24/.
#scp "bellis@bbrltda.slac.stanford.edu:/awg/breco/bellis/analysis52/workdir/rootfiles/SP-123[57]-R24/basicPID_pi0_R24/SP-123[57]-R24-1_SKIMMED.root" basicPID_pi0_R24/.

#scp "bellis@bbrltda.slac.stanford.edu:/awg/breco/bellis/analysis52/workdir/rootfiles/SP-998-R24/basicPID_pi0_R24/SP-998-R24-1_SKIMMED.root" basicPID_pi0_R24/.
#scp "bellis@bbrltda.slac.stanford.edu:/awg/breco/bellis/analysis52/workdir/rootfiles/SP-1005-R24/basicPID_pi0_R24/SP-1005-R24-1_SKIMMED.root" basicPID_pi0_R24/.

#scp "bellis@bbrltda.slac.stanford.edu:/awg/breco/bellis/analysis52/workdir/rootfiles/SP-945[67]-R24/basicPID_pi0_R24/SP-945[67]-R24-1_SKIMMED.root" basicPID_pi0_R24/.

# FROM SIENA
#scp "mbellis@olsen.cs.siena.edu:BaBar_BNV_output/OUTPUT_[pn]*SP-*.pkl" BNV_output/.
#scp "mbellis@olsen.cs.siena.edu:BaBar_BNV_output/OUTPUT_[pn]*SP-1235*.pkl" BNV_output/.
#scp -r "mbellis@olsen.cs.siena.edu:cut_summary_files" BNV_output/.

#rsync -avh mbellis@olsen.cs.siena.edu:cut_summary_files /home/bellis/babar_data/BNV_output/


# Direct from grawp
rsync -avh mbellis@localhost:/qnap/mbellis/bellis/BaBar/rootfiles/cut_summary_files_df /home/bellis/babar_data/

