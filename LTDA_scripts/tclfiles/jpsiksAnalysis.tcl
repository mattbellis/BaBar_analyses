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

#..Print Frequency
FwkCfgVar PrintFreq 1000

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


sourceFoundFile CompositionSequences/CompPsiInitSequence.tcl

#sourceFoundFile UsrTools/UsrDataProcs.tcl
#enableReadUsrData
#readEventUsrData myEventData
#readCandUsrData xxx

#seq append BetaMiniPhysicsSequence -a  PidSequence  CompPsiInitSequence


#### Do SimpleComposition
seq create SmpMyB0Sequence

# ->  B0
mod clone SmpMakerDefiner myB0ToJpsiKs
seq append SmpMyB0Sequence myB0ToJpsiKs
catch { setProduction myB0ToJpsiKs }
talkto myB0ToJpsiKs {
    debug              set f
    verbose            set f
    decayMode          set "B0 -> J/psi K_S0"
    #daughterListNames  set "JPsiLooseChm"
    daughterListNames  set "JPsiLooseMuMu"
    daughterListNames  set "KsDefault"

    fittingAlgorithm   set "Add4"
    preFitSelectors    set "Mass 4.0:7.0"
    #preFitSelectors    set "DeltaE -0.5:0.5"
    #postFitSelectors   set "Mes 4.0:7.0"
    #postFitSelectors   set "DeltaE -0.2:0.2"

    createUsrData  set t
}

## Add Analysis module
##
path append Everything SmpMyB0Sequence
path append Everything BtuTupleMaker


talkto BtuTupleMaker {
    listToDump set myB0ToJpsiKs

    fillMC set true

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsInt       set "nTracks nGoodTrkLoose"
    eventTagsFloat     set "R2All"

    mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    ntpBlockConfigs set "B0    B0     2 100"
    ntpBlockConfigs set "J/psi Jpsi   2 20"
    ntpBlockConfigs set "K_S0  KS     2  30"


    ntpBlockConfigs set "e+    Elec  4  20"
    ntpBlockConfigs set "mu+   Mu    0  20"
    ntpBlockConfigs set "pi+   Pi    0  30"
    ntpBlockConfigs set "gamma gamma 0  30"

    ntpBlockToTrk   set "Elec Mu Pi "

    ntpBlockContents set "B0   : Mass CMMomentum MCIdx UsrData(myB0ToJpsiKs)"
    ntpBlockContents set "Jpsi : Mass VtxChi2 MCIdx "
    ntpBlockContents set "KS: Mass Momentum VtxChi2 MCIdx"
    ntpBlockContents set "Pi   : Momentum MCIdx"
    ntpBlockContents set "Elec   : Momentum MCIdx"
    ntpBlockContents set "Mu     : Momentum MCIdx"
    ntpBlockContents set "gamma  : "
    ntpBlockContents set "TRK  : MCIdx"

#    trkExtraContents set PidMap:KSelectorsMap,piSelectorsMap
#    trkExtraContents set HOTS:detailSVT

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

mod talk EvtCounter
  printFreq set $PrintFreq
  exit


path list
if [info exists NEvents] {
   ev begin -nev $NEvents
} else {
  ev begin 
}

ErrMsg trace "completed OK"
exit
