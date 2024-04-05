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
createsmpmerger BetaMiniPhysicsSequence AllLambda0 {
  inputListNames    set "DstarChrgKLooseRS"
  disableCloneCheck set true
}
sequence append BetaMiniPhysicsSequence CompPsiInitSequence
#####################################################################
#####################################################################
# Refit the Lambda0 to constrain the mass
createsmprefitter BetaMiniPhysicsSequence MyConstL0 {
  decayMode         set "Lambda0 -> p+ pi-"
  unrefinedListName set "LambdaDefault"
  fittingAlgorithm  set "TreeFitter"
  fitConstraints    set "Mass"
  fitConstraints    set "Geo"
  postFitSelectors  set "Flight"
  postFitSelectors  set "FlightSignificance"
  createUsrData     set t
}
#####################################################################
createsmpmerger BetaMiniPhysicsSequence AllConstLambda0 {
  inputListNames    set "MyConstL0"
  disableCloneCheck set true
}   

#####################################################################
#####################################################################
# Anti-Lambda0's
#####################################################################
#####################################################################
createsmpmerger BetaMiniPhysicsSequence AllAntiLambda0 {
  inputListNames    set "LambdaDefault"
  disableCloneCheck set true
}
#####################################################################
#####################################################################
# Refit the Lambda0 to constrain the mass
createsmprefitter BetaMiniPhysicsSequence MyConstAntiL0 {
  decayMode         set "anti-Lambda0 -> anti-p- pi+"
  unrefinedListName set "LambdaDefault"
  fittingAlgorithm  set "TreeFitter"
  fitConstraints    set "Mass"
  fitConstraints    set "Geo"
  postFitSelectors  set "Flight"
  postFitSelectors  set "FlightSignificance"
  createUsrData     set t
}
#####################################################################
createsmpmerger BetaMiniPhysicsSequence AllConstAntiLambda0 {
  inputListNames    set "MyConstAntiL0"
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

set baryons {
{"Lambda0"          "Lambda0"  "L" "pbar"  "anti-p-" "ap" "L0"}
{"AntiLambda0" "anti-Lambda0" "aL" "p"     "p+"      "p" "AntiL0"}}

foreach bar $baryons {
foreach lep $leptons {

  set b0 [lindex $bar 0]
  set b1 [lindex $bar 1]
  set b2 [lindex $bar 2]
  set b3 [lindex $bar 6]


  # Anti baryons
  set ab0 [lindex $bar 3]
  set ab1 [lindex $bar 4]
  set ab2 [lindex $bar 5]

  set l0 [lindex $lep 0]
  set l1 [lindex $lep 1]
  set l2 [lindex $lep 2]
  set l3 [lindex $lep 3]
  set l4 [lindex $lep 4]


createsmpmaker BetaMiniPhysicsSequence myB_unc$b2$l0 {
  debug              set f
  verbose            set f
  decayMode          set "B- -> K- D*+ D-"
  daughterListNames  set "AllConst$b0"
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
createsmprefitter BetaMiniPhysicsSequence myB_con$b2$l0 {
  debug              set f
  verbose            set f
  decayMode          set "B- -> $b1 $l1"
  unrefinedListName  set "myB_unc$b2$l0"
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
#####################################################################
# Set up the Smp stuff
#################################################################
createsmpmerger BetaMiniPhysicsSequence AllB_$b2$l0 {
  inputListNames    set "myB_con$b2$l0"
  #inputListNames    set "myB_unc$b2$l0"
  inputListNames    set "subXlistComp_$b2$l0"
  disableCloneCheck set true
  createUsrData     set true
}
}
}

#####################################################################
## Add Analysis module
#####################################################################
foreach bar $baryons {
foreach lep $leptons {

  set b0 [lindex $bar 0]
  set b1 [lindex $bar 1]
  set b2 [lindex $bar 2]
  set b3 [lindex $bar 6]

  # Anti baryons
  set ab0 [lindex $bar 3]
  set ab1 [lindex $bar 4]
  set ab2 [lindex $bar 5]

  set l0 [lindex $lep 0]
  set l1 [lindex $lep 1]
  set l2 [lindex $lep 2]
  set l3 [lindex $lep 3]
  set l4 [lindex $lep 4]

  mod  clone  BtuTupleMaker BtuTupleMaker_$b2$l0
  path append Everything BtuTupleMaker_$b2$l0

  talkto BtuTupleMaker_$b2$l0 {

    ntupleName set ntp_$b0$l0
    listToDump set AllB_$b2$l0

    fillMC set true

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsInt       set "nTracks nGoodTrkLoose nChargedTracks" 
    eventTagsFloat     set "R2 R2All thrustMag thrustMagAll thrustCosTh thrustCosThAll thrustPhi thrustPhiAll sphericityAll"

    mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    # Our dummy baryon-antibaryon composite particles
    ntpBlockConfigs set "B-         B             2   100"
    ntpBlockConfigs set "$b1        Lambda0       2   20"
    ntpBlockConfigs set "$l1        $l0           $l4 100"
    ntpBlockConfigs set "p+         p             0   20"
    ntpBlockConfigs set "pi-        pi            0   30"
    ntpBlockConfigs set "gamma      gamma         0   90"

    ntpBlockContents set "B         : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(myB_unc$b2$l0) ShapeVars"
    ntpBlockContents set "Lambda0   : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(MyConst$b3) Flight FlightBS"
    ntpBlockContents set "pi        : Momentum CMMomentum MCIdx"
    ntpBlockContents set "p         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "$l0       : Momentum CMMomentum MCIdx"
    ntpBlockContents set "gamma     : Momentum CMMomentum MCIdx"
    ntpBlockContents set "TRK       : Momentum CMMomentum MCIdx"

    ntpAuxListContents set "B       : myB_con$b2$l0: _con_ : Mass Momentum CMMomentum Vertex VtxChi2 UsrData(myB_con$b2$l0)"
    ntpAuxListContents set "Lambda0 : All$b0       : _unc_ : Mass Momentum CMMomentum Vertex VtxChi2"

    fillAllCandsInList set "TRK ChargedTracks"

#..Want to save all CalorNeutrals in the gamma block
    gamExtraContents set EMC

    ntpBlockToTrk   set "p $l0 pi "

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
