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

#############################################################
# BremRecoElectrons!!!!!!!!!!!!!! ###########################
#############################################################
#sourceFoundFile CompositionSequences/CompPsiInitSequence.tcl
sourceFoundFile CompositionSequences/CompPsiInitSequence.tcl

#sequence enable eBremRecoPidHllMerge
#sequence enable CompProdCreateSequence
#sequence enable CompBremSelectors
#sourceFoundFile UsrTools/UsrDataProcs.tcl
#enableReadUsrData
#readEventUsrData myEventData
#readCandUsrData xxx

#seq append BetaMiniPhysicsSequence -a  PidSequence  CompPsiInitSequence


#####################################################################
# NEW STUFF
#####################################################################
createsmpmerger BetaMiniPhysicsSequence AllDc {
  inputListNames    set "DcToKPiPiLoose"
  disableCloneCheck set true
}
sequence append BetaMiniPhysicsSequence CompPsiInitSequence
#####################################################################
#####################################################################
# Refit the LambdaC to constrain the mass
createsmprefitter BetaMiniPhysicsSequence MyConstDctoKpipi {
  decayMode         set "D+ -> K- pi+ pi+"
  unrefinedListName set "DcToKPiPiLoose"
  fittingAlgorithm  set "TreeFitter"
  fitConstraints    set "Mass"
  fitConstraints    set "Geo"
}
#####################################################################
createsmpmerger BetaMiniPhysicsSequence AllConstDc {
  inputListNames    set "MyConstDctoKpipi"
  #inputListNames    set "MyConstLcTopConstKs"
  #inputListNames    set "MyConstLcTopConstKspipi"
  #inputListNames    set "MyConstLcToConstLzpi"
  #inputListNames    set "MyConstLcToConstLzpipipi"
  disableCloneCheck set true
}   

#####################################################################
# NEW STUFF
#####################################################################
#####################################################################
#### Do SimpleComposition

createsmpmaker BetaMiniPhysicsSequence myB_uncDpi {
  debug              set f
  verbose            set f
  decayMode          set "B0 -> D+ pi-"
  daughterListNames  set "AllConstDc"
  daughterListNames  set "GoodTracksVeryLoose"
  fittingAlgorithm   set "TreeFitter"
  fitConstraints     set "Geo"
  preFitSelectors    set "Mass    5.1:5.5"
  preFitSelectors    set "DeltaE"
  preFitSelectors    set "Mes"
  preFitSelectors    set "Mmiss"
  postFitSelectors   set "Mass"
  postFitSelectors   set "DeltaE"
  postFitSelectors   set "Mes"
  postFitSelectors   set "Mmiss"
  postFitSelectors   set "ProbChiSq"
  createUsrData      set t
}
###### Constrained
createsmprefitter BetaMiniPhysicsSequence myB_conDpi {
  debug              set f
  verbose            set f
  decayMode          set "B0 -> D+ pi-"
  unrefinedListName  set "myB_uncDpi"
  fittingAlgorithm   set "TreeFitter"
  fitConstraints     set "Geo"
  fitSettings        set "InvalidateFit"
  fitSettings        set "UpdateDaughters"
  preFitSelectors    set "Mass    5.1:5.5"
  preFitSelectors    set "DeltaE"
  preFitSelectors    set "Mes"
  preFitSelectors    set "Mmiss"
  postFitSelectors   set "Mass"
  postFitSelectors   set "DeltaE"
  postFitSelectors   set "Mes"
  postFitSelectors   set "Mmiss"
  postFitSelectors   set "ProbChiSq"
  createUsrData      set t
}
#################################################################

#####################################################################
# Set up the Smp stuff
#################################################################
################# NEW #####################################
createsmpmerger BetaMiniPhysicsSequence AllB_Dpi {
  inputListNames    set "myB_uncDpi"
  inputListNames    set "myB_conDpi"
  disableCloneCheck set true
  createUsrData     set true
}


#####################################################################
## Add Analysis module
#####################################################################
mod  clone  BtuTupleMaker BtuTupleMaker_Dpi
path append Everything BtuTupleMaker_Dpi

talkto BtuTupleMaker_Dpi {

  ntupleName set ntp1_Dpi
  listToDump set AllB_Dpi

  fillMC set true

  eventBlockContents set "EventID CMp4 BeamSpot"
  eventTagsInt       set "nTracks nGoodTrkLoose nChargedTracks" 
  eventTagsFloat     set "R2 R2All thrustMag thrustMagAll thrustCosTh thrustCosThAll thrustPhi thrustPhiAll sphericityAll"
  

  mcBlockContents    set "Mass CMMomentum Momentum Vertex"

  ntpBlockConfigs set "B0         B             2   100"
  ntpBlockConfigs set "D+         Dc            3   20"
  ntpBlockConfigs set "pi+        pi            0   30"
  ntpBlockConfigs set "K+         K             0   30"

  ntpBlockContents set "B         : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(myB_uncDpi) ShapeVars"
  ntpBlockContents set "Dc        : Mass Momentum CMMomentum MCIdx Vertex VtxChi2"
  ntpBlockContents set "pi        : Momentum CMMomentum MCIdx"
  ntpBlockContents set "K         : Momentum CMMomentum MCIdx"

  ntpBlockContents set "TRK  : MCIdx Momentum CMMomentum"

  ntpAuxListContents set "B       : myB_conDpi   : _con_ : Mass Momentum CMMomentum UsrData(myB_conDpi)"
  ntpAuxListContents set "Dc      : AllDc        : _unc_ : Mass Momentum CMMomentum Vertex VtxChi2"


  ################# Write out all the charged tracks
  fillAllCandsInList set "TRK ChargedTracks"

#..Want to save all CalorNeutrals in the gamma block
  gamExtraContents set EMC

  ntpBlockToTrk   set "pi K "

  trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
  trkExtraContents set HOTS:detailSVT

  show
}

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
