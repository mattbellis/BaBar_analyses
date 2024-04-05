#..Analysis.tcl
#  Main tcl file for B+ --> Jpsi K+ [Jpsi --> mu+ mu-] workbook tutorial

#..General setup needed in all jobs
sourceFoundFile ErrLogger/ErrLog.tcl
sourceFoundFile FrameScripts/FwkCfgVar.tcl
sourceFoundFile FrameScripts/talkto.tcl

#-------------- FwkCfgVars needed to control this job ---------------------
set ProdTclOnly true

#..allowed values of BetaMiniReadPersistence are "Kan", "Bdb"
FwkCfgVar BetaMiniReadPersistence Kan

#..allowed values of levelOfDetail are "micro", "cache", "extend" or "refit"
FwkCfgVar levelOfDetail "cache"

#..allowed values of ConfigPatch are "Run2" or "MC".
FwkCfgVar ConfigPatch "MC"

#..Filter on tag bits by default
FwkCfgVar FilterOnTag   "true"

#..Print Frequency
FwkCfgVar PrintFreq 1000

#..Ntuple type and name 
FwkCfgVar BetaMiniTuple "root"
FwkCfgVar histFileName "Tutorial.root"

#..Number of Events defaults to 0 (run on full tcl file)
FwkCfgVar NEvents 0

#--------------------------------------------------------------------------
#..General physics sequences

#..set to 'trace' to get info on a configuration problem
ErrLoggingLevel warning

#..btaMiniPhysics is the basic physics sequences; 
sourceFoundFile BetaMiniUser/btaMiniPhysics.tcl

#--------------------------------------------------------------------------
#..Use SimpleComposition to make the candidates of interest

#..Create Analysis sequence and append it to the path.
#  All the composition modules get added to this sequence

sequence create AnalysisSequence
path append Everything AnalysisSequence

#------------------ Jpsi Lists --------------------------------------

#..Basic Jpsi to mu mu list, no mass constraint (for ntuple)
mod clone SmpMakerDefiner MyJpsiToMuMu
seq append AnalysisSequence MyJpsiToMuMu
talkto MyJpsiToMuMu {
    decayMode set "J/psi -> mu+ mu-"
    daughterListNames  set muNNVeryLoose
    daughterListNames  set muNNVeryLoose
    fittingAlgorithm   set "Cascade"
    fitConstraints     set "Geo"
    preFitSelectors    set "Mass 2.8:3.4"
    postFitSelectors   set "Mass 2.9:3.3"
}

#..Now add the mass constraint
mod clone SmpRefitterDefiner MyJpsiToMuMuMass
seq append AnalysisSequence MyJpsiToMuMuMass
talkto MyJpsiToMuMuMass {
    unrefinedListName  set MyJpsiToMuMu
    fittingAlgorithm   set "Cascade"
    fitConstraints     set "Geo"
    fitConstraints     set "Mass"
}

#------------------------ B+ ---------------------------------------
#..B+ --> Jpsi K+
mod clone SmpMakerDefiner BchtoJpsiKch
seq append AnalysisSequence BchtoJpsiKch
talkto BchtoJpsiKch {
    decayMode             set "B+ -> J/psi K+"
    daughterListNames     set "MyJpsiToMuMuMass"
    daughterListNames     set "KLHVeryLoose"
    fittingAlgorithm      set "TreeFitter"
    fitConstraints        set "Geo"
    preFitSelectors       set "DeltaE -0.20:0.20"
    preFitSelectors       set "Mes 5.19:5.30"
    postFitSelectors      set "ProbChiSq 0.001:"
    postFitSelectors      set "DeltaE -0.12:0.12"
    postFitSelectors      set "Mes 5.20:5.30"
    postFitSelectors      set "CmsCosTheta"
    postFitSelectors      set "Mmiss"
    createUsrData         set true
}

#--------------------------------------------------------------------
#..Use BtuTupleMaker to write out ntuples for SimpleComposition job
path append Everything BtuTupleMaker

talkto BtuTupleMaker {

#..Event information to dump
    eventBlockContents   set "EventID CMp4 BeamSpot"
    eventTagsInt set "nTracks"
    eventTagsFloat set "R2All xPrimaryVtx yPrimaryVtx zPrimaryVtx"
    writeEveryEvent set false

#..MC truth info
    fillMC set true
    mcBlockContents set "Mass CMMomentum Momentum Vertex"

#..Particle blocks to store
    listToDump set BchtoJpsiKch

    ntpBlockConfigs set "B-      B    2      50"
    ntpBlockContents set "B: MCIdx Mass Momentum CMMomentum Vertex VtxChi2 UsrData(BchtoJpsiKch)"

    ntpBlockConfigs set "J/psi   Jpsi   2      50"
    ntpBlockContents set "Jpsi: MCIdx Mass Momentum CMMomentum Vertex VtxChi2"
    ntpAuxListContents set "Jpsi: MyJpsiToMuMu : Unc : Mass"

    ntpBlockConfigs set "K+      K      0      50"
    ntpBlockContents set "K: MCIdx Momentum CMMomentum PIDWeight(KLHVeryLoose,KLHLoose,KLHTight)"

    ntpBlockConfigs set "mu+      mu      0      50"
    ntpBlockContents set "mu: MCIdx Momentum CMMomentum PIDWeight(muNNVeryLoose,muNNLoose)"

#..Want to save all CalorNeutrals in the gamma block
    ntpBlockConfigs set "gamma   gamma  0      60"
    ntpBlockContents set "gamma: MCIdx Momentum"
    gamExtraContents set EMC
    fillAllCandsInList set "gamma CalorNeutral"

#..TRK block. Save all of them as well.
    fillAllCandsInList set "TRK ChargedTracks"

#..remember to change this back to K pi mu e
    ntpBlockToTrk   set "K mu"
    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    trkExtraContents set HOTS
    trkExtraContents set Eff:ave
    ntpBlockContents set "TRK: Doca DocaXY"
}

#--------------- Turn on PID weights and neutral corrections ----------------

#pidCfg_mode weight *

talkto EmcNeutCorrLoader {
   correctionOn set true
   #endcapShift  set true 
}

#----------------------------------------------------------------------------
#..Use $FilterOnTag to disable tag filtering if desired.
module clone TagFilterByName TagJpsill
module talk TagJpsill
  orList set JpsiELoose
  orList set JpsiMuLoose
  assertIfMissing set true
exit
if { $FilterOnTag=="true" } {
    sequence append BetaMiniReadSequence -a KanEventUpdateTag TagJpsill
}

#-----------------------------------------------------------------------
#..Run time options

mod talk EvtCounter
  printFreq set $PrintFreq
exit

path list

if { $NEvents>=0 } {
    ev beg -nev $NEvents
    exit
}
