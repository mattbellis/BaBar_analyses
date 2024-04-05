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
# NEW STUFF
#####################################################################
createsmpmerger BetaMiniPhysicsSequence AllLambdaC {
  inputListNames    set "LambdaCTopKpi"
  #inputListNames    set "LambdaCTopKs"
  #inputListNames    set "LambdaCTopKspipi"
  #inputListNames    set "LambdaCToLzpi"
  #inputListNames    set "LambdaCToLzpipipi"
  disableCloneCheck set true
}
#####################################################################
#####################################################################
# Refit the LambdaC to constrain the mass
createsmprefitter BetaMiniPhysicsSequence MyConstLcTopKpi {
  decayMode         set "Lambda_c+ -> p+ K- pi+"
  unrefinedListName set "LambdaCTopKpi"
  fittingAlgorithm  set "TreeFitter"
  fitConstraints    set "Mass"
}
#####################################################################
createsmpmerger BetaMiniPhysicsSequence AllConstLambdaC {
  inputListNames    set "MyConstLcTopKpi"
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
#seq create SmpMyB_uncL_mu
#seq create SmpMyB_conL_mu
#seq create SmpMyB_uncL_e
#seq create SmpMyB_conL_e

# muon
#mod clone SmpMakerDefiner myB_uncL_mu
#seq append SmpMyB_uncL_mu myB_uncL_mu
#catch { setProduction myB_uncL_mu }

#mod clone SmpMakerDefiner myB_conL_mu
#seq append SmpMyB_conL_mu myB_conL_mu
#catch { setProduction myB_conL_mu }

# electron
#mod clone SmpMakerDefiner myB_uncL_e
#seq append SmpMyB_uncL_e myB_uncL_e
#catch { setProduction myB_uncL_e }

set leptons {
    {"mu" "mu-" "muCombinedVeryLooseFakeRate"}
    {"e" "e-" "eCombinedSuperLoose"}}

foreach lep $leptons {

  set l0 [lindex $lep 0]
  set l1 [lindex $lep 1]
  set l2 [lindex $lep 2]

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
      #fitConstraints     set "Mass"
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
      createUsrData      set t
  }
  #################################################################
}

#####################################################################
# Set up the Smp stuff
#################################################################
# muon
#################################################################
# Unconstrained
#talkto myB_uncL_mu {
    #debug              set f
    #verbose            set f
    #decayMode          set "B0 -> Lambda_c+ mu-"
    #daughterListNames  set "AllConstLambdaC"
    #daughterListNames  set "muCombinedVeryLooseFakeRate"
    #fittingAlgorithm   set "TreeFitter"
    #fitConstraints     set "Geo"
    #preFitSelectors    set "Mass    5.0:5.5"
    #preFitSelectors    set "DeltaE -0.5:0.5"
    #preFitSelectors    set "Mes"
    #preFitSelectors    set "Mmiss"
    #postFitSelectors   set "Mass"
    #postFitSelectors   set "DeltaE"
    #postFitSelectors   set "Mes"
    #postFitSelectors   set "Mmiss"
    #postFitSelectors   set "ProbChiSq"
    #createUsrData      set t
#}
# Constrained
#createsmprefitter BetaMiniPhysicsSequence myB_conL_mu {
    #debug              set f
    #verbose            set f
    #decayMode          set "B0 -> Lambda_c+ mu-"
    #unrefinedListName  set "myB_uncL_mu"
    #fittingAlgorithm   set "TreeFitter"
    #fitConstraints     set "Geo"
    ##fitConstraints     set "Mass"
    ##fitSettings        set "InvalidateFit"
    #fitSettings        set "UpdateDaughters"
    #preFitSelectors    set "Mass    5.0:5.5"
    #preFitSelectors    set "DeltaE -0.5:0.5"
    #preFitSelectors    set "Mes"
    #preFitSelectors    set "Mmiss"
    #postFitSelectors   set "Mass"
    #postFitSelectors   set "DeltaE"
    #postFitSelectors   set "Mes"
    #postFitSelectors   set "Mmiss"
    #postFitSelectors   set "ProbChiSq"
    #createUsrData      set t
#}
#################################################################
#################################################################

#################################################################
# electron
#################################################################
# Unconstrained
#talkto myB_uncL_e {
    #debug              set f
    #verbose            set f
    #decayMode          set "B0 -> Lambda_c+ e-"
    #daughterListNames  set "AllConstLambdaC"
    #daughterListNames  set "eCombinedSuperLoose"
    #fittingAlgorithm   set "TreeFitter"
    #fitConstraints     set "Geo"
    #preFitSelectors    set "Mass    5.0:5.5"
    #preFitSelectors    set "DeltaE -0.5:0.5"
    #preFitSelectors    set "Mes"
    #preFitSelectors    set "Mmiss"
    #postFitSelectors   set "Mass"
    #postFitSelectors   set "DeltaE"
    #postFitSelectors   set "Mes"
    #postFitSelectors   set "Mmiss"
    #postFitSelectors   set "ProbChiSq"
    #createUsrData      set t
#}
# Constrained
#createsmprefitter BetaMiniPhysicsSequence myB_conL_e {
    #debug              set f
    #verbose            set f
    #decayMode          set "B0 -> Lambda_c+ e-"
    #unrefinedListName  set "myB_uncL_e"
    #fittingAlgorithm   set "TreeFitter"
    #fitConstraints     set "Geo"
    ##fitConstraints     set "Mass"
    ##fitSettings        set "InvalidateFit"
    #fitSettings        set "UpdateDaughters"
    #preFitSelectors    set "Mass    5.0:5.5"
    #preFitSelectors    set "DeltaE -0.5:0.5"
    #preFitSelectors    set "Mes"
    #preFitSelectors    set "Mmiss"
    #postFitSelectors   set "Mass"
    #postFitSelectors   set "DeltaE"
    #postFitSelectors   set "Mes"
    #postFitSelectors   set "Mmiss"
    #postFitSelectors   set "ProbChiSq"
    #createUsrData      set t
#}
# electron
#talkto myB_uncL_e {
    #debug              set f
    #verbose            set f
    #decayMode          set "B0 -> Lambda_c+ e-"
    #daughterListNames  set "AllConstLambdaC"
    #daughterListNames  set "eCombinedSuperLoose"

    #fittingAlgorithm   set "TreeFitter"
    #fitConstraints     set "Geo"
    #fitSettings        set "InvalidateFit"
    #preFitSelectors    set "Mass 5.0:5.5"
#
    #createUsrData  set t
#}


################# NEW #####################################
createsmpmerger BetaMiniPhysicsSequence AllB_mu {
  inputListNames    set "myB_uncL_mu"
  inputListNames    set "myB_conL_mu"
  disableCloneCheck set true
  createUsrData     set true
}

createsmpmerger BetaMiniPhysicsSequence AllB_e {
  inputListNames    set "myB_uncL_e"
  inputListNames    set "myB_conL_e"
  disableCloneCheck set true
  createUsrData     set true
}



#####################################################################
## Add Analysis module
##
#path append Everything SmpMyB_uncL_mu
#path append Everything SmpMyB_conL_mu
#path append Everything SmpMyB_uncL_e
#path append Everything SmpMyB_conL_e

#mod  clone  BtuTupleMaker BtuTupleMaker_mu
#mod  clone  BtuTupleMaker BtuTupleMaker_e

path append Everything    BtuTupleMaker_e
path append Everything    BtuTupleMaker_mu
#####################################################################
#####################################################################
talkto BtuTupleMaker_mu {
  
    ntupleName set ntp1_LambdaCmu
    listToDump set AllB_mu

    fillMC set true

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsInt       set "nTracks nGoodTrkLoose"
    eventTagsFloat     set "R2All"

    mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    ntpBlockConfigs set "B0         B             2   100"
    ntpBlockConfigs set "Lambda_c+  LambdaC       3   20"
    ntpBlockConfigs set "mu-        mu            0   30"
    ntpBlockConfigs set "p+         p             0   20"
    ntpBlockConfigs set "pi+        pi            0   30"
    ntpBlockConfigs set "K+         K             0   30"

    ntpBlockContents set "B         : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(myB_uncL_mu) ShapeVars"
    ntpBlockContents set "LambdaC   : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 Flight FlightBS"
    ntpBlockContents set "pi        : Momentum CMMomentum MCIdx"
    ntpBlockContents set "p         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "K         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "mu        : Momentum CMMomentum MCIdx"
    ntpBlockContents set "TRK       : MCIdx"

    ntpAuxListContents set "B       : myB_conL_mu : _con_ : Mass Momentum CMMomentum UsrData(myB_conL_mu)"
    ntpAuxListContents set "LambdaC : AllLambdaC  : _unc_   : Mass Momentum CMMomentum Vertex VtxChi2"

    ntpBlockToTrk   set "p mu pi K "

    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    trkExtraContents set HOTS:detailSVT

    show
}

#####################################################################
talkto BtuTupleMaker_e {
  
    ntupleName set ntp2_LambdaCe
    listToDump set AllB_e

    fillMC set true

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsInt       set "nTracks nGoodTrkLoose"
    eventTagsFloat     set "R2All"

    mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    #ntpBlockConfigs    set "Lambda_c+ LambdaC 4     100"
    #ntpBlockContents   set "LambdaC: MCIdx Mass Momentum CMMomentum Vertex VtxChi2 Dalitz DalitzMC nDaughters"
    #ntpAuxListContents set "LambdaC: AllLambdaC  : _unc_ : Mass  Momentum CMMomentum Vertex VtxChi2 Dalitz DalitzMC nDaughters"

    ntpBlockConfigs set "B0         B             2   100"
    ntpBlockConfigs set "Lambda_c+  LambdaC       3   20"
    ntpBlockConfigs set "e-         e             0   30"
    ntpBlockConfigs set "p+         p             0   20"
    ntpBlockConfigs set "pi+        pi            0   30"
    ntpBlockConfigs set "K+         K             0   30"

    ntpBlockContents set "B         : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(myB_uncL_e) ShapeVars"
    ntpBlockContents set "LambdaC   : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 Flight FlightBS"
    ntpBlockContents set "pi        : Momentum CMMomentum MCIdx"
    ntpBlockContents set "p         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "K         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "e         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "TRK       : MCIdx"

    ntpAuxListContents set "B       : myB_conL_e  : _con_ : Mass Momentum CMMomentum UsrData(myB_conL_e)"
    ntpAuxListContents set "LambdaC : AllLambdaC  : _unc_   : Mass Momentum CMMomentum Vertex VtxChi2"

    ntpBlockToTrk   set "p e pi K "

    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    trkExtraContents set HOTS:detailSVT

    show
}

#########################
#########################
#################################################################
#################################################################
#talkto BtuTupleMaker_e {
  
    #ntupleName set ntp1_LambdaCe
    #listToDump set myB_e

    #fillMC set true
#
    #eventBlockContents set "EventID CMp4 BeamSpot"
    #eventTagsInt       set "nTracks nGoodTrkLoose"
    #eventTagsFloat     set "R2All"
#
    #mcBlockContents    set "Mass CMMomentum Momentum Vertex"
#
    #ntpBlockConfigs set "B0         B             2   100"
    #ntpBlockConfigs set "Lambda_c+  LambdaC       3   20"
    #ntpBlockConfigs set "e-         e             0   30"
    #ntpBlockConfigs set "p+         p             0   20"
    #ntpBlockConfigs set "pi+        pi            0   30"
    #ntpBlockConfigs set "K+         K             0   30"
#
    #ntpBlockContents set "B         : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(myB_e) ShapeVars"
    #ntpBlockContents set "LambdaC   : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 Flight FlightBS"
    #ntpBlockContents set "pi        : Momentum CMMomentum MCIdx"
    #ntpBlockContents set "K         : Momentum CMMomentum MCIdx"
    #ntpBlockContents set "p         : Momentum CMMomentum MCIdx"
    #ntpBlockContents set "e         : Momentum CMMomentum MCIdx"
    #ntpBlockContents set "TRK       : MCIdx"
#
    #ntpBlockToTrk   set "p e  pi K "
#
    #trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    #trkExtraContents set HOTS:detailSVT
#
    #show
#}
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
