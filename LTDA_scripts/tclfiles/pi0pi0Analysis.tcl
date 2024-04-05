#------------------------------------------------------------------------------
# $Id: BtuMyAnalysis.tcl,v 1.4 2004/06/11 04:16:12 chcheng Exp $
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
sourceFoundFile BetaMiniUser/btaMiniPhysics.tcl


#sourceFoundFile UsrTools/UsrDataProcs.tcl
#enableReadUsrData
#readEventUsrData myEventData
#readCandUsrData xxx


#### Do SimpleComposition
seq create SmpMyB0Sequence

# ->  B0
mod clone SmpMakerDefiner myB0ToPi0Pi0
seq append SmpMyB0Sequence myB0ToPi0Pi0
catch { setProduction myB0ToPi0Pi0 }
talkto myB0ToPi0Pi0 {
    debug              set f
    verbose            set f
    decayMode          set "B0 -> pi0 pi0"
    daughterListNames  set "pi0LooseMass"
    daughterListNames  set "pi0LooseMass"

    fittingAlgorithm   set "Add4"
    preFitSelectors    set "Mass 4.5:5.5"
    preFitSelectors    set "DeltaE -0.5:0.5"
    postFitSelectors   set "Mes 5.2:5.3"
    postFitSelectors   set "DeltaE -0.2:0.2"

    createUsrData  set t
}

## Add Analysis module
##
path append Everything SmpMyB0Sequence
path append Everything BtuTupleMaker


talkto BtuTupleMaker {
    listToDump set myB0ToPi0Pi0

    fillMC set true

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsInt       set "nTracks nGoodTrkLoose"
    eventTagsFloat     set "R2All"

    mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    ntpBlockConfigs set "B0    B0     2 100"
    ntpBlockConfigs set "pi0   pi0    2 100"
    ntpBlockConfigs set "gamma   gamma    0  30"

    ntpBlockContents set "B0   : Mass CMMomentum MCIdx UsrData(myB0ToPi0Pi0)"
    ntpBlockContents set "pi0  : Mass VtxChi2 MCIdx "
    ntpBlockContents set "gamma: Momentum MCIdx"

    ntpAuxListContents set "pi0 : pi0Loose : _unc_ : Mass"

#    ntpBlockContents set "TRK  : MCIdx"

#    fillAllCandsInList set "pi0   pi0Loose"
#    fillAllCandsInList set "TRK   ChargedTracks"

#    trkExtraContents set Eff:ave,charge
#    trkExtraContents set PidMap:KSelectorsMap,piSelectorsMap

    gamExtraContents set EMC

    baseTrackList   set ChargedTracks
#    basePhotonList  set GoodPhotonLoose

    wantATrkBlock   set false

    show
}

#
#  Turn off some specialty items
#
module disable MyDstarAnalysis
module disable MyK0Analysis
module disable MyMiniAnalysis
module disable BtuMyAnalysis
#module disable BtuTupleMaker

path list
if [info exists NEvents] {
   ev begin -nev $NEvents
} else {
  ev begin 
}

ErrMsg trace "completed OK"
exit
