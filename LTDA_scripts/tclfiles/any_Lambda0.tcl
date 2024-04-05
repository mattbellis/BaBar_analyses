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
##### DO I NEED THIS???? ############
createsmpmerger BetaMiniPhysicsSequence AllLambda0 {
  inputListNames    set "LambdaLoose"
  disableCloneCheck set true
}
sequence append BetaMiniPhysicsSequence CompPsiInitSequence

#######################################################
# Define some mesons to loop over
#######################################################
set leptons {
{"mu" "mu-" "muCombinedVeryLooseFakeRate" "mu" "0"}
{"ebr" "e-" "eBremReco" "e" "4"}}

set mesons {
{"pi" "pi+" "ChargedTracks" "pi" }
{"K"  "K+"  "ChargedTracks" "K"  }}

foreach mes $mesons {
  foreach lep $leptons {

    set m0 [lindex $mes 0]
    set m1 [lindex $mes 1]
    set m2 [lindex $mes 2]
    set m3 [lindex $mes 3]

    set l0 [lindex $lep 0]
    set l1 [lindex $lep 1]
    set l2 [lindex $lep 2]
    set l3 [lindex $lep 3]
    set l4 [lindex $lep 4]

    #####################################################################
    #####################################################################
    # Refit the Lambda0 to constrain the mass
    createsmpmaker BetaMiniPhysicsSequence My_unc_L0_to_$m3$l3 {
      decayMode          set "Lambda0 -> $l1 $m1"
      #unrefinedListName  set "LambdaLoose"
      daughterListNames  set "$l2"
      daughterListNames  set "$m2"
      fittingAlgorithm   set "TreeFitter"
      fitConstraints     set "Geo"
      preFitSelectors    set "Mass 1.105:1.125"
      postFitSelectors   set "ProbChiSq 0.001:"
      postFitSelectors   set "Flight"
      postFitSelectors   set "FlightSignificance"
      createUsrData      set t
    }
    #####################################################################
    #####################################################################
    #createsmprefitter BetaMiniPhysicsSequence My_con_L0_to_$m3$l3 {
      #decayMode          set "Lambda0 -> $l1 $m1"
      #unrefinedListName  set "My_unc_L0_to_$m3$l3"
      #fittingAlgorithm   set "TreeFitter"
      #fitConstraints     set "Geo"
      #fitConstraints     set "Mass"
      #preFitSelectors    set "Mass 1.105:1.125"
      #postFitSelectors   set "ProbChiSq 0.001:"
      #postFitSelectors   set "Flight"
      #postFitSelectors   set "FlightSignificance"
      #createUsrData      set t
    #}

    ################# NEW #####################################

    createsmpmerger BetaMiniPhysicsSequence All_L0_$m3$l3 {
      #inputListNames    set "My_con_L0_to_$m3$l3"
      inputListNames    set "My_unc_L0_to_$m3$l3"
      disableCloneCheck set true
      createUsrData     set true
    }
  }
}
#####################################################################
#####################################################################
# Refit the Lambda0 to constrain the mass
#createsmprefitter BetaMiniPhysicsSequence MyConstL0_to_mu_pi {
  #decayMode         set "Lambda0 -> mu+ pi-"
  #unrefinedListName set "LambdaLoose"
  #fittingAlgorithm  set "TreeFitter"
  #fitConstraints    set "Mass"
  #fitConstraints    set "Geo"
  #postFitSelectors  set "Flight"
  #postFitSelectors  set "FlightSignificance"
  #createUsrData     set t
#}
#####################################################################
#createsmpmerger BetaMiniPhysicsSequence AllConstLambda0 {
  #inputListNames    set "MyConstL0"
  #disableCloneCheck set true
#}   

#####################################################################
#####################################################################
# NEW STUFF
#####################################################################
#####################################################################
#### Do SimpleComposition

#####################################################################
## Add Analysis module
#####################################################################
foreach mes $mesons {
  foreach lep $leptons {

    set m0 [lindex $mes 0]
    set m1 [lindex $mes 1]
    set m2 [lindex $mes 2]
    set m3 [lindex $mes 3]

    set l0 [lindex $lep 0]
    set l1 [lindex $lep 1]
    set l2 [lindex $lep 2]
    set l3 [lindex $lep 3]
    set l4 [lindex $lep 4]

  mod  clone  BtuTupleMaker BtuTupleMaker_$m3$l3
  path append Everything BtuTupleMaker_$m3$l3

  talkto BtuTupleMaker_$m3$l3 {

    ntupleName set ntp_$m3$l3
    listToDump set All_L0_$m3$l3

    fillMC set true

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsInt       set "nTracks nGoodTrkLoose nChargedTracks" 
    eventTagsFloat     set "R2 R2All thrustMag thrustMagAll thrustCosTh thrustCosThAll thrustPhi thrustPhiAll sphericityAll"

    mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    # Our dummy baryon-antibaryon composite particles
    ntpBlockConfigs set "Lambda0    Lambda0       2   20"
    ntpBlockConfigs set "$l1        $l0           $l4 100"
    ntpBlockConfigs set "$m1        $m0           0   30"
    ntpBlockConfigs set "gamma      gamma         0   90"

    #ntpBlockContents set "Lambda0   : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(My_con_L0_to_$m3$l3) Flight FlightBS"
    ntpBlockContents set "Lambda0   : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(My_unc_L0_to_$m3$l3) Flight FlightBS"
    ntpBlockContents set "$m0       : Momentum CMMomentum MCIdx"
    ntpBlockContents set "$l0       : Momentum CMMomentum MCIdx"
    ntpBlockContents set "gamma     : Momentum CMMomentum MCIdx"
    #ntpBlockContents set "TRK       : Momentum CMMomentum MCIdx"

    #ntpAuxListContents set "Lambda0 : My_unc_L0_to_$m3$l3   : _unc_ : Mass Momentum CMMomentum Vertex VtxChi2"

    #fillAllCandsInList set "TRK ChargedTracks"

#..Want to save all CalorNeutrals in the gamma block
    gamExtraContents set EMC

    ntpBlockToTrk   set "$l0 $m0 "

    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    trkExtraContents set HOTS:detailSVT

    ###########################################
    # This will give me two different daughter candidates
    # if that's what happens.
    # Trying to set this as true for TRK's only?
    ############################################
    checkClones set false
    #checkCloneBlocks set "$m0 $l0 TRK" 
    checkCloneBlocks set "$m0 $l0" 

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
