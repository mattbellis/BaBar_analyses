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
sourceFoundFile CompositionSequences/CompPsiInitSequence.tcl

#####################################################################
# NEW STUFF
#####################################################################
createsmpmerger BetaMiniPhysicsSequence AllD0 {
  inputListNames    set "D0ToKPiLoose"
  disableCloneCheck set true
}
sequence append BetaMiniPhysicsSequence CompPsiInitSequence
#####################################################################
#####################################################################
# Refit the LambdaC to constrain the mass
createsmprefitter BetaMiniPhysicsSequence MyConstD0{
  decayMode         set "D0 -> K- pi+"
  unrefinedListName set "D0ToKpiLoose"
  fittingAlgorithm  set "TreeFitter"
  fitConstraints    set "Mass"
  fitConstraints    set "Geo"
}
#####################################################################
createsmpmerger BetaMiniPhysicsSequence AllConstD0 {
  inputListNames    set "MyConstD0"
  disableCloneCheck set true
}   

#####################################################################
# NEW STUFF
#####################################################################
#####################################################################
#### Do SimpleComposition
createsmpmaker BetaMiniPhysicsSequence my_uncDstar {
  debug              set f
  verbose            set f
  decayMode          set "D*+ -> D0 pi+"
  daughterListNames  set "AllConstD0"
  daughterListNames  set "GoodTracksVeryLoose"
  fittingAlgorithm   set "TreeFitter"
  fitConstraints     set "Geo"
  preFitSelectors    set "Mass    1.9:2.1"
  createUsrData      set t
}
###### Constrained
createsmprefitter BetaMiniPhysicsSequence my_conDstar {
  debug              set f
  verbose            set f
  decayMode          set "D*+ -> D0 pi+"
  unrefinedListName  set "my_uncDstar"
  fittingAlgorithm   set "TreeFitter"
  fitConstraints     set "Geo"
  fitSettings        set "InvalidateFit"
  fitSettings        set "UpdateDaughters"
  preFitSelectors    set "Mass    1.9:2.1"
  createUsrData      set t
}
#################################################################
#####################################################################
#### Do SimpleComposition
createsmpmaker BetaMiniPhysicsSequence my_uncD1 {
  debug              set f
  verbose            set f
  decayMode          set "D_10 -> D*+ pi-"
  daughterListNames  set "my_uncDstar"
  daughterListNames  set "GoodTracksVeryLoose"
  fittingAlgorithm   set "TreeFitter"
  fitConstraints     set "Geo"
  preFitSelectors    set "Mass    2.2:2.6"
  createUsrData      set t
}
###### Constrained
createsmprefitter BetaMiniPhysicsSequence my_conD1 {
  debug              set f
  verbose            set f
  decayMode          set "D_10 -> D*+ pi+"
  unrefinedListName  set "my_uncD1"
  fittingAlgorithm   set "TreeFitter"
  fitConstraints     set "Geo"
  fitSettings        set "InvalidateFit"
  fitSettings        set "UpdateDaughters"
  preFitSelectors    set "Mass    2.2:2.6"
  createUsrData      set t
}
#################################################################


#####################################################################
# Set up the Smp stuff
#################################################################
################# NEW #####################################
createsmpmerger BetaMiniPhysicsSequence All_D {
  inputListNames    set "my_uncDstar"
  inputListNames    set "my_conDstar"
  inputListNames    set "my_uncD1"
  inputListNames    set "my_conD1"
  disableCloneCheck set true
  createUsrData     set true
}


#####################################################################
## Add Analysis module
#####################################################################
mod  clone  BtuTupleMaker BtuTupleMaker_D1
path append Everything BtuTupleMaker_D1

talkto BtuTupleMaker_D1 {

  ntupleName set ntp1_D1
  listToDump set All_D

  fillMC set true

  eventBlockContents set "EventID CMp4 BeamSpot"
  eventTagsInt       set "nTracks nGoodTrkLoose nChargedTracks" 
  eventTagsFloat     set "R2 R2All thrustMag thrustMagAll thrustCosTh thrustCosThAll thrustPhi thrustPhiAll sphericityAll"
  

  mcBlockContents    set "Mass CMMomentum Momentum Vertex"

  ntpBlockConfigs set "D_10       D_10          2   20"
  ntpBlockConfigs set "D*+        Dstarp        2   20"
  ntpBlockConfigs set "D0         D0            2   20"
  ntpBlockConfigs set "pi+        pi            0   30"
  ntpBlockConfigs set "K+         K             0   30"

  ntpBlockContents set "D_10      : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(my_uncD1) ShapeVars"
  ntpBlockContents set "Dstarp    : Mass Momentum CMMomentum MCIdx Vertex VtxChi2"
  ntpBlockContents set "D0        : Mass Momentum CMMomentum MCIdx Vertex VtxChi2"
  ntpBlockContents set "pi        : Momentum CMMomentum MCIdx"
  ntpBlockContents set "K         : Momentum CMMomentum MCIdx"

  ntpBlockContents set "TRK  : MCIdx Momentum CMMomentum"

  ntpAuxListContents set "D_10    : my_conD1     : _con_ : Mass Momentum CMMomentum UsrData(my_conD1)"
  ntpAuxListContents set "Dstarp  : my_uncDstar  : _unc_ : Mass Momentum CMMomentum Vertex VtxChi2"
  ntpAuxListContents set "D0      : AllD0        : _unc_ : Mass Momentum CMMomentum Vertex VtxChi2"


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
