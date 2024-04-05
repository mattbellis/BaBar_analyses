#------------------------------------------------------------------------------
# $Id: BtuMyAnalysis.tcl,v 1.6 2004/07/14 19:04:52 chcheng Exp $
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
FwkCfgVar NEvents

## choose the flavor of ntuple to write (hbook or root) and the file name
##
FwkCfgVar BetaMiniTuple "root"
FwkCfgVar histFileName "MyMiniAnalysis.roo"

##
##  You can enter input collections two ways: either append them to a list, or
##  explicitly enter them in the input module. Do one or the other, BUT NOT 
##  BOTH.
##  If inputList is set before executing btaMini.tcl, that will automatically
##  add the collections to the appropriate input module, otherwise make sure you
##  talk to the right one.
##
## lappend inputList collection1 collection2 ...
##
##  OR THE FOLLOWING (choose the correct one based on persistence)
##
## talkto BdbEventInput {
## talkto KanEventInput {
##    input add collection1
##    input add collection2
##    ...
## }

## create Everything path and add core sequences to it. btaMiniPhysics is the 
## same as btaMini, just appending a few standard list generating modules. For 
## reading data with stored composites, you may have a conflict running 
## btaMiniPhyscs.tcl
##
## You can also run (most of) the PhysProdSequence, complete with its 3 gamma 
## conversion finders, etc. Consider disabling the portion of this sequence 
## that you do not need to save yourself some time.  The BetaLumiSequence
## and TagProd sequences are left off, as they otherwise cause problems.
##
#sourceFoundFile BetaMiniUser/btaMini.tcl
sourceFoundFile BetaMiniUser/btaMiniPhysics.tcl
#sourceFoundFile BetaMiniUser/btaMiniPhysProdSequence.tcl


sourceFoundFile UsrTools/UsrDataProcs.tcl
enableReadUsrData
#readEventUsrData myEventData
readCandUsrData  B0ToD0KPi


## Add Analysis module
##
path append Everything BtuMyAnalysis
path append Everything BtuTupleMaker

talkto BtuMyAnalysis {
    inputList  set B0ToD0barNonCPKPi
    outputList set myB0List
}

talkto BtuTupleMaker {
    listToDump set myB0List

    fillMC set true

    eventBlockContents set "EventID CMp4 BeamSpot "
    eventTagsBool      set "BGFMultiHadron B0ToD0barNonCPKPi"
    eventTagsInt       set "nTracks nGoodTrkLoose"
    eventTagsFloat     set "R2All"

    mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    ntpBlockConfigs set "B0    B0     3 100"
    ntpBlockConfigs set "D0    D0     4 100"
    ntpBlockConfigs set "K_S0  KS     2  10"
    ntpBlockConfigs set "K+    K      0  10"
    ntpBlockConfigs set "pi+   Pi     0  30"
    ntpBlockConfigs set "pi0   Pi0    2  30"
    ntpBlockConfigs set "gamma   gamma    0  30"

    ntpBlockToTrk   set "K Pi"

    ntpBlockContents set "B0   : Mass CMMomentum Vertex VtxChi2 MCIdx"
    ntpBlockContents set "D0   : Mass Vertex VtxChi2"
    ntpBlockContents set "KS   : Mass VtxChi2"
    ntpBlockContents set "Pi0  : Mass VtxChi2"
    ntpBlockContents set "K    : Momentum"
    ntpBlockContents set "Pi   : Momentum"
    ntpBlockContents set "gamma: Momentum"
    ntpBlockContents set "TRK  : MCIdx"

    trkExtraContents set HOTS:detailSVT
    trkExtraContents set Eff:ave,charge
    trkExtraContents set PidMap:KSelectorsMap,eSelectorsMap

    gamExtraContents set EMC

    baseTrackList   set ChargedTracks
    
    show
}

##
##  If your job has a tag-level filter, here is how you should run it
##  so as to avoid wasting time reading the mini when the tag filter fails
##  Here's a simple example that restricts to just multi-hadron events
##  on Kan input

module clone TagFilterByName MyTagFilter
module talk MyTagFilter
  andList set B0ToD0barNonCPKPi
  assertIfMissing set true
exit
sequence append BetaMiniReadSequence -a KanEventUpdateTag MyTagFilter

#
#  Turn off some specialty items
#
module disable MyDstarAnalysis
module disable MyK0Analysis
module disable MyMiniAnalysis
#module disable BtuMyAnalysis
#module disable BtuTupleMaker

path list
if [info exists NEvents] {
   ev begin -nev $NEvents
} else {
  ev begin 
}

ErrMsg trace "completed OK"
exit
