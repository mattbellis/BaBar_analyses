#------------------------------------------------------------------------------
# $Id: MyMiniAnalysis.tcl,v 1.29 2004/11/19 22:42:08 fnc Exp $
# Sample MyMiniAnalysis.tcl file
#------------------------------------------------------------------------------
# always source the error logger early in your main tcl script
sourceFoundFile ErrLogger/ErrLog.tcl
sourceFoundFile FrameScripts/FwkCfgVar.tcl
sourceFoundFile FrameScripts/talkto.tcl
sourceFoundFile SimpleComposition/SmpProcs.tcl

# set the error logging level to 'warning'.  If you encounter a configuration 
# error you can get more information using 'trace'
ErrLoggingLevel warning

##
## Set the number of events to run. If this isn't set, all events in the
## input collections will be processed.
##
FwkCfgVar NEvent

## create Everything path and add core sequences to it. btaMiniPhysics is the 
## same as btaMini, just appending a few standard list generating modules. For 
## reading data with stored composites, you may have a conflict running 
## btaMiniPhyscs.tcl
##
## You can also run (most of) the PhysProdSequence, complete with its 3 gamma 
## conversion finders, etc. Consider disabling the portion of this sequence 
## that you do not need to save yourself some time.  The BetaLumiSequence
## and TagProd sequences are left off, as they otherwise cause problems.
##
#sourceFoundFile BetaMiniUser/btaMini.tcl
sourceFoundFile BetaMiniUser/btaMiniPhysics.tcl
#sourceFoundFile BetaMiniUser/btaMiniPhysProdSequence.tcl

# Append QA sequence if requested, disable module otherwise to avoid empty histos
FwkCfgVar MyMiniQA
if [info exists MyMiniQA] {
  sourceFoundFile BetaMiniQA/BetaMiniQaSequence.tcl
  path append Everything BetaMiniQaSequence
  talkto QaMiniBtaCandidates {
    startPrint set  0
    stopPrint  set  3
    printFreq  set  1
  }
  path append Everything TagInspector
  sourceFoundFile SkimMini/listOfTagBits.tcl
} else {
  module disable QaMiniBtaCandidates
}

mod talk PdtInit
    pdtTable set "PDT/pdt-data.table"
exit

## Add Analysis module
##
path append Everything MyMiniAnalysis

##
##  If your job has a tag-level filter, here is how you should run it
##  so as to avoid wasting time reading the mini when the tag filter fails
##  Here's a simple example that restricts to just multi-hadron events
##  on Kan input

module clone TagFilterByName TagBGFMultiHadron
module talk TagBGFMultiHadron
  andList set BGFMultiHadron
  assertIfMissing set true
exit
#sequence append BetaMiniReadSequence -a KanEventUpdateTag TagBGFMultiHadron

#
#  Turn off some specialty items
#
module disable MyDstarAnalysis
module disable MyK0Analysis
seq disable SmpCompositionSequence

talkto MyMiniAnalysis {
      eventInfoList set ChargedTracks
}

createsmpmerger BetaMiniPhysicsSequence AllLambdaC {

    inputListNames    set "LambdaCTopKpi"
    inputListNames    set "LambdaCTopKs"
    inputListNames    set "LambdaCTopKspipi"
    inputListNames    set "LambdaCToLzpi"
    inputListNames    set "LambdaCToLzpipipi"
    disableCloneCheck set true
}

createsmprefitter BetaMiniPhysicsSequence MyConstKs {

    decayMode         set "K_S0 -> pi+ pi-"
    unrefinedListName set "KsLoose_LambdaC"
    preFitSelectors   set "Mass"
    fittingAlgorithm  set "TreeFitter"
    fitConstraints    set "Mass"
    postFitSelectors  set "ProbChiSq"
    postFitSelectors  set "FlightSignificance"
    createUsrData     set true
}

createsmprefitter BetaMiniPhysicsSequence MyConstLambda {

    decayMode         set "Lambda0 -> p+ pi-"
    unrefinedListName set "Lambda_LambdaC"
    preFitSelectors   set "Mass"
    fittingAlgorithm  set "TreeFitter"
    fitConstraints    set "Mass"
    postFitSelectors  set "ProbChiSq"
    postFitSelectors  set "FlightSignificance"
#    postFitSelectors  set "Helicity" # Causes random seg faults
    createUsrData     set true

}

createsmprefitter BetaMiniPhysicsSequence MyConstLcTopKpi {

    decayMode         set "Lambda_c+ -> p+ K- pi+"
    unrefinedListName set "LambdaCTopKpi"
    fittingAlgorithm  set "TreeFitter"
    fitConstraints    set "Mass"

}

createsmprefiner BetaMiniPhysicsSequence MyConstLcTopConstKs {

    decayMode         set "Lambda_c+ -> p+ K_S0"
    unrefinedListName set "LambdaCTopKs"
    daughterListNames set "pLHVeryLoose"
    daughterListNames set "MyConstKs"
    fittingAlgorithm  set "TreeFitter"
    fitConstraints    set "Mass"

}

createsmprefiner BetaMiniPhysicsSequence MyConstLcTopConstKspipi {

    decayMode         set "Lambda_c+ -> p+ K_S0 pi+ pi-"
    unrefinedListName set "LambdaCTopKspipi"
    daughterListNames set "pLHVeryLoose"
    daughterListNames set "MyConstKs"
    daughterListNames set "ChargedTracks"
    daughterListNames set "ChargedTracks"
    fittingAlgorithm  set "TreeFitter"
    fitConstraints    set "Mass"

}

createsmprefiner BetaMiniPhysicsSequence MyConstLcToConstLzpi {

    decayMode         set "Lambda_c+ -> Lambda0 pi+"
    unrefinedListName set "LambdaCToLzpi"
    daughterListNames set "MyConstLambda"
    daughterListNames set "ChargedTracks"
    fittingAlgorithm  set "TreeFitter"
    fitConstraints    set "Mass"

}

createsmprefiner BetaMiniPhysicsSequence MyConstLcToConstLzpipipi {

    decayMode         set "Lambda_c+ -> Lambda0 pi+ pi+ pi-"
    unrefinedListName set "LambdaCToLzpipipi"
    daughterListNames set "MyConstLambda"
    daughterListNames set "ChargedTracks"
    daughterListNames set "ChargedTracks"
    daughterListNames set "ChargedTracks"
    fittingAlgorithm  set "TreeFitter"
    fitConstraints    set "Mass"

}

createsmpmerger BetaMiniPhysicsSequence AllConstLambdaC {

    inputListNames    set "MyConstLcTopKpi"
    inputListNames    set "MyConstLcTopConstKs"
    inputListNames    set "MyConstLcTopConstKspipi"
    inputListNames    set "MyConstLcToConstLzpi"
    inputListNames    set "MyConstLcToConstLzpipipi"
    disableCloneCheck set true

}


createsmpmaker BetaMiniPhysicsSequence MyBzConstLc {

    decayMode         set "anti-B0 -> Lambda_c+ anti-p-"
    daughterListNames set "AllConstLambdaC"
    daughterListNames set "pLHVeryLoose"
    preFitSelectors   set "Mass"
    preFitSelectors   set "Mmiss"
    preFitSelectors   set "Mes"
    preFitSelectors   set "DeltaE"
    fittingAlgorithm  set "TreeFitter"
    postFitSelectors  set "Mass 5.0:6.0"
    postFitSelectors  set "Mmiss"
    postFitSelectors  set "Mes"
    postFitSelectors  set "DeltaE"
    postFitSelectors  set "ProbChiSq 0.000001:"
    createUsrData     set true
}

createsmpmaker BetaMiniPhysicsSequence MyBmConstLc {

    decayMode         set "B- -> Lambda_c+ anti-p- pi-"
    daughterListNames set "AllConstLambdaC"
    daughterListNames set "pLHVeryLoose"
    daughterListNames set "ChargedTracks"
    preFitSelectors   set "Mass"
    preFitSelectors   set "Mmiss"
    preFitSelectors   set "Mes"
    preFitSelectors   set "DeltaE"
    fittingAlgorithm  set "TreeFitter"
    postFitSelectors  set "Mass 5.0:6.0"
    postFitSelectors  set "Mmiss"
    postFitSelectors  set "Mes"
    postFitSelectors  set "DeltaE"
    postFitSelectors  set "ProbChiSq 0.000001:"
    createUsrData     set true
}

createsmpmerger BetaMiniPhysicsSequence AllB {

    inputListNames    set "MyBzConstLc"
    inputListNames    set "MyBmConstLc"
    disableCloneCheck set true
    createUsrData     set true
}

createsmprefitter BetaMiniPhysicsSequence MyConstBmConstLc {

    decayMode         set "B- -> Lambda_c+ anti-p- pi-"
    unrefinedListName set "MyBmConstLc"
    preFitSelectors   set "Mass"
    fittingAlgorithm  set "TreeFitter"
    fitConstraints    set "Mass"
    fitSettings       set "InvalidateFit"
    fitSettings       set "UpdateDaughters"
    postFitSelectors  set "Mass"
    postFitSelectors  set "Mmiss"
    postFitSelectors  set "DeltaE"
    postFitSelectors  set "Mes"
    postFitSelectors  set "ProbChiSq"
    createUsrData     set true
}

createsmprefitter BetaMiniPhysicsSequence MyConstBzConstLc {

    decayMode         set "anti-B0 -> Lambda_c+ anti-p-"
    unrefinedListName set "MyBzConstLc"
    preFitSelectors   set "Mass"
    fittingAlgorithm  set "TreeFitter"
    fitConstraints    set "Mass"
    fitSettings       set "InvalidateFit"
    fitSettings       set "UpdateDaughters"
    postFitSelectors  set "Mass"
    postFitSelectors  set "Mmiss"
    postFitSelectors  set "DeltaE"
    postFitSelectors  set "Mes"
    postFitSelectors  set "ProbChiSq"
    createUsrData     set true
}

#pidCfg_mode weight *LH*

path append Everything BtuTupleMaker

talkto BtuTupleMaker {

#..Event information to dump
    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsInt set "nTracks"
    eventTagsFloat set "R2All thrustMagAll thrustCosThAll thrustPhiAll sphericityAll"
    writeEveryEvent set false

#..MC truth info
#    fillMC set true
    fillMC set false
    checkClones set true
    mcBlockContents set "Mass CMMomentum Momentum Vertex"

#..Particle blocks to store
    listToDump set AllB

    ntpBlockConfigs    set "B-        Bm      3     100"
    ntpBlockContents   set "Bm: MCIdx Mass Momentum CMMomentum Vertex VtxChi2 Dalitz DalitzMC Helicity2body Helicity3body CandThrust LgndrMoments UsrData(MyBmConstLc)"
    ntpAuxListContents set "Bm : MyConstBmConstLc  : _con_ : Mass Momentum Dalitz DalitzMC Helicity2body Helicity3body UsrData(MyConstBmConstLc)"

    ntpBlockConfigs    set "B0        Bz      2     100"
    ntpBlockContents   set "Bz: MCIdx Mass Momentum CMMomentum Vertex VtxChi2 Dalitz DalitzMC Helicity2body CandThrust LgndrMoments UsrData(MyBzConstLc)"
    ntpAuxListContents set "Bz : MyConstBzConstLc  : _con_ : Mass Momentum Helicity2body UsrData(MyConstBzConstLc)"

    ntpBlockConfigs    set "Lambda_c+ LambdaC 4     100"
    ntpBlockContents   set "LambdaC: MCIdx Mass Momentum CMMomentum Vertex VtxChi2 Dalitz DalitzMC nDaughters"
    ntpAuxListContents set "LambdaC: AllLambdaC  : _unc_ : Mass  Momentum CMMomentum Vertex VtxChi2 Dalitz DalitzMC nDaughters"

    ntpBlockConfigs    set "Lambda0   Lambda  2     100"
    ntpBlockContents   set "Lambda: MCIdx Mass Momentum CMMomentum Vertex VtxChi2 Flight FlightBS UsrData(MyConstLambda)"
    ntpAuxListContents set "Lambda: Lambda_LambdaC : _unc_ : Mass Momentum CMMomentum Vertex VtxChi2 Flight FlightBS"

    ntpBlockConfigs    set "K_S0      Ks      2     100"
    ntpBlockContents   set "Ks: MCIdx Mass Momentum CMMomentum Vertex VtxChi2 Flight FlightBS UsrData(MyConstKs)"
    ntpAuxListContents set "Ks: KsLoose_LambdaC : _unc_ : Mass Momentum CMMomentum Vertex VtxChi2 Flight FlightBS"

    ntpBlockConfigs    set "anti-p-   p       0     100"
    ntpBlockContents   set "p: MCIdx Momentum CMMomentum PIDWeight(pLHVeryLoose,pLHLoose,pLHTight,pLHVeryTight)"

    ntpBlockConfigs    set "K+        K       0     100"
    ntpBlockContents   set "K: MCIdx Momentum CMMomentum PIDWeight(KLHVeryLoose,KLHLoose,KLHTight,KLHVeryTight)"

    ntpBlockConfigs    set "pi-       pi      0     100"
#    trkExtraContents   set "HOTS:"
    trkExtraContents   set "Dirc:pi,K,p"


}

module talk EvtCounter
  printFreq set 1000
#  printFreq set 1
exit

#path list
if [info exists NEvent] {
  ev begin -nev $NEvent
} else {
  ev begin
}

ErrMsg trace "completed OK"
exit
