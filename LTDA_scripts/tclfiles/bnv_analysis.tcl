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
  inputListNames    set "LambdaDefault"
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
#createsmpmerger BetaMiniPhysicsSequence AllAntiLambda0 {
  #inputListNames    set "LambdaDefault"
  #disableCloneCheck set true
#}
######################################################################
######################################################################
## Refit the Lambda0 to constrain the mass
#createsmprefitter BetaMiniPhysicsSequence MyConstAntiL0 {
  #decayMode         set "anti-Lambda0 -> anti-p- pi+"
  #unrefinedListName set "LambdaDefault"
  #fittingAlgorithm  set "TreeFitter"
  #fitConstraints    set "Mass"
  #fitConstraints    set "Geo"
  #postFitSelectors  set "Flight"
  #postFitSelectors  set "FlightSignificance"
  #createUsrData     set t
#}
#####################################################################
#createsmpmerger BetaMiniPhysicsSequence AllConstAntiLambda0 {
#  inputListNames    set "MyConstAntiL0"
#  disableCloneCheck set true
#}   

#####################################################################
# NEW STUFF
#####################################################################
#####################################################################
#### Do SimpleComposition


createsmpmaker BetaMiniPhysicsSequence myB_unc {
  debug              set f
  verbose            set f
  decayMode          set "B+ -> Lambda0 p+"
  daughterListNames  set "AllConstLambda0"
  daughterListNames  set "GoodTracksVeryLoose"
  fittingAlgorithm   set "TreeFitter"
  fitConstraints     set "Geo"
  preFitSelectors    set "Mass    5.0:5.5"
  preFitSelectors    set "DeltaE -1.5:1.5"
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
createsmprefitter BetaMiniPhysicsSequence myB_con {
  debug              set f
  verbose            set f
  decayMode          set "B+ -> Lambda0 p+"
  unrefinedListName  set "myB_unc"
  fittingAlgorithm   set "TreeFitter"
  fitConstraints     set "Geo"
  #fitSettings        set "InvalidateFit"
  fitSettings        set "UpdateDaughters"
  preFitSelectors    set "Mass    5.0:5.5"
  preFitSelectors    set "DeltaE -1.5:1.5"
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
################# NEW #####################################
#createsmpsublister BetaMiniPhysicsSequence AllB {
  #unrefinedListName set "myB_unc"
  #isCloneOfListName set "myB_con"
  #whatToDoWithCloneList set AcceptOverlaps
#}
## subXlistComp will have all X candidates that do NOT overlap with the B

createsmpmerger BetaMiniPhysicsSequence AllB_pLam {
  inputListNames    set "myB_unc"
  inputListNames    set "myB_con"
  disableCloneCheck set true
  createUsrData     set true
}

#####################################################################
## Add Analysis module
#####################################################################
  mod  clone  BtuTupleMaker BtuTupleMaker_B
  path append Everything BtuTupleMaker_B

  talkto BtuTupleMaker_B {

    ntupleName set ntp_B
    listToDump set AllB_pLam

    fillMC set true

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsInt       set "nTracks nGoodTrkLoose nChargedTracks" 
    eventTagsFloat     set "R2 R2All thrustMag thrustMagAll thrustCosTh thrustCosThAll thrustPhi thrustPhiAll sphericityAll"

    mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    # Our dummy baryon-antibaryon composite particles
    ntpBlockConfigs set "B-         B             2   100"
    ntpBlockConfigs set "Lambda0    Lambda0       2   20"
    ntpBlockConfigs set "p+         p             0   20"
    ntpBlockConfigs set "pi-        pi            0   30"

    ntpBlockContents set "B         : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(myB_unc) ShapeVars"
    ntpBlockContents set "Lambda0   : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(MyConstL0) Flight FlightBS"
    ntpBlockContents set "pi        : Momentum CMMomentum MCIdx"
    ntpBlockContents set "p         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "TRK       : Momentum CMMomentum MCIdx"

    ntpAuxListContents set "B       : myB_con: _con_ : Mass Momentum CMMomentum Vertex VtxChi2 UsrData(myB_con)"
    ntpAuxListContents set "Lambda0 : AllLambda0       : _unc_ : Mass Momentum CMMomentum Vertex VtxChi2"

    fillAllCandsInList set "TRK ChargedTracks"

#..Want to save all CalorNeutrals in the gamma block
    gamExtraContents set EMC

    ntpBlockToTrk   set "p pi "

    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    trkExtraContents set HOTS:detailSVT

    ###########################################
    # This will give me two different daughter candidates
    # if that's what happens.
    # Trying to set this as true for TRK's only?
    ############################################
    checkClones set false
    checkCloneBlocks set "p pi TRK" 

    show
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
