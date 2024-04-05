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
    mcBlockContents set "Mass CMMomentum Momentum Vertex"

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsFloat     set "R2 R2All xPrimaryVtx yPrimaryVtx zPrimaryVtx probPrimaryVtx thrustMag thrustMagAll thrustCosTh thrustCosThAll thrustPhi thrustPhiAll sphericityAll"
    #eventTagsFloat     set "R2 R2All xPrimaryVtx yPrimaryVtx zPrimaryVtx probPrimaryVtx" 
    eventTagsInt       set "nTracks nGoodTrkLoose nChargedTracks" 
    eventTagsBool      set ""

    #fillMC             set false
    fillMC             set true

    listToDump         set myList

    #mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    #ntpBlockConfigs  set "gamma  gamma   4   100"
    #ntpBlockConfigs  set "D0   D0      2   100"

    #Momentum CMMomentum Doca DocaXY
    ntpBlockConfigs  set "p+     p       0   100"
    ntpBlockConfigs  set "K+     K       0   100"
    ntpBlockConfigs  set "pi+    pi      0   100"
    ntpBlockConfigs  set "mu-    mu      0   100"
    ntpBlockConfigs  set "e-     e       0   100"

    ntpBlockContents set "p :  MCIdx"
    ntpBlockContents set "K :  MCIdx"
    ntpBlockContents set "pi : MCIdx"
    ntpBlockContents set "mu : MCIdx"
    ntpBlockContents set "e :  MCIdx"

    ntpBlockConfigs  set "gamma      gamma         0   90"
    ntpBlockContents set "gamma     : MCIdx Momentum CMMomentum"

    ntpBlockContents set "TRK  : MCIdx Momentum CMMomentum"

    ################# Write out all the charged tracks
    fillAllCandsInList set "TRK ChargedTracks"

    fillAllCandsInList set "gamma CalorNeutral"
    ntpBlockToTrk set "pi K mu e p"

    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    
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
