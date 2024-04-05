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


talkto myList {
    inputListNames set D0ToKPiLoosePID
    inputListNames set KLHNotPion
    inputListNames set GoodTracksVeryLoose
    inputListNames set CalorClusterNeutral
}

###
talkto BtuTupleMaker {

    listToDump         set myList
    eventBlockContents   set "EventID CMp4 BeamSpot"
    eventTagsFloat     set "R2 R2All xPrimaryVtx yPrimaryVtx zPrimaryVtx probPrimaryVtx"
    fillMC             set false
    #mcBlockContents set "Mass CMMomentum Momentum Vertex"

    eventBlockContents set "EventID"
    eventTagsInt       set "nTracks"
    eventTagsBool      set ""

    #mcBlockContents    set "Mass CMMomentum Momentum Vertex"
    ntpBlockConfigs  set "pi+    Pi      0   100"
    ntpBlockConfigs  set "K+     K       0   100"
    ntpBlockConfigs  set "gamma  gamma   4   100"
    #ntpBlockConfigs  set "mu-    mu      0   100"
    #ntpBlockConfigs  set "e-     e       0   100"
    ntpBlockConfigs  set "D0   D0      2   100"

    #Momentum CMMomentum Doca DocaXY

    ntpBlockContents set "gamma : Momentum CMMomentum"
    ntpBlockContents set "Pi : Momentum CMMomentum Doca DocaXY "
    ntpBlockContents set "K :  Momentum CMMomentum Doca DocaXY "
    #ntpBlockContents set "mu : Momentum CMMomentum Doca DocaXY"
    #ntpBlockContents set "e :  MCIdx Doca DocaXY PIDWeight(eMicroVeryLoose) UsrData(myCandData)"
    ntpBlockContents set "D0 : Mass Momentum CMMomentum Vertex"

    ntpBlockToTrk set "Pi K"

    #gamExtraContents set EMC
    trkExtraContents set HOTS:detailSVT,detailDCH
    
    #fillAllCandsInList set "gamma CalorNeutral"
    
    writeEveryEvent  set f 
    

    show
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





