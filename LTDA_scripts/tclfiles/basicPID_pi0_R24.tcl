#..Analysis2.tcl
#  Main tcl file for B --> Jpsi pi+ pi- K workbook tutorial

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
#FwkCfgVar ConfigPatch "MC"
FwkCfgVar ConfigPatch "Run2"

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
ErrLoggingLevel trace

#..btaMiniPhysics is the basic physics sequences; 
sourceFoundFile BetaMiniUser/btaMiniPhysics.tcl
#sourceFoundFile BetaMiniSequences/BetaMiniSequence.tcl
#sourceFoundFile BetaMiniSequences/BetaMiniPhysicsSequence.tcl
#sourceFoundFile BTaggingSequences/BtsVtxTagSequence.tcl
#sourceFoundFile BTaggingTools/BtgTaggingSequence.tcl
#sourceFoundFile UsrTools/UsrDataProcs.tcl

## Add Analysis module
##
#path append Everything StdHepPrint
#path append Everything StdHepAsciiDump

mod clone SmpMergerDefiner myList
path append Everything myList
path append Everything BtuTupleMaker
#path append Everything LambdaCTopKpi


# LambdaCs
#talkto LambdaCTopKpi {
  #createUsrData  set t
#}

talkto myList {
    # muons
    inputListNames set muCombinedVeryLooseFakeRate
    # protons
    inputListNames set pCombinedSuperLoose
    # electrons
    inputListNames set eCombinedSuperLoose
    #inputListNames set eBremReco
    # pions
    inputListNames set piCombinedSuperLoose
    # kaons
    inputListNames set KCombinedSuperLoose

    #inputList set LambdaCTopKpi
    #outputList set myLambdaCList
}

###
talkto BtuTupleMaker {

    #eventTagsFloat     set "R2 R2All xPrimaryVtx yPrimaryVtx zPrimaryVtx probPrimaryVtx eePx eePy eePz eeE beamSX beamSY beamSZ"
    #mcBlockContents set "Mass CMMomentum Momentum Vertex"

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsFloat     set "R2 R2All xPrimaryVtx yPrimaryVtx zPrimaryVtx probPrimaryVtx thrustMag thrustMagAll thrustCosTh thrustCosThAll thrustPhi thrustPhiAll sphericityAll"
    eventTagsInt       set "nTracks nGoodTrkLoose"
    eventTagsBool      set ""

    fillMC             set true

    listToDump         set myList

    #mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    #ntpBlockConfigs  set "gamma  gamma   4   256"
    #ntpBlockConfigs  set "D0   D0      2   256"

    #Momentum CMMomentum Doca DocaXY

    #ntpBlockContents set "gamma : Momentum CMMomentum"
    #ntpBlockContents set "D0 : Mass Momentum CMMomentum Vertex"

    ntpBlockConfigs  set "p+     p       0   256"
    #ntpBlockContents set "p :  Momentum CMMomentum Doca DocaXY PIDWeight(pLHVeryLoose,pLHLoose,pLHTight,pLHVeryTight)"
    ntpBlockContents set "p :  MCIdx CMMomentum"
    #ntpBlockContents set "p :  MCIdx"

    ntpBlockConfigs  set "K+     K       0   256"
    #ntpBlockContents set "K :  MCIdx Momentum CMMomentum Doca DocaXY PIDWeight(KLHVeryLoose,KLHLoose,KLHTight,KLHVeryTight)"
    ntpBlockContents set "K :  MCIdx CMMomentum"
    #ntpBlockContents set "K :  MCIdx"

    ntpBlockConfigs  set "pi+    pi      0   256"
    #ntpBlockContents set "Pi : Momentum CMMomentum Doca DocaXY PIDWeight(piLHVeryLoose,piLHLoose,piLHTight,piLHVeryTight)"
    ntpBlockContents set "pi : MCIdx CMMomentum"
    #ntpBlockContents set "pi : MCIdx"

    ntpBlockConfigs  set "mu-    mu      0   256"
    #ntpBlockContents set "mu : Momentum CMMomentum Doca DocaXY PIDWeight(muNNVeryLoose,muNNLoose,muNNTight,muNNVeryTight)"
    ntpBlockContents set "mu : MCIdx CMMomentum"
    #ntpBlockContents set "mu : MCIdx"

    ntpBlockConfigs  set "e-     e       0   256"
    #ntpBlockContents set "e :  MCIdx Doca DocaXY PIDWeight(eMicroVeryLoose) UsrData(myCandData)"
    ntpBlockContents set "e :  MCIdx CMMomentum"
    #ntpBlockContents set "e :  MCIdx"
    #
    ntpBlockConfigs set "pi0   pi0    2 256"
    ntpBlockContents set "pi0  : Mass VtxChi2 MCIdx CMMomentum"
    ntpAuxListContents set "pi0 : pi0LooseMass : _unc_ : Mass CMMomentum"
    #ntpAuxListContents set "pi0 : pi0LooseMass : _con_ : Mass CMMomentum"
    #ntpAuxListContents set "pi0 : MergedPi0Tight : _unc_ : Mass CMMomentum"



    ntpBlockConfigs set "gamma      gamma         0   256"
    ntpBlockContents set "gamma     : MCIdx CMMomentum"

    ntpBlockContents set "TRK  : MCIdx CMMomentum"
 
 
    ntpBlockToTrk set "pi K mu e p"

    gamExtraContents set EMC
    ## These are to get DCH and SVT info out for beta and dedx
    #trkExtraContents set HOTS:detailSVT,detailDCH
    #trkExtraContents set Dirc
    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    
    fillAllCandsInList set "gamma CalorNeutral"
    fillAllCandsInList set "pi0   pi0Loose"
    
    writeEveryEvent  set f 
    wantATrkBlock set true

    show
}
#
# I needed to add this line so that the PIDWeights get filled correctly
# for the nested selectors.
# But then I commented it out so it would work with data instead of MC
#pidCfg_mode weight *
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
