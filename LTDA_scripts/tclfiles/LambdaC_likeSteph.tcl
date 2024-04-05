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
createsmpmerger BetaMiniPhysicsSequence AllLambdaC {
  inputListNames    set "LambdaCTopKpi"
  disableCloneCheck set true
}
sequence append BetaMiniPhysicsSequence CompPsiInitSequence
#####################################################################
#####################################################################
# Refit the LambdaC to constrain the mass
createsmprefitter BetaMiniPhysicsSequence MyConstLcTopKpi {
  decayMode         set "Lambda_c+ -> p+ K- pi+"
  unrefinedListName set "LambdaCTopKpi"
  fittingAlgorithm  set "TreeFitter"
  fitConstraints    set "Mass"
  fitConstraints    set "Geo"
  postFitSelectors  set "Flight"
  postFitSelectors  set "FlightSignificance"
  createUsrData     set t
}
#####################################################################
createsmpmerger BetaMiniPhysicsSequence AllConstLambdaC {
  inputListNames    set "MyConstLcTopKpi"
  disableCloneCheck set true
}   

#####################################################################
# NEW STUFF
#####################################################################
#####################################################################
#### Do SimpleComposition

set leptons {
{"mu" "mu-" "muCombinedVeryLooseFakeRate" "mu" "0"}
{"ebr" "e-" "eBremReco" "e" "4"}}

foreach lep $leptons {

  set l0 [lindex $lep 0]
  set l1 [lindex $lep 1]
  set l2 [lindex $lep 2]
  set l3 [lindex $lep 3]
  set l4 [lindex $lep 4]

createsmpmaker BetaMiniPhysicsSequence my_fakeB_$l0 {
  debug              set f
  verbose            set f
  decayMode          set "dummy00_1 -> Lambda_c+ anti-p-"
  daughterListNames  set "AllConstLambdaC"
  daughterListNames  set "pLHVeryLoose"
  fittingAlgorithm   set "TreeFitter"
  fitConstraints     set "Geo"
  postFitSelectors   set "Mass"
  postFitSelectors   set "ProbChiSq"
  postFitSelectors   set "Flight"
  postFitSelectors   set "FlightSignificance"
  createUsrData      set t
}

###### Constrained
createsmpmaker BetaMiniPhysicsSequence myB_uncL_$l0 {
  debug              set f
  verbose            set f
  decayMode          set "B0 -> Lambda_c+ $l1"
  daughterListNames  set "AllConstLambdaC"
  daughterListNames  set "$l2"
  fittingAlgorithm   set "TreeFitter"
  fitConstraints     set "Geo"
  preFitSelectors    set "Mass    5.0:5.5"
  preFitSelectors    set "DeltaE -0.5:0.5"
  preFitSelectors    set "Mes"
  preFitSelectors    set "Mmiss"
  postFitSelectors   set "Mass"
  postFitSelectors   set "DeltaE"
  postFitSelectors   set "Mes"
  postFitSelectors   set "Mmiss"
  postFitSelectors   set "ProbChiSq"
  postFitSelectors   set "Flight"
  postFitSelectors   set "FlightSignificance"
  createUsrData      set t
}
###### Constrained
createsmprefitter BetaMiniPhysicsSequence myB_conL_$l0 {
  debug              set f
  verbose            set f
  decayMode          set "B0 -> Lambda_c+ $l1"
  unrefinedListName  set "myB_uncL_$l0"
  fittingAlgorithm   set "TreeFitter"
  fitConstraints     set "Geo"
  #fitSettings        set "InvalidateFit"
  fitSettings        set "UpdateDaughters"
  preFitSelectors    set "Mass    5.0:5.5"
  preFitSelectors    set "DeltaE -0.5:0.5"
  preFitSelectors    set "Mes"
  preFitSelectors    set "Mmiss"
  postFitSelectors   set "Mass"
  postFitSelectors   set "DeltaE"
  postFitSelectors   set "Mes"
  postFitSelectors   set "Mmiss"
  postFitSelectors   set "ProbChiSq"
  postFitSelectors   set "Flight"
  postFitSelectors   set "FlightSignificance"
  createUsrData      set t
}
#################################################################

#####################################################################
# Set up the Smp stuff
#################################################################
################# NEW #####################################
createsmpsublister BetaMiniPhysicsSequence subXlistComp_$l0 {
   unrefinedListName set "my_fakeB_$l0"
   isCloneOfListName set "myB_conL_$l0"
   whatToDoWithCloneList set AcceptOverlaps
}
## subXlistComp will have all X candidates that do NOT overlap with the B

createsmpmerger BetaMiniPhysicsSequence AllB_$l0 {
  inputListNames    set "myB_conL_$l0"
  #inputListNames    set "myB_uncL_$l0"
  inputListNames    set "subXlistComp_$l0"
  disableCloneCheck set true
  createUsrData     set true
}
}

#####################################################################
## Add Analysis module
#####################################################################
foreach lep $leptons {

  set l0 [lindex $lep 0]
  set l1 [lindex $lep 1]
  set l2 [lindex $lep 2]
  set l3 [lindex $lep 3]
  set l4 [lindex $lep 4]


  mod  clone  BtuTupleMaker BtuTupleMaker_$l0
  path append Everything BtuTupleMaker_$l0

  talkto BtuTupleMaker_$l0 {

    ntupleName set ntp_LambdaC$l0
    listToDump set AllB_$l0

    fillMC set true

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsInt       set "nTracks nGoodTrkLoose nChargedTracks" 
    eventTagsFloat     set "R2 R2All thrustMag thrustMagAll thrustCosTh thrustCosThAll thrustPhi thrustPhiAll sphericityAll"
    
    mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    # Our dummy baryon-antibaryon composite particles
    ntpBlockConfigs set "dummy00_1  dummy         2   100"

    ntpBlockConfigs set "B0         B             2   100"
    ntpBlockConfigs set "Lambda_c+  LambdaC       3   20"
    ntpBlockConfigs set "$l1        $l0           $l4 100"
    ntpBlockConfigs set "p+         p             0   20"
    ntpBlockConfigs set "pi+        pi            0   30"
    ntpBlockConfigs set "K+         K             0   30"
    ntpBlockConfigs set "gamma      gamma         0   90"

    ntpBlockContents set "dummy     : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(my_fakeB_$l0) ShapeVars"
    ntpBlockContents set "B         : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(myB_uncL_$l0) ShapeVars"
    ntpBlockContents set "LambdaC   : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(MyConstLcTopKpi) Flight FlightBS"
    ntpBlockContents set "pi        : Momentum CMMomentum MCIdx"
    ntpBlockContents set "p         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "K         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "$l0       : Momentum CMMomentum MCIdx"
    ntpBlockContents set "gamma     : Momentum CMMomentum MCIdx"
    ntpBlockContents set "TRK       : Momentum CMMomentum MCIdx"


    ntpAuxListContents set "B       : myB_conL_$l0 : _con_ : Mass Momentum CMMomentum Vertex VtxChi2 UsrData(myB_conL_$l0)"
    ntpAuxListContents set "LambdaC : AllLambdaC   : _unc_ : Mass Momentum CMMomentum Vertex VtxChi2"

    fillAllCandsInList set "TRK ChargedTracks"

#..Want to save all CalorNeutrals in the gamma block
    gamExtraContents set EMC


    ntpBlockToTrk   set "p $l0 pi K "

    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    trkExtraContents set HOTS:detailSVT

    ###########################################
    # This will give me two different daughter candidates
    # if that's what happens.
    # Trying to set this as true for TRK's only?
    ############################################
    checkClones set false
    checkCloneBlocks set "p pi $l0 TRK"

    show
  }
}

#####################################################################
#  Turn off some specialty items
#####################################################################
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
