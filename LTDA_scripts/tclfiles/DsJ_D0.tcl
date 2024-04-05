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
FwkCfgVar ConfigPatch "Run2"

##
## Set the number of events to run. If this isn't set, all events in the
## input collections will be processed.
##
FwkCfgVar NEvent

## choose the flavor of ntuple to write (hbook or root) and the file name
##
FwkCfgVar BetaMiniTuple "root"
#FwkCfgVar histFileName "MyMiniAnalysis.root"

##
sourceFoundFile BetaMiniUser/btaMiniPhysics.tcl


#sourceFoundFile UsrTools/UsrDataProcs.tcl
#enableReadUsrData
#readEventUsrData myEventData
#readCandUsrData xxx


mod clone SmpSubListerDefiner GammaForDs
catch { setProduction GammaForDs }
talkto GammaForDs {
        unrefinedListName  set GoodPhotonLoose
        selectors   set "LabE 0.1:10.0"
        selectors   set "Lat 0.0:0.8"
        maxNumberOfCandidates  set 50000
}

talkto pi0AllDefault {
         createUsrData      set  true
        maxNumberOfCandidates  set 50000
}
mod clone SmpRefinerDefiner Ks_Pid
catch { setProduction Ks_Pid }
#Refine the default Ks list
talkto Ks_Pid {
        decayMode         set "K_S0 -> pi+ pi-"
        unrefinedListName set  KsDefault
        createUsrData     set  true
        fittingAlgorithm  set "TreeFitter"
        preFitSelectors   set "Mass 0.46:0.53"
        postFitSelectors  set "ProbChiSq 0.:"
        postFitSelectors  set "FlightSignificance 0.:"
        fitConstraints    set "Mass"
        fitSettings       set "UpdateDaughters"
        maxNumberOfCandidates  set 50000
}

# the D0 lists
mod clone SmpMakerDefiner myD0ToKPi
mod clone SmpMakerDefiner myD0ToK3Pi
mod clone SmpMakerDefiner myD0ToKsPiPi
mod clone SmpMakerDefiner myD0ToKPiPi0
mod clone SmpMakerDefiner myD0ToKsPiPiPi0
mod clone SmpMakerDefiner myD0ToK3PiPi0

catch { setProduction  myD0ToKPi}
catch { setProduction  myD0ToK3Pi}
catch { setProduction  myD0ToKsPiPi}
catch { setProduction  myD0ToKPiPi0}
catch { setProduction  myD0ToKsPiPiPi0}
catch { setProduction  myD0ToK3PiPi0}

talkto myD0ToKPi {
       decayMode          set "D0 -> K- pi+"
       daughterListNames  set "KCombinedVeryLoose"
       daughterListNames  set "piCombinedVeryLoose"
       fittingAlgorithm   set "TreeFitter"
       preFitSelectors    set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "ProbChiSq 0.001:"
       fitSettings        set "UpdateDaughters"
       maxNumberOfCandidates  set 50000
}

talkto myD0ToKPiPi0 {
       decayMode          set "D0 -> K- pi+ pi0"
       daughterListNames  set "KCombinedVeryLoose"
       daughterListNames  set "piCombinedVeryLoose"
       daughterListNames  set "pi0AllDefault"
       fittingAlgorithm   set "TreeFitter"
       preFitSelectors    set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "ProbChiSq 0.001:"
       fitSettings        set "UpdateDaughters"
       maxNumberOfCandidates  set 50000
}


talkto myD0ToKsPiPi {
       decayMode          set "D0 -> K_S0 pi+ pi-"
       daughterListNames  set "Ks_Pid"
       daughterListNames  set "piCombinedVeryLoose"
       daughterListNames  set "piCombinedVeryLoose"
       fittingAlgorithm   set "TreeFitter"
       preFitSelectors    set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "ProbChiSq 0.001:"
       fitSettings        set "UpdateDaughters"
        maxNumberOfCandidates  set 50000
}

talkto myD0ToKsPiPiPi0 {
       decayMode          set "D0 -> K_S0 pi+ pi- pi0"
       daughterListNames  set "Ks_Pid"
       daughterListNames  set "piCombinedVeryLoose"
       daughterListNames  set "piCombinedVeryLoose"
       daughterListNames  set "pi0AllDefault"
       fittingAlgorithm   set "TreeFitter"
       preFitSelectors    set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "ProbChiSq 0.001:"
       fitSettings        set "UpdateDaughters"
        maxNumberOfCandidates  set 50000
}

talkto myD0ToK3Pi {
       decayMode          set "D0 -> K- pi+ pi+ pi-"
       daughterListNames  set "KCombinedVeryLoose"
       daughterListNames  set "piCombinedVeryLoose"
       daughterListNames  set "piCombinedVeryLoose"
       daughterListNames  set "piCombinedVeryLoose"
       fittingAlgorithm   set "TreeFitter"
       preFitSelectors    set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "ProbChiSq 0.001:"
       fitSettings        set "UpdateDaughters"
        maxNumberOfCandidates  set 50000
}

talkto myD0ToK3PiPi0 {
       decayMode          set "D0 -> K- pi+ pi+ pi- pi0"
       daughterListNames  set "KCombinedVeryLoose"
       daughterListNames  set "piCombinedVeryLoose"
       daughterListNames  set "piCombinedVeryLoose"
       daughterListNames  set "piCombinedVeryLoose"
       daughterListNames  set "pi0AllDefault"
       fittingAlgorithm   set "TreeFitter"
       preFitSelectors    set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "ProbChiSq 0.001:"
       fitSettings        set "UpdateDaughters"
        maxNumberOfCandidates  set 50000
}

# the D+ lists
mod clone SmpMakerDefiner myDcToKPiPi
mod clone SmpMakerDefiner myDcToKsPi
mod clone SmpMakerDefiner myDcToKsPiPi0
mod clone SmpMakerDefiner myDcToKPiPiPi0

catch { setProduction  myDcToKPiPi }
catch { setProduction  myDcToKsPi }
catch { setProduction  myDcToKsPiPi0 }
catch { setProduction  myDcToKPiPiPi0 }

talkto myDcToKPiPi {
       decayMode          set "D+ -> K- pi+ pi+"
       daughterListNames  set "KCombinedVeryLoose"
       daughterListNames  set "piCombinedVeryLoose"
       daughterListNames  set "piCombinedVeryLoose"
       fittingAlgorithm   set "TreeFitter"
       preFitSelectors    set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "ProbChiSq 0.001:"
       fitSettings        set "UpdateDaughters"
        maxNumberOfCandidates  set 50000
}

talkto myDcToKPiPiPi0 {
       decayMode          set "D+ -> K- pi+ pi+ pi0"
       daughterListNames  set "KCombinedVeryLoose"
       daughterListNames  set "piCombinedVeryLoose"
       daughterListNames  set "piCombinedVeryLoose"
       daughterListNames  set "pi0AllDefault"
       fittingAlgorithm   set "TreeFitter"
       preFitSelectors    set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "ProbChiSq 0.001:"
       fitSettings        set "UpdateDaughters"
}

talkto myDcToKsPi {
       decayMode          set "D+ -> K_S0 pi+"
       daughterListNames  set "Ks_Pid"
       daughterListNames  set "piCombinedVeryLoose"
       fittingAlgorithm   set "TreeFitter"
       preFitSelectors    set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "ProbChiSq 0.001:"
       fitSettings        set "UpdateDaughters"
        maxNumberOfCandidates  set 50000
}

talkto myDcToKsPiPi0 {
       decayMode          set "D+ -> K_S0 pi+ pi0"
       daughterListNames  set "Ks_Pid"
       daughterListNames  set "piCombinedVeryLoose"
       daughterListNames  set "pi0AllDefault"
       fittingAlgorithm   set "TreeFitter"
       preFitSelectors    set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "ProbChiSq 0.001:"
       fitSettings        set "UpdateDaughters"
        maxNumberOfCandidates  set 50000
}


##merged lists 
mod clone SmpMergerDefiner myD0
catch { setProduction myD0 }

mod clone SmpMergerDefiner myDc
catch { setProduction myDc }

talkto myD0 {
   inputListNames    set  myD0ToKPi
   inputListNames    set  myD0ToK3Pi
   inputListNames    set  myD0ToKsPiPi
   inputListNames    set  myD0ToKPiPi0
   inputListNames    set  myD0ToKsPiPiPi0
   inputListNames    set  myD0ToK3PiPi0
   disableCloneCheck set true
   maxNumberOfCandidates  set 50000
}

talkto myDc {
   inputListNames    set  myDcToKPiPi
   inputListNames    set  myDcToKsPi
   inputListNames    set  myDcToKsPiPi0
   inputListNames    set  myDcToKPiPiPi0
   disableCloneCheck set true
   maxNumberOfCandidates  set 50000
}



# the D_s+ lists
mod clone SmpMakerDefiner myDsToKKPi
mod clone SmpMakerDefiner myDsToKKPiPi0

catch { setProduction  myDsToKKPi }
catch { setProduction  myDsToKKPiPi0 }

talkto myDsToKKPi {
       decayMode          set "D_s+ -> K- K+ pi+"
       daughterListNames  set "KCombinedVeryLoose"
       daughterListNames  set "KCombinedVeryLoose"
       daughterListNames  set "piCombinedVeryLoose"
       fittingAlgorithm   set "TreeFitter"
       preFitSelectors    set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "ProbChiSq 0.001:"
       fitSettings        set "UpdateDaughters"
        maxNumberOfCandidates  set 50000
}


talkto myDsToKKPiPi0 {
       decayMode          set "D_s+ -> K- K+ pi+ pi0"
       daughterListNames  set "KCombinedVeryLoose"
       daughterListNames  set "KCombinedVeryLoose"
       daughterListNames  set "piCombinedVeryLoose"
       daughterListNames  set "pi0AllDefault"
       fittingAlgorithm   set "TreeFitter"
       preFitSelectors    set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "ProbChiSq 0.001:"
       fitSettings        set "UpdateDaughters"
        maxNumberOfCandidates  set 50000
}


mod clone SmpMergerDefiner myDs
catch { setProduction myDs }

talkto myDs {
   inputListNames    set  myDsToKKPi
   inputListNames    set  myDsToKKPiPi0
   disableCloneCheck set true
   maxNumberOfCandidates  set 50000
}




# the D_s*+ lists
mod clone SmpMakerDefiner myDsstar
catch { setProduction  myDsstar }


talkto myDsstar {
       decayMode          set "D_s*+ -> D_s+ gamma"
       daughterListNames  set "myDs"
       daughterListNames  set "GammaForDs"
       fitConstraints     set "Beam"
       preFitSelectors    set "DeltaM 0.10:0.20"
       postFitSelectors   set "DeltaM 0.10:0.19"
       fittingAlgorithm   set "TreeFitter"
       postFitSelectors   set "ProbChiSq 0.001:"
       fitSettings        set "InvalidateFit"
       fitSettings        set "UpdateDaughters"
       fitSettings        set "FitAll"
        maxNumberOfCandidates  set 50000
}



# the D_sJ*+ lists
mod clone SmpMakerDefiner myDsJToDsPi0
mod clone SmpMakerDefiner myDsJToDsgamma
mod clone SmpMakerDefiner myDsJToDsstarPi0
mod clone SmpMakerDefiner myDsJToDsPiPi

catch { setProduction   myDsJToDsPi0 }
catch { setProduction   myDsJToDsgamma }
catch { setProduction   myDsJToDsstarPi0 }
catch { setProduction   myDsJToDsPiPi }


talkto myDsJToDsPi0 {
       decayMode          set "D_s1+ -> D_s+ pi0"
       daughterListNames  set "myDs"
       daughterListNames  set "pi0AllDefault"
       fittingAlgorithm   set "TreeFitter"
       fitConstraints     set "Beam"
       preFitSelectors    set "Mass 2.0:2.8"
       postFitSelectors   set "Mass 2.1:2.7"
       postFitSelectors   set "ProbChiSq 0.001:"
       fitSettings        set "InvalidateFit"
       fitSettings        set "FitAll"
       fitSettings        set "UpdateDaughters"
        maxNumberOfCandidates  set 50000
}


talkto myDsJToDsgamma {
       decayMode          set "D_s1+ -> D_s+ gamma"
       daughterListNames  set "myDs"
       daughterListNames  set "GoodPhotonLoose"
       fittingAlgorithm   set "TreeFitter"
       fitConstraints     set "Beam"
       preFitSelectors    set "Mass 2.0:2.8"
       postFitSelectors   set "Mass 2.1:2.7"
       postFitSelectors   set "ProbChiSq 0.001:"
       fitSettings        set "InvalidateFit"
       fitSettings        set "FitAll"
       fitSettings        set "UpdateDaughters"
        maxNumberOfCandidates  set 50000
}


talkto myDsJToDsstarPi0 {
       decayMode          set "D_s1+ -> D_s*+ pi0"
       daughterListNames  set "myDsstar"
       daughterListNames  set "pi0AllDefault"
       fittingAlgorithm   set "TreeFitter"
       fitConstraints     set "Beam"
       preFitSelectors    set "Mass 2.0:2.8"
       postFitSelectors   set "Mass 2.1:2.7"
       postFitSelectors   set "ProbChiSq 0.001:"
       fitSettings        set "InvalidateFit"
       fitSettings        set "FitAll"
       fitSettings        set "UpdateDaughters"
        maxNumberOfCandidates  set 50000
}


talkto myDsJToDsPiPi {
       decayMode          set "D_s1+ -> D_s+ pi+ pi-"
       daughterListNames  set "myDs"
       daughterListNames  set "piCombinedVeryLoose"
       daughterListNames  set "piCombinedVeryLoose"
       fittingAlgorithm   set "TreeFitter"
       fitConstraints     set "Beam"
       preFitSelectors    set "Mass 2.0:2.8"
       postFitSelectors   set "Mass 2.1:2.7"
       postFitSelectors   set "ProbChiSq 0.001:"
       fitSettings        set "InvalidateFit"
       fitSettings        set "FitAll"
       fitSettings        set "UpdateDaughters"
        maxNumberOfCandidates  set 50000
}



# the B0 lists

mod clone SmpMakerDefiner MyB0TomyDsJToDsPi0myDc
mod clone SmpMakerDefiner MyB0TomyDsJToDsgammamyDc
mod clone SmpMakerDefiner MyB0TomyDsJToDsstarPi0myDc
mod clone SmpMakerDefiner MyB0TomyDsJToDsPiPimyDc

catch { setProduction   MyB0TomyDsJToDsPi0myDc }
catch { setProduction   MyB0TomyDsJToDsgammamyDc }
catch { setProduction   MyB0TomyDsJToDsstarPi0myDc }
catch { setProduction   MyB0TomyDsJToDsPiPimyDc }


talkto MyB0TomyDsJToDsPi0myDc {
       decayMode             set "B0 -> D_s1+ D-"
       daughterListNames     set myDsJToDsPi0
       daughterListNames     set myDc
       fittingAlgorithm      set "TreeFitter"
       preFitSelectors       set "DeltaE -0.4:0.4"
       preFitSelectors       set "Mes 5.1:5.4"
       postFitSelectors      set "DeltaE -0.2:0.2"
       postFitSelectors      set "Mes 5.2:5.3"
       fitSettings           set "InvalidateFit"
       fitSettings           set "FitAll"
       fitSettings           set "UpdateDaughters"
       createUsrData     set  true
        maxNumberOfCandidates  set 50000
}



talkto MyB0TomyDsJToDsgammamyDc {
       decayMode             set "B0 -> D_s1+ D-"
       daughterListNames     set myDsJToDsgamma
       daughterListNames     set myDc
       fittingAlgorithm      set "TreeFitter"
       preFitSelectors       set "DeltaE -0.4:0.4"
       preFitSelectors       set "Mes 5.1:5.4"
       postFitSelectors      set "DeltaE -0.2:0.2"
       postFitSelectors      set "Mes 5.2:5.3"
       fitSettings           set "InvalidateFit"
       fitSettings           set "FitAll"
       fitSettings           set "UpdateDaughters"
       createUsrData     set  true
        maxNumberOfCandidates  set 50000
}


talkto MyB0TomyDsJToDsstarPi0myDc {
       decayMode             set "B0 -> D_s1+ D-"
       daughterListNames     set myDsJToDsstarPi0
       daughterListNames     set myDc
       fittingAlgorithm      set "TreeFitter"
       preFitSelectors       set "DeltaE -0.4:0.4"
       preFitSelectors       set "Mes 5.1:5.4"
       postFitSelectors      set "DeltaE -0.2:0.2"
       postFitSelectors      set "Mes 5.2:5.3"
       fitSettings           set "InvalidateFit"
       fitSettings           set "FitAll"
       fitSettings           set "UpdateDaughters"
       createUsrData     set  true
        maxNumberOfCandidates  set 50000
}


talkto MyB0TomyDsJToDsPiPimyDc {
       decayMode             set "B0 -> D_s1+ D-"
       daughterListNames     set myDsJToDsPiPi
       daughterListNames     set myDc
       fittingAlgorithm      set "TreeFitter"
       preFitSelectors       set "DeltaE -0.4:0.4"
       preFitSelectors       set "Mes 5.1:5.4"
       postFitSelectors      set "DeltaE -0.2:0.2"
       postFitSelectors      set "Mes 5.2:5.3"
       fitSettings           set "InvalidateFit"
       fitSettings           set "FitAll"
       fitSettings           set "UpdateDaughters"
       createUsrData     set  true
        maxNumberOfCandidates  set 50000
}




# the B+ lists

mod clone SmpMakerDefiner MyBcTomyDsJToDsPi0myD0bar
mod clone SmpMakerDefiner MyBcTomyDsJToDsgammamyD0bar
mod clone SmpMakerDefiner MyBcTomyDsJToDsstarPi0myD0bar
mod clone SmpMakerDefiner MyBcTomyDsJToDsPiPimyD0bar

catch { setProduction   MyBcTomyDsJToDsPi0myD0bar }
catch { setProduction   MyBcTomyDsJToDsgammamyD0bar }
catch { setProduction   MyBcTomyDsJToDsstarPi0myD0bar }
catch { setProduction   MyBcTomyDsJToDsPiPimyD0bar }


talkto MyBcTomyDsJToDsPi0myD0bar {
       decayMode             set "B+ -> D_s1+ anti-D0"
       daughterListNames     set myDsJToDsPi0
       daughterListNames     set myD0
       fittingAlgorithm      set "TreeFitter"
       preFitSelectors       set "DeltaE -0.4:0.4"
       preFitSelectors       set "Mes 5.1:5.4"
       postFitSelectors      set "DeltaE -0.2:0.2"
       postFitSelectors      set "Mes 5.2:5.3"
       fitSettings           set "InvalidateFit"
       fitSettings           set "FitAll"
       fitSettings           set "UpdateDaughters"
       createUsrData     set  true
        maxNumberOfCandidates  set 50000
}



talkto MyBcTomyDsJToDsgammamyD0bar {
       decayMode             set "B+ -> D_s1+ anti-D0"
       daughterListNames     set myDsJToDsgamma
       daughterListNames     set myD0
       fittingAlgorithm      set "TreeFitter"
       preFitSelectors       set "DeltaE -0.4:0.4"
       preFitSelectors       set "Mes 5.1:5.4"
       postFitSelectors      set "DeltaE -0.2:0.2"
       postFitSelectors      set "Mes 5.2:5.3"
       fitSettings           set "InvalidateFit"
       fitSettings           set "FitAll"
       fitSettings           set "UpdateDaughters"
       createUsrData     set  true
        maxNumberOfCandidates  set 50000
}


talkto MyBcTomyDsJToDsstarPi0myD0bar {
       decayMode             set "B+ -> D_s1+ anti-D0"
       daughterListNames     set myDsJToDsstarPi0
       daughterListNames     set myD0
       fittingAlgorithm      set "TreeFitter"
       preFitSelectors       set "DeltaE -0.4:0.4"
       preFitSelectors       set "Mes 5.1:5.4"
       postFitSelectors      set "DeltaE -0.2:0.2"
       postFitSelectors      set "Mes 5.2:5.3"
       fitSettings           set "InvalidateFit"
       fitSettings           set "FitAll"
       fitSettings           set "UpdateDaughters"
       createUsrData     set  true
        maxNumberOfCandidates  set 50000
}


talkto MyBcTomyDsJToDsPiPimyD0bar {
       decayMode             set "B+ -> D_s1+ anti-D0"
       daughterListNames     set myDsJToDsPiPi
       daughterListNames     set myD0
       fittingAlgorithm      set "TreeFitter"
       preFitSelectors       set "DeltaE -0.4:0.4"
       preFitSelectors       set "Mes 5.1:5.4"
       postFitSelectors      set "DeltaE -0.2:0.2"
       postFitSelectors      set "Mes 5.2:5.3"
       fitSettings           set "InvalidateFit"
       fitSettings           set "FitAll"
       fitSettings           set "UpdateDaughters"
       createUsrData     set  true
        maxNumberOfCandidates  set 50000
}









path append Everything GammaForDs 
path append Everything pi0AllDefault 
path append Everything Ks_Pid 
path append Everything myD0ToKPi 
path append Everything myD0ToKPiPi0 
path append Everything myD0ToKsPiPi 
path append Everything myD0ToKsPiPiPi0 
path append Everything myD0ToK3Pi 
path append Everything myD0ToK3PiPi0 
path append Everything myDcToKPiPi 
path append Everything myDcToKPiPiPi0 
path append Everything myDcToKsPi 
path append Everything myDcToKsPiPi0 
path append Everything myD0 
path append Everything myDc 
path append Everything myDsToKKPi 
path append Everything myDsToKKPiPi0 
path append Everything myDs 
path append Everything myDsstar 
path append Everything myDsJToDsPi0 
path append Everything myDsJToDsgamma 
path append Everything myDsJToDsstarPi0 
path append Everything myDsJToDsPiPi 
path append Everything MyB0TomyDsJToDsPi0myDc 
path append Everything MyB0TomyDsJToDsgammamyDc 
path append Everything MyB0TomyDsJToDsstarPi0myDc 
path append Everything MyB0TomyDsJToDsPiPimyDc 
path append Everything MyBcTomyDsJToDsPi0myD0bar 
path append Everything MyBcTomyDsJToDsgammamyD0bar 
path append Everything MyBcTomyDsJToDsstarPi0myD0bar 
path append Everything MyBcTomyDsJToDsPiPimyD0bar 




#====================== NTUPLE DUMPING ========================================
#..Use BtuTupleMaker to write out ntuples for SimpleComposition job

mod clone BtuTupleMaker B0TomyDsJToDsPi0myDc 
mod clone BtuTupleMaker B0TomyDsJToDsgammamyDc 
mod clone BtuTupleMaker B0TomyDsJToDsstarPi0myDc 
mod clone BtuTupleMaker B0TomyDsJToDsPiPimyDc 
mod clone BtuTupleMaker BcTomyDsJToDsPi0myD0bar 
mod clone BtuTupleMaker BcTomyDsJToDsgammamyD0bar 
mod clone BtuTupleMaker BcTomyDsJToDsstarPi0myD0bar 
mod clone BtuTupleMaker BcTomyDsJToDsPiPimyD0bar 

path append Everything  B0TomyDsJToDsPi0myDc 
path append Everything  B0TomyDsJToDsgammamyDc 
path append Everything  B0TomyDsJToDsstarPi0myDc 
path append Everything  B0TomyDsJToDsPiPimyDc 
path append Everything  BcTomyDsJToDsPi0myD0bar 
path append Everything  BcTomyDsJToDsgammamyD0bar 
path append Everything  BcTomyDsJToDsstarPi0myD0bar 
path append Everything  BcTomyDsJToDsPiPimyD0bar 

#1
talkto  B0TomyDsJToDsPi0myDc {
ntupleName set B0ToDsJToDsPi0Dc
#-------------------- Event Information ---------------------------------------
   eventBlockContents set "EventID CMp4 BeamSpot"
   eventTagsBool      set "BGFMultiHadron"
   eventTagsInt       set "nTracks"
   eventTagsFloat set "R2 R2All xPrimaryVtx yPrimaryVtx zPrimaryVtx"
   writeEveryEvent set false
#-------------------- MC truth info -------------------------------------------
    fillMC set false
   #write all cands info
#   checkClones set false
#-------------------- -------------------------------------------------
#..Now the particle blocks...
#=========================================
    listToDump set MyB0TomyDsJToDsPi0myDc
#=========================================
    ntpBlockConfigs set "B0        B0  2       50000"
    ntpBlockContents set "B0   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(MyB0TomyDsJToDsPi0myDc)"
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "D_s1+        D_sJ  3       50000"
    ntpBlockContents set "D_sJ   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "D-        D  4       50000"
    ntpBlockContents set "D   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "D_s+        Ds  4       50000"
    ntpBlockContents set "Ds   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#--------------------------------------------------------------------------
    ntpBlockConfigs set "K_S0        K_S  2       50000"
    ntpBlockContents set "K_S   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(Ks_Pid)"
#--------------------------------------------------------------------------
    ntpBlockConfigs set "pi0        pi0  2       50000"
    ntpBlockContents set "pi0   :  Mass CMMomentum Momentum UsrData(pi0AllDefault)"
#-------------------- Single Particles -------------------------------------
    ntpBlockConfigs set "K-            K      0       50000"
    ntpBlockContents set "K: CMMomentum Momentum Doca DocaXY Poca"
    ntpBlockConfigs set "pi+            pi      0       50000"
    ntpBlockContents set "pi: CMMomentum Momentum Doca DocaXY Poca"

#..Want to save all CalorNeutrals in the gamma block
    ntpBlockConfigs set "gamma   gamma  0      50000"
    ntpBlockContents set "gamma: CMMomentum Momentum"
    gamExtraContents set EMC
                            
#..TRK block. Save all of them as well.
#    fillAllCandsInList set "TRK ChargedTracks"
#    ntpBlockToTrk    set "K pi"
#    trkExtraContents set "BitMap:KSelectorsMap,piSelectorsMap,TracksMap"
#    trkExtraContents set HOTS:detailSVT,detailDCH
#    trkExtraContents set Eff:ave, charge
#    trkExtraContents set Dirc
#    ntpBlockContents set "TRK: Momentum Doca DocaXY"
}

#2
talkto  B0TomyDsJToDsgammamyDc {
ntupleName set B0ToDsJToDsgammaDc
#-------------------- Event Information ---------------------------------------
   eventBlockContents set "EventID CMp4 BeamSpot"
   eventTagsBool      set "BGFMultiHadron"
   eventTagsInt       set "nTracks"
   eventTagsFloat set "R2 R2All xPrimaryVtx yPrimaryVtx zPrimaryVtx"
   writeEveryEvent set false
#-------------------- MC truth info -------------------------------------------
    fillMC set false
   #write all cands info
#   checkClones set false
#-------------------- -------------------------------------------------
#..Now the particle blocks...

#=========================================
    listToDump set MyB0TomyDsJToDsgammamyDc
#=========================================
    ntpBlockConfigs set "B0        B0  2       50000"
    ntpBlockContents set "B0   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(MyB0TomyDsJToDsgammamyDc)"
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "D_s1+        D_sJ  3       50000"
    ntpBlockContents set "D_sJ   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "D-        D  4       50000"
    ntpBlockContents set "D   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "D_s+        Ds  4       50000"
    ntpBlockContents set "Ds   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#--------------------------------------------------------------------------
    ntpBlockConfigs set "K_S0        K_S  2       50000"
    ntpBlockContents set "K_S   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(Ks_Pid)"
#--------------------------------------------------------------------------
    ntpBlockConfigs set "pi0        pi0  2       50000"
    ntpBlockContents set "pi0   :  Mass CMMomentum Momentum UsrData(pi0AllDefault)"
#-------------------- Single Particles -------------------------------------
    ntpBlockConfigs set "K-            K      0       50000"
    ntpBlockContents set "K: CMMomentum Momentum Doca DocaXY Poca"
    ntpBlockConfigs set "pi+            pi      0       50000"
    ntpBlockContents set "pi: CMMomentum Momentum Doca DocaXY Poca"

#..Want to save all CalorNeutrals in the gamma block
    ntpBlockConfigs set "gamma   gamma  0      50000"
    ntpBlockContents set "gamma: CMMomentum Momentum"
    gamExtraContents set EMC
                            
#..TRK block. Save all of them as well.
#    fillAllCandsInList set "TRK ChargedTracks"
#    ntpBlockToTrk    set "K pi"
#    trkExtraContents set "BitMap:KSelectorsMap,piSelectorsMap,TracksMap"
#    trkExtraContents set HOTS:detailSVT,detailDCH
#    trkExtraContents set Eff:ave, charge
#    trkExtraContents set Dirc
#    ntpBlockContents set "TRK: Momentum Doca DocaXY"
}

#
#3
talkto  B0TomyDsJToDsstarPi0myDc {
ntupleName set B0ToDsJToDsstarPi0Dc
#-------------------- Event Information ---------------------------------------
   eventBlockContents set "EventID CMp4 BeamSpot"
   eventTagsBool      set "BGFMultiHadron"
   eventTagsInt       set "nTracks"
   eventTagsFloat set "R2 R2All xPrimaryVtx yPrimaryVtx zPrimaryVtx"
   writeEveryEvent set false
#-------------------- MC truth info -------------------------------------------
    fillMC set false
   #write all cands info
#   checkClones set false
#-------------------- -------------------------------------------------
#..Now the particle blocks...
#=========================================
    listToDump set MyB0TomyDsJToDsstarPi0myDc
#=========================================
    ntpBlockConfigs set "B0        B0  2       50000"
    ntpBlockContents set "B0   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(MyB0TomyDsJToDsstarPi0myDc)"
#-------------------------------------------------------------------------
    ntpBlockConfigs set "D_s1+        D_sJ  3       50000"
    ntpBlockContents set "D_sJ   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "D-        D  4       50000"
    ntpBlockContents set "D   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "D_s*+        Dsstar  2       50000"
    ntpBlockContents set "Dsstar   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "D_s+        Ds  4       50000"
    ntpBlockContents set "Ds   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "K_S0        K_S  2       50000"
    ntpBlockContents set "K_S   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(Ks_Pid)"
#--------------------------------------------------------------------------
    ntpBlockConfigs set "pi0        pi0  2       50000"
    ntpBlockContents set "pi0   :  Mass CMMomentum Momentum UsrData(pi0AllDefault)"
#-------------------- Single Particles -------------------------------------
    ntpBlockConfigs set "K-            K      0       50000"
    ntpBlockContents set "K: CMMomentum Momentum Doca DocaXY Poca"
    ntpBlockConfigs set "pi+            pi      0       50000"
    ntpBlockContents set "pi: CMMomentum Momentum Doca DocaXY Poca"

#..Want to save all CalorNeutrals in the gamma block
    ntpBlockConfigs set "gamma   gamma  0      50000"
    ntpBlockContents set "gamma: CMMomentum Momentum"
    gamExtraContents set EMC
                            
#..TRK block. Save all of them as well.
#    fillAllCandsInList set "TRK ChargedTracks"
#    ntpBlockToTrk    set "K pi"
#    trkExtraContents set "BitMap:KSelectorsMap,piSelectorsMap,TracksMap"
#    trkExtraContents set HOTS:detailSVT,detailDCH
#    trkExtraContents set Eff:ave, charge
#    trkExtraContents set Dirc
#    ntpBlockContents set "TRK: Momentum Doca DocaXY"
}

#4
talkto  B0TomyDsJToDsPiPimyDc {
ntupleName set B0ToDsJToDsPiPiDc
#-------------------- Event Information ---------------------------------------
   eventBlockContents set "EventID CMp4 BeamSpot"
   eventTagsBool      set "BGFMultiHadron"
   eventTagsInt       set "nTracks"
   eventTagsFloat set "R2 R2All xPrimaryVtx yPrimaryVtx zPrimaryVtx"
   writeEveryEvent set false
#-------------------- MC truth info -------------------------------------------
    fillMC set false
   #write all cands info
#   checkClones set false
#-------------------- -------------------------------------------------
#..Now the particle blocks...
#=========================================
    listToDump set MyB0TomyDsJToDsPiPimyDc
#=========================================
    ntpBlockConfigs set "B0        B0  2       50000"
    ntpBlockContents set "B0   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(MyB0TomyDsJToDsPiPimyDc)"
#-------------------------------------------------------------------------
    ntpBlockConfigs set "D_s1+        D_sJ  3       50000"
    ntpBlockContents set "D_sJ   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "D-        D  4       50000"
    ntpBlockContents set "D   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "D_s+        Ds  4       50000"
    ntpBlockContents set "Ds   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#--------------------------------------------------------------------------
    ntpBlockConfigs set "K_S0        K_S  2       50000"
    ntpBlockContents set "K_S   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(Ks_Pid)"
#--------------------------------------------------------------------------
    ntpBlockConfigs set "pi0        pi0  2       50000"
    ntpBlockContents set "pi0   :  Mass CMMomentum Momentum UsrData(pi0AllDefault)"
#-------------------- Single Particles -------------------------------------
    ntpBlockConfigs set "K-            K      0       50000"
    ntpBlockContents set "K: CMMomentum Momentum Doca DocaXY Poca"
    ntpBlockConfigs set "pi+            pi      0       50000"
    ntpBlockContents set "pi: CMMomentum Momentum Doca DocaXY Poca"

#..Want to save all CalorNeutrals in the gamma block
    ntpBlockConfigs set "gamma   gamma  0      50000"
    ntpBlockContents set "gamma: CMMomentum Momentum"
    gamExtraContents set EMC
                            
#..TRK block. Save all of them as well.
#    fillAllCandsInList set "TRK ChargedTracks"
#    ntpBlockToTrk    set "K pi"
#    trkExtraContents set "BitMap:KSelectorsMap,piSelectorsMap,TracksMap"
#    trkExtraContents set HOTS:detailSVT,detailDCH
#    trkExtraContents set Eff:ave, charge
#    trkExtraContents set Dirc
#    ntpBlockContents set "TRK: Momentum Doca DocaXY"
}

#5

#6

#7

#8

#9
talkto  BcTomyDsJToDsPi0myD0bar {
ntupleName set BcToDsJToDsPi0D0bar
#-------------------- Event Information ---------------------------------------
   eventBlockContents set "EventID CMp4 BeamSpot"
   eventTagsBool      set "BGFMultiHadron"
   eventTagsInt       set "nTracks"
   eventTagsFloat set "R2 R2All xPrimaryVtx yPrimaryVtx zPrimaryVtx"
   writeEveryEvent set false
#-------------------- MC truth info -------------------------------------------
    fillMC set false
   #write all cands info
#   checkClones set false
#-------------------- -------------------------------------------------
#..Now the particle blocks...
#=========================================
    listToDump set MyBcTomyDsJToDsPi0myD0bar
#=========================================
    ntpBlockConfigs set "B+        Bc  2       50000"
    ntpBlockContents set "Bc   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(MyBcTomyDsJToDsPi0myD0bar)"
#-------------------------------------------------------------------------
    ntpBlockConfigs set "D_s1+        D_sJ  3       50000"
    ntpBlockContents set "D_sJ   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "anti-D0        D0  5       50000"
    ntpBlockContents set "D0   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "D_s+        Ds  4       50000"
    ntpBlockContents set "Ds   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#--------------------------------------------------------------------------
    ntpBlockConfigs set "K_S0        K_S  2       50000"
    ntpBlockContents set "K_S   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(Ks_Pid)"
#--------------------------------------------------------------------------
    ntpBlockConfigs set "pi0        pi0  2       50000"
    ntpBlockContents set "pi0   :  Mass CMMomentum Momentum UsrData(pi0AllDefault)"
#-------------------- Single Particles -------------------------------------
    ntpBlockConfigs set "K-            K      0       50000"
    ntpBlockContents set "K: CMMomentum Momentum Doca DocaXY Poca"
    ntpBlockConfigs set "pi+            pi      0       50000"
    ntpBlockContents set "pi: CMMomentum Momentum Doca DocaXY Poca"

#..Want to save all CalorNeutrals in the gamma block
    ntpBlockConfigs set "gamma   gamma  0      50000"
    ntpBlockContents set "gamma: CMMomentum Momentum"
    gamExtraContents set EMC
                            
#..TRK block. Save all of them as well.
#    fillAllCandsInList set "TRK ChargedTracks"
#    ntpBlockToTrk    set "K pi"
#    trkExtraContents set "BitMap:KSelectorsMap,piSelectorsMap,TracksMap"
#    trkExtraContents set HOTS:detailSVT,detailDCH
#    trkExtraContents set Eff:ave, charge
#    trkExtraContents set Dirc
#    ntpBlockContents set "TRK: Momentum Doca DocaXY"
}

#10
talkto  BcTomyDsJToDsgammamyD0bar {
ntupleName set BcToDsJToDsgammaD0bar
#-------------------- Event Information ---------------------------------------
   eventBlockContents set "EventID CMp4 BeamSpot"
   eventTagsBool      set "BGFMultiHadron"
   eventTagsInt       set "nTracks"
   eventTagsFloat set "R2 R2All xPrimaryVtx yPrimaryVtx zPrimaryVtx"
   writeEveryEvent set false
#-------------------- MC truth info -------------------------------------------
    fillMC set false
   #write all cands info
#   checkClones set false
#-------------------- -------------------------------------------------
#..Now the particle blocks...
#=========================================
    listToDump set MyBcTomyDsJToDsgammamyD0bar
#=========================================
    ntpBlockConfigs set "B+        Bc  2       50000"
    ntpBlockContents set "Bc   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(MyBcTomyDsJToDsgammamyD0bar)"
#-------------------------------------------------------------------------
    ntpBlockConfigs set "D_s1+        D_sJ  3       50000"
    ntpBlockContents set "D_sJ   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "anti-D0        D0  5       50000"
    ntpBlockContents set "D0   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "D_s+        Ds  4       50000"
    ntpBlockContents set "Ds   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#--------------------------------------------------------------------------
    ntpBlockConfigs set "K_S0        K_S  2       50000"
    ntpBlockContents set "K_S   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(Ks_Pid)"
#--------------------------------------------------------------------------
    ntpBlockConfigs set "pi0        pi0  2       50000"
    ntpBlockContents set "pi0   :  Mass CMMomentum Momentum UsrData(pi0AllDefault)"
#-------------------- Single Particles -------------------------------------
    ntpBlockConfigs set "K-            K      0       50000"
    ntpBlockContents set "K: CMMomentum Momentum Doca DocaXY Poca"
    ntpBlockConfigs set "pi+            pi      0       50000"
    ntpBlockContents set "pi: CMMomentum Momentum Doca DocaXY Poca"

#..Want to save all CalorNeutrals in the gamma block
    ntpBlockConfigs set "gamma   gamma  0      50000"
    ntpBlockContents set "gamma: CMMomentum Momentum"
    gamExtraContents set EMC
                            
#..TRK block. Save all of them as well.
#    fillAllCandsInList set "TRK ChargedTracks"
#    ntpBlockToTrk    set "K pi"
#    trkExtraContents set "BitMap:KSelectorsMap,piSelectorsMap,TracksMap"
#    trkExtraContents set HOTS:detailSVT,detailDCH
#    trkExtraContents set Eff:ave, charge
#    trkExtraContents set Dirc
#    ntpBlockContents set "TRK: Momentum Doca DocaXY"
}

#11
talkto  BcTomyDsJToDsstarPi0myD0bar {
ntupleName set BcToDsJToDsstarPi0D0bar
#-------------------- Event Information ---------------------------------------
   eventBlockContents set "EventID CMp4 BeamSpot"
   eventTagsBool      set "BGFMultiHadron"
   eventTagsInt       set "nTracks"
   eventTagsFloat set "R2 R2All xPrimaryVtx yPrimaryVtx zPrimaryVtx"
   writeEveryEvent set false
#-------------------- MC truth info -------------------------------------------
    fillMC set false
   #write all cands info
#   checkClones set false
#-------------------- -------------------------------------------------
#..Now the particle blocks...
#=========================================
    listToDump set MyBcTomyDsJToDsstarPi0myD0bar
#=========================================
    ntpBlockConfigs set "B+        Bc  2       50000"
    ntpBlockContents set "Bc   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(MyBcTomyDsJToDsstarPi0myD0bar)"
#-------------------------------------------------------------------------
    ntpBlockConfigs set "D_s1+        D_sJ  3       50000"
    ntpBlockContents set "D_sJ   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "anti-D0        D0  5       50000"
    ntpBlockContents set "D0   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "D_s*+        Dsstar  2       50000"
    ntpBlockContents set "Dsstar   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
   ntpBlockConfigs set "D_s+        Ds  4       50000"
    ntpBlockContents set "Ds   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#--------------------------------------------------------------------------
    ntpBlockConfigs set "K_S0        K_S  2       50000"
    ntpBlockContents set "K_S   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(Ks_Pid)"
#--------------------------------------------------------------------------
    ntpBlockConfigs set "pi0        pi0  2       50000"
    ntpBlockContents set "pi0   :  Mass CMMomentum Momentum UsrData(pi0AllDefault)"
#-------------------- Single Particles -------------------------------------
    ntpBlockConfigs set "K-            K      0       50000"
    ntpBlockContents set "K: CMMomentum Momentum Doca DocaXY Poca"
    ntpBlockConfigs set "pi+            pi      0       50000"
    ntpBlockContents set "pi: CMMomentum Momentum Doca DocaXY Poca"

#..Want to save all CalorNeutrals in the gamma block
    ntpBlockConfigs set "gamma   gamma  0      50000"
    ntpBlockContents set "gamma: CMMomentum Momentum"
    gamExtraContents set EMC
                            
#..TRK block. Save all of them as well.
#    fillAllCandsInList set "TRK ChargedTracks"
#    ntpBlockToTrk    set "K pi"
#    trkExtraContents set "BitMap:KSelectorsMap,piSelectorsMap,TracksMap"
#    trkExtraContents set HOTS:detailSVT,detailDCH
#    trkExtraContents set Eff:ave, charge
#    trkExtraContents set Dirc
#    ntpBlockContents set "TRK: Momentum Doca DocaXY"
}

#12
talkto  BcTomyDsJToDsPiPimyD0bar {
ntupleName set BcToDsJToDsPiPiD0bar
#-------------------- Event Information ---------------------------------------
   eventBlockContents set "EventID CMp4 BeamSpot"
   eventTagsBool      set "BGFMultiHadron"
   eventTagsInt       set "nTracks"
   eventTagsFloat set "R2 R2All xPrimaryVtx yPrimaryVtx zPrimaryVtx"
   writeEveryEvent set false
#-------------------- MC truth info -------------------------------------------
    fillMC set false
   #write all cands info
#   checkClones set false
#-------------------- -------------------------------------------------
#..Now the particle blocks...
#=========================================
    listToDump set MyBcTomyDsJToDsPiPimyD0bar
#=========================================
    ntpBlockConfigs set "B+        Bc  2       50000"
    ntpBlockContents set "Bc   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(MyBcTomyDsJToDsPiPimyD0bar)"
#-------------------------------------------------------------------------
    ntpBlockConfigs set "D_s1+        D_sJ  3       50000"
    ntpBlockContents set "D_sJ   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "anti-D0        D0  5       50000"
    ntpBlockContents set "D0   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#----------------------- -------------------------------------------------
    ntpBlockConfigs set "D_s+        Ds  4       50000"
    ntpBlockContents set "Ds   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#--------------------------------------------------------------------------
    ntpBlockConfigs set "K_S0        K_S  2       50000"
    ntpBlockContents set "K_S   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(Ks_Pid)"
#--------------------------------------------------------------------------
    ntpBlockConfigs set "pi0        pi0  2       50000"
    ntpBlockContents set "pi0   :  Mass CMMomentum Momentum UsrData(pi0AllDefault)"
#-------------------- Single Particles -------------------------------------
    ntpBlockConfigs set "K-            K      0       50000"
    ntpBlockContents set "K: CMMomentum Momentum Doca DocaXY Poca"
    ntpBlockConfigs set "pi+            pi      0       50000"
    ntpBlockContents set "pi: CMMomentum Momentum Doca DocaXY Poca"

#..Want to save all CalorNeutrals in the gamma block
    ntpBlockConfigs set "gamma   gamma  0      50000"
    ntpBlockContents set "gamma: CMMomentum Momentum"
    gamExtraContents set EMC
                            
#..TRK block. Save all of them as well.
#    fillAllCandsInList set "TRK ChargedTracks"
#    ntpBlockToTrk    set "K pi"
#    trkExtraContents set "BitMap:KSelectorsMap,piSelectorsMap,TracksMap"
#    trkExtraContents set HOTS:detailSVT,detailDCH
#    trkExtraContents set Eff:ave, charge
#    trkExtraContents set Dirc
#    ntpBlockContents set "TRK: Momentum Doca DocaXY"
}

#13

#14

#15

#16

#mod disable B0TomyDsJToDsPi0myDc 
#mod disable MyB0TomyDsJToDsPi0myDc 
#mod disable B0TomyDsJToDsgammamyDc 
#mod disable MyB0TomyDsJToDsgammamyDc 
#mod disable B0TomyDsJToDsstarPi0myDc 
#mod disable MyB0TomyDsJToDsstarPi0myDc 
#mod disable B0TomyDsJToDsPiPimyDc 
#mod disable MyB0TomyDsJToDsPiPimyDc 
mod disable BcTomyDsJToDsPi0myD0bar 
mod disable MyBcTomyDsJToDsPi0myD0bar 
mod disable BcTomyDsJToDsgammamyD0bar 
mod disable MyBcTomyDsJToDsgammamyD0bar 
mod disable BcTomyDsJToDsstarPi0myD0bar 
mod disable MyBcTomyDsJToDsstarPi0myD0bar 
mod disable BcTomyDsJToDsPiPimyD0bar 
mod disable MyBcTomyDsJToDsPiPimyD0bar 


module talk EvtCounter
printFreq set 1000
exit

#path list
if [info exists NEvent] {
   ev begin -nev $NEvent
} else {
  ev begin
}

ErrMsg trace "completed OK"
exit





