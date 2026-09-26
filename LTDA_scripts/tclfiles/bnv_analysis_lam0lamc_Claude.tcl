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
  #disableCloneCheck set true
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

#==================================================================
# 1. Mass-constrained intermediate states used INSIDE the Lambda_c+
#    These must be built from the same loose daughter lists that the
#    pre-built LambdaC composites use (KsLoose_LambdaC, Lambda_LambdaC),
#    so that createsmprefiner can match the candidates.
#==================================================================
createsmprefitter BetaMiniPhysicsSequence MyConstKs {
  decayMode         set "K_S0 -> pi+ pi-"
  unrefinedListName set "KsDefault"
  createUsrData     set  true
  fittingAlgorithm  set "TreeFitter"
  preFitSelectors   set "Mass 0.45:0.54"
  postFitSelectors  set "ProbChiSq 0.:"
  postFitSelectors  set "FlightSignificance 0.:"
  fitConstraints    set "Mass"
  fitConstraints    set "Geo"
  #fitSettings       set "UpdateDaughters"
}

#####################################################################
#####################################################################
createsmpmaker BetaMiniPhysicsSequence MyLcTopKpi {
  decayMode         set "Lambda_c+ -> p+ K- pi+"
  daughterListNames set "pLHVeryLoose"
  daughterListNames set "KLHVeryLoose"
  daughterListNames set "ChargedTracks"
  fittingAlgorithm   set "Cascade"
  fitConstraints     set "Geo"
  preFitSelectors    set "Mass 2.220:2.350"
  postFitSelectors   set "Mass 2.220:2.350"
  postFitSelectors   set "ProbChiSq 0.00001:"
  createUsrData      set true
}
######################
#createsmprefiner BetaMiniPhysicsSequence MyConstLcTopKpi {
createsmprefitter BetaMiniPhysicsSequence MyConstLcTopKpi {
  decayMode         set "Lambda_c+ -> p+ K- pi+"
  unrefinedListName set "MyLcTopKpi"
  fittingAlgorithm  set "TreeFitter"
  fitConstraints     set "Mass"
  preFitSelectors    set "Mass 2.220:2.350"
  postFitSelectors   set "Mass 2.220:2.350"
  #fitSettings        set "UpdateDaughters"
  createUsrData      set true
}
#####################################################################
#####################################################################
createsmpmaker BetaMiniPhysicsSequence MyLcTopKs {
  decayMode         set "Lambda_c+ -> p+ K_S0"
  daughterListNames set "pLHVeryLoose"
  daughterListNames set "MyConstKs"
  fittingAlgorithm  set "Cascade"
  fitConstraints    set "Geo"
  preFitSelectors    set "Mass 2.220:2.350"
  postFitSelectors   set "Mass 2.220:2.350"
  postFitSelectors   set "ProbChiSq 0.00001:"
  createUsrData     set true
}

#####################
#createsmprefiner BetaMiniPhysicsSequence MyConstLcTopKs {
createsmprefitter BetaMiniPhysicsSequence MyConstLcTopKs {
  decayMode         set "Lambda_c+ -> p+ K_S0"
  unrefinedListName set "MyLcTopKs"
  fittingAlgorithm  set "TreeFitter"
  fitConstraints    set "Mass"
  preFitSelectors    set "Mass 2.220:2.350"
  postFitSelectors   set "Mass 2.220:2.350"
  postFitSelectors   set "ProbChiSq 0.00001:"
  #fitSettings        set "UpdateDaughters"
  createUsrData     set true
}


#####################################################################
#####################################################################
createsmpmaker BetaMiniPhysicsSequence MyLcTopKspipi {
  decayMode         set "Lambda_c+ -> p+ K_S0 pi+ pi-"
  daughterListNames set "pLHVeryLoose"
  daughterListNames set "MyConstKs"
  daughterListNames set "ChargedTracks"
  daughterListNames set "ChargedTracks"
  fittingAlgorithm  set "Cascade"
  fitConstraints    set "Geo"
  preFitSelectors    set "Mass 2.220:2.350"
  postFitSelectors   set "Mass 2.220:2.350"
  postFitSelectors   set "ProbChiSq 0.00001:"
  createUsrData     set true
}

#####################
#createsmprefiner BetaMiniPhysicsSequence MyConstLcTopKspipi {
createsmprefitter BetaMiniPhysicsSequence MyConstLcTopKspipi {
  decayMode         set "Lambda_c+ -> p+ K_S0 pi+ pi-"
  unrefinedListName set "MyLcTopKspipi"
  fittingAlgorithm  set "TreeFitter"
  fitConstraints    set "Mass"
  preFitSelectors    set "Mass 2.220:2.350"
  postFitSelectors   set "Mass 2.220:2.350"
  postFitSelectors   set "ProbChiSq 0.00001:"
  #fitSettings        set "UpdateDaughters"
  createUsrData     set true
}


#####################################################################
#####################################################################
createsmpmaker BetaMiniPhysicsSequence MyLcToLzpipipi {
  decayMode         set "Lambda_c+ -> Lambda0 pi- pi+ pi+"
  daughterListNames set "MyConstL0"
  daughterListNames set "ChargedTracks"
  daughterListNames set "ChargedTracks"
  daughterListNames set "ChargedTracks"
  fittingAlgorithm  set "Cascade"
  fitConstraints    set "Geo"
  preFitSelectors    set "Mass 2.220:2.350"
  postFitSelectors   set "Mass 2.220:2.350"
  postFitSelectors   set "ProbChiSq 0.00001:"
  createUsrData     set true
}

#####################
#createsmprefiner BetaMiniPhysicsSequence MyConstLcToLzpipipi {
createsmprefitter BetaMiniPhysicsSequence MyConstLcToLzpipipi {
  decayMode         set "Lambda_c+ -> Lambda0 pi- pi+ pi+"
  unrefinedListName set "MyLcToLzpipipi"
  fittingAlgorithm  set "TreeFitter"
  fitConstraints    set "Mass"
  preFitSelectors    set "Mass 2.220:2.350"
  postFitSelectors   set "Mass 2.220:2.350"
  postFitSelectors   set "ProbChiSq 0.00001:"
  #fitSettings        set "UpdateDaughters"
  createUsrData     set true
}

#####################################################################
#####################################################################

createsmpmerger BetaMiniPhysicsSequence AllLambdaC {
  inputListNames    set "MyLcTopKpi"
  inputListNames    set "MyLcTopKs"
  inputListNames    set "MyLcTopKspipi"
  inputListNames    set "MyLcToLzpipipi"
  disableCloneCheck set true
}

#####################################################################

createsmpmerger BetaMiniPhysicsSequence AllConstLambdaC {
  inputListNames    set "MyConstLcTopKpi"
  inputListNames    set "MyConstLcTopKs"
  inputListNames    set "MyConstLcTopKspipi"
  inputListNames    set "MyConstLcToLzpipipi"
  disableCloneCheck set true
}

#####################################################################

#####################################################################
#####################################################################
# NEW STUFF
#####################################################################
#####################################################################
#### Do SimpleComposition


createsmpmaker BetaMiniPhysicsSequence myB_unc {
  debug              set f
  verbose            set f
  #decayMode          set "B0 -> Lambda0 Lambda0"
  decayMode         set "B+ -> Lambda_c+ Lambda0"
  #daughterListNames  set "MyConstLcTopKpi"
  daughterListNames  set "AllConstLambdaC"
  daughterListNames  set "AllConstLambda0"
  fittingAlgorithm   set "TreeFitter"
  fitConstraints     set "Geo"
  preFitSelectors    set "Mass    5.0:5.5"
  preFitSelectors    set "DeltaE -1.0:1.0"
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
  decayMode         set "B+ -> Lambda_c+ Lambda0"
  #decayMode          set "B0 -> Lambda0 Lambda0"
  unrefinedListName  set "myB_unc"
  fittingAlgorithm   set "TreeFitter"
  fitConstraints     set "Geo"
  #fitSettings        set "InvalidateFit"
  fitSettings        set "UpdateDaughters"
  preFitSelectors    set "Mass    5.0:5.5"
  preFitSelectors    set "DeltaE -1.0:1.0"
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

    ###########################################################################
    # BLOCK ORDER MATTERS.
    # BtuTupleMaker fills blocks in the order they are declared here. While
    # filling a block, any daughter not already in its type's list is APPENDED
    # to that list and given the next index. If the daughter's block has
    # already been written, the appended entry never reaches the ntuple and
    # Xd{i}Idx points past the end of the block (e.g. K_Sd1Idx >= npi).
    #
    # So every parent must be declared ABOVE all of its daughters:
    #
    #   B -> LambdaC -> Lambda0 -> K_S -> pi0      (composites, top down)
    #     -> p, K, pi, e, mu, gamma                (final-state particles)
    #     -> TRK                                   (automatic, filled last)
    #
    #   B+        -> Lambda_c+ Lambda0
    #   Lambda_c+ -> p K pi | p K_S | p K_S pi pi | Lambda0 pi pi pi
    #   Lambda0   -> p pi
    #   K_S0      -> pi pi
    #   pi0       -> gamma gamma
    #
    # The max-candidate numbers are also limits: once a block is full, further
    # entries are dropped, and their indices point past the end the same way.
    # The pi, p and Lambda0 blocks are enlarged below for that reason.
    ###########################################################################

    #-------------------- B (top of tree) -------------------------------------
    ntpBlockConfigs    set "B+         B             2   100"
    ntpBlockContents   set "B       : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(myB_unc) ShapeVars"
    ntpAuxListContents set "B       : myB_con: _con_ : Mass Momentum CMMomentum Vertex VtxChi2 UsrData(myB_con)"

    #-------------------- Lambda_c+ (daughters: p K pi K_S Lambda0) ------------
    #..maxDaughters 4 to cover the Lzpipipi / pKspipi modes
    ntpBlockConfigs    set "Lambda_c+  LambdaC  4   100"
    ntpBlockContents   set "LambdaC : MCIdx Mass Momentum CMMomentum Vertex VtxChi2 Flight FlightBS nDaughters"
    ntpAuxListContents set "LambdaC : AllLambdaC : _unc_ : Mass Momentum CMMomentum Vertex VtxChi2 nDaughters"
    #ntpAuxListContents set "LambdaC : AllConstLambdaC : _unc_ : Mass Momentum CMMomentum Vertex VtxChi2 nDaughters"

    #-------------------- Lambda0 (below B and LambdaC; daughters p pi) --------
    ntpBlockConfigs    set "Lambda0    Lambda0       2   50"
    ntpBlockContents   set "Lambda0   : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(MyConstL0) Flight FlightBS"
    ntpAuxListContents set "Lambda0 : AllLambda0       : _unc_ : Mass Momentum CMMomentum Vertex VtxChi2"

    #-------------------- K_S (below LambdaC; daughters pi pi) -----------------
    ntpBlockConfigs    set "K_S0        K_S  2       50"
    ntpBlockContents   set "K_S   :  Mass CMMomentum Momentum MCIdx Vertex VtxChi2 UsrData(MyConstKs) Flight FlightBS"

    #-------------------- pi0 (daughters gamma gamma) --------------------------
    ntpBlockConfigs    set "pi0   pi0    2 256"
    ntpBlockContents   set "pi0  : Mass VtxChi2 MCIdx CMMomentum"
    ntpAuxListContents set "pi0 : pi0LooseMass : _unc_ : Mass Momentum CMMomentum"

    #-------------------- final-state particles (no daughters) -----------------
    ntpBlockConfigs    set "p+         p             0   50"
    ntpBlockContents   set "p         : Momentum CMMomentum MCIdx"

    ntpBlockConfigs    set "K+     K       0   100"
    ntpBlockContents   set "K :  MCIdx Momentum CMMomentum"

    ntpBlockConfigs    set "pi-        pi            0   100"
    ntpBlockContents   set "pi        : Momentum CMMomentum MCIdx"

    ntpBlockConfigs    set "e-     e       0   100"
    ntpBlockContents   set "e :  MCIdx Momentum CMMomentum"

    ntpBlockConfigs    set "mu-    mu      0   100"
    ntpBlockContents   set "mu : MCIdx Momentum CMMomentum"

    ntpBlockConfigs    set "gamma      gamma         0   90"
    ntpBlockContents   set "gamma     : MCIdx Momentum CMMomentum"

    #-------------------- TRK (charged-track block, filled last) ---------------
    ntpBlockContents   set "TRK       : Momentum CMMomentum MCIdx"

    #..Pre-fill some blocks with whole lists
    fillAllCandsInList set "Lambda0 MyConstL0"
    fillAllCandsInList set "TRK ChargedTracks"

    #..Want to save all CalorNeutrals in the gamma block
    gamExtraContents   set EMC
    fillAllCandsInList set "gamma CalorNeutral"

    fillAllCandsInList set "pi0   pi0Loose"

    #..Link charged final-state blocks to TRK (gives {block}TrkIdx)
    ntpBlockToTrk set "pi K mu e p"

    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    trkExtraContents set HOTS:detailSVT

    ###########################################
    # This will give me two different daughter candidates
    # if that's what happens.
    # Trying to set this as true for TRK's only?
    #
    # Checking the documentation here
    # https://babar-wiki.heprc.uvic.ca/bbr_wiki/index.php/Physics_analysis/BtoDtaunu_SLtag/tupleCode/script
    ############################################
    #checkClones set false
    #checkCloneBlocks set "p pi Lambda0 TRK"
    checkClones set true
    #checkCloneBlocks set "p pi gamma TRK"

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
