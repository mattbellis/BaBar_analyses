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
FwkCfgVar histFileName "MyMiniAnalysis.root"

##
sourceFoundFile BetaMiniUser/btaMiniPhysics.tcl


sourceFoundFile CompositionSequences/CompPsiInitSequence.tcl

#sourceFoundFile UsrTools/UsrDataProcs.tcl
#enableReadUsrData
#readEventUsrData myEventData
#readCandUsrData xxx

#seq append BetaMiniPhysicsSequence -a  PidSequence  CompPsiInitSequence


#####################################################################
#### Do SimpleComposition
seq create SmpMyDummy

# phiphi
mod clone SmpMakerDefiner myDummy
seq append SmpMyDummy myDummy
catch { setProduction myDummy}

#####################################################################
# Set up the Smp stuff
talkto myDummy {
    debug              set f
    verbose            set f
    decayMode          set "dummy00_1 -> phi phi"
    daughterListNames  set "phiTightPID"
    daughterListNames  set "phiTightPID"

    fittingAlgorithm   set "Cascade"
    fitConstraints     set "Geo"
    preFitSelectors    set "Mass 1.0:12.0"

    createUsrData  set t
}

#####################################################################
## Add Analysis module
##
path append Everything SmpMyDummy

mod  clone  BtuTupleMaker BtuTupleMaker_myparticle
path append Everything    BtuTupleMaker_myparticle

#####################################################################

talkto BtuTupleMaker_myparticle {
  
    ntupleName set ntp1_phiphi
    listToDump set myDummy

    fillMC set true

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsInt       set "nTracks nGoodTrkLoose"
    eventTagsFloat     set "R2All"

    mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    ntpBlockConfigs set "dummy00_1  dummy00_1     2   100"
    ntpBlockConfigs set "phi        phi           2   20"
    ntpBlockConfigs set "K+         K             0   30"

    ntpBlockContents set "dummy00_1 : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(myDummy)"
    ntpBlockContents set "phi       : Mass Momentum CMMomentum MCIdx "
    ntpBlockContents set "K         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "TRK       : MCIdx"

    ntpBlockToTrk   set "K "

    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    trkExtraContents set HOTS:detailSVT

    show
}

#########################
#####################################################################
#####################################################################
#
#  Turn off some specialty items
#
module disable MyDstarAnalysis
module disable MyK0Analysis
module disable MyMiniAnalysis
module disable BtuMyAnalysis
#module disable BtuTupleMaker

# Needed to put this in for some reason. Found a mention
# of this on Hypernews. 
sequence disable SmpLambdaCProdSequence

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
