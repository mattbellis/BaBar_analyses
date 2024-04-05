#------------------------------------------------------------------------------
# $Id: MyMiniAnalysis.tcl,v 1.29 2004/11/19 22:42:08 fnc Exp $
# Sample MyMiniAnalysis.tcl file
#------------------------------------------------------------------------------
# always source the error logger early in your main tcl script
sourceFoundFile ErrLogger/ErrLog.tcl
sourceFoundFile FrameScripts/FwkCfgVar.tcl
sourceFoundFile FrameScripts/talkto.tcl
# Disable the use of envvars
set ProdTclOnly true

# set the error logging level to 'warning'.  If you encounter a configuration 
# error you can get more information using 'trace'
ErrLoggingLevel warning

## allowed values of BetaMiniReadPersistence are (currently) "Kan", "Bdb"
##
FwkCfgVar BetaMiniReadPersistence Kan

## allowed (non-expert) values of levelOfDetail are "micro", "cache", "extend" 
## or "refit"
##
FwkCfgVar levelOfDetail "cache"

## allowed values of ConfigPatch are "Run1", "Run2" or "MC".  This MUST be set 
## consistent ## with your input data type or you will get INCONSISTENT OR 
## INCORRECT RESULTS
##
FwkCfgVar ConfigPatch "MC"

##
## Set the number of events to run. If this isn't set, all events in the
## input collections will be processed.
##
FwkCfgVar NEvent

## choose the flavor of ntuple to write (hbook or root) and the file name
##
FwkCfgVar BetaMiniTuple "root"
FwkCfgVar histFileName "MyMiniAnalysis.root"

#sourceFoundFile BetaMiniUser/btaMini.tcl
sourceFoundFile BetaMiniUser/btaMiniPhysics.tcl
#sourceFoundFile BetaMiniUser/btaMiniPhysProdSequence.tcl

talkto EvtCounter {
    printFreq set $PrintFreq
}


#module clone TagFilterByName TagBGFMultiHadron
#module talk TagBGFMultiHadron
#  andList set BGFMultiHadron
#  assertIfMissing set true
#exit
#sequence append BetaMiniReadSequence -a KanEventUpdateTag TagBGFMultiHadron
#module clone TagFilterByName MuMu
#module talk MuMu
#    andList set isBCMuMu
#    assertIfMissing set true
#    exit
#sequence append BetaMiniReadSequence -a KanEventUpdateTag MuMu

# a maker creates composite candidates from daughter lists
mod clone SmpMakerDefiner MyPhi
seq append SmpCompositionSequence MyPhi
catch { setProduction MyPhi }
talkto MyPhi {
    decayMode         set "phi -> K+ K-"
    daughterListNames set "$tracklist"
    daughterListNames set "$tracklist"
    fitConstraints    set "Geo"
    preFitSelectors   set "Mass :10"
    preFitSelectors   set "TwoTrkDoca :50"
    fittingAlgorithm  set "Cascade"
    postFitSelectors  set "ProbChiSq 0.001:1"
    postFitSelectors  set "Helicity"
    maxNumberOfCandidates set -1
    createUsrData set t
}

path append Everything BtuTupleMaker

talkto BtuTupleMaker {
    listToDump set MyPhi

    fillMC set t
    writeEveryEvent set t
    eventTagsBool set "isBCMuMu isBCMultiHadron BGFMultiHadron BGFMuMu"
    eventTagsFloat set "R2 R2All"
    eventTagsInt set "nTracks"
    mcBlockContents set "Mass CMMomentum Momentum"
    eventBlockContents set "EventID CMp4"

    ntpBlockConfigs set "phi Phi 2 100"
    ntpBlockContents set "Phi : MCIdx Mass Momentum MomentumErr Vertex VtxChi2 VtxCov UsrData(MyPhi)"
    ntpBlockConfigs set "K+ K  0  50"

    ntpBlockContents set "K: MCIdx Mass Momentum MomentumErr PIDWeight(VeryTightKMKaonMicroSelection)"


    ntpBlockToTrk set "K"
    fillAllCandsInList set "TRK GoodTracksLoose"
    ntpBlockContents set "TRK: MCIdx Momentum CMMomentum Doca DocaXY"
    trkExtraContents set BitMap:KSelectorsMap,muSelectorsMap,eSelectorsMap
    trkExtraContents set HOTS
}

pidCfg_mode tweak *

ErrMsg trace "completed OK"
ev beg -nev $NEvents

exit
