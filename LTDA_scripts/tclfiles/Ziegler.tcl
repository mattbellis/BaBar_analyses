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


# final state cands Lists:
talkto GammaForEta {
        selectors set "LabE 0.080:10.0"
}
mod clone SmpMakerDefiner myetagg
catch { setProduction myetagg }
talkto myetagg {
         decayMode          set "eta -> gamma gamma"
         daughterListNames  set "GammaForEta"
         daughterListNames  set "GammaForEta"
         fitConstraints     set "PrimaryVertex"
         fitConstraints     set "Momentum"
         fitConstraints     set "Mass"
         fittingAlgorithm   set "Add4"
         preFitSelectors    set "LabP 0.200:10.0"
         preFitSelectors    set "Mass 0.470:0.620"
         postFitSelectors   set "Mass 0.470:0.620"
         fitSettings        set "UpdateDaughters"
}

mod clone SmpMakerDefiner myetaP
catch { setProduction myetaP }
talkto myetaP {
         decayMode          set "eta' -> eta pi+ pi-"
         daughterListNames  set "myetagg"
         createUsrData      set  true
         daughterListNames  set "GoodTracksLoose"
         daughterListNames  set "GoodTracksLoose"
         fittingAlgorithm   set "TreeFitter"
         preFitSelectors    set "Mass 0.91:1.00"
         postFitSelectors   set "Mass 0.91:1.00"
         postFitSelectors   set "ProbChiSq 0.001:"
         fitConstraints     set "Mass"
         fitSettings        set "UpdateDaughters"
}
mod clone SmpRefinerDefiner Ks_Pid
catch { setProduction Ks_Pid }
#Refine the default Ks list
talkto Ks_Pid {
        decayMode         set "K_S0 -> pi+ pi-"
        unrefinedListName set  KsDefault
        createUsrData     set  true
        fittingAlgorithm  set "TreeFitter"
        preFitSelectors   set "Mass 0.47267:0.52267"
        postFitSelectors  set "ProbChiSq 0.001:"
        postFitSelectors  set "FlightSignificance 0:"
        fitConstraints    set "Mass"
        fitSettings       set "UpdateDaughters"
}

mod clone SmpMakerDefiner myDcToEtaPiKs
mod clone SmpMakerDefiner myDcToEta_pPiKs

catch { setProduction myDcToEtaPiKs }
catch { setProduction myDcToEta_pPiKs }

talkto myDcToEtaPiKs {
       decayMode          set "D+ -> eta K_S0 pi+"
       daughterListNames  set "myetagg"
       daughterListNames  set "Ks_Pid"
       daughterListNames  set "piLHTight"
       fittingAlgorithm   set "TreeFitter"
       preFitSelectors    set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "ProbChiSq 0.001:"
       postFitSelectors   set "CmsP 2.5:"
       fitSettings        set "UpdateDaughters"
}
talkto myDcToEta_pPiKs {
       decayMode          set "D+ -> eta' K_S0 pi+"
       daughterListNames  set "myetaP"
       daughterListNames  set "Ks_Pid"
       daughterListNames  set "piLHTight"
       fittingAlgorithm   set "TreeFitter"
       preFitSelectors    set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "Mass pdg-0.12:pdg+0.12"
       postFitSelectors   set "ProbChiSq 0.001:"
       postFitSelectors   set "CmsP 2.5:"
       fitSettings        set "UpdateDaughters"
}

#====================== NTUPLE DUMPING 
========================================
#..Use BtuTupleMaker to write out ntuples for SimpleComposition job

path append Everything GammaForEta
path append Everything myetagg
path append Everything myetaP
path append Everything Ks_Pid

path append Everything myDcToEtaPiKs
path append Everything myDcToEta_pPiKs


mod clone BtuTupleMaker BtuTupleMakerEKsPi
path append Everything BtuTupleMakerEKsPi
mod clone BtuTupleMaker BtuTupleMakerEpKsPi
path append Everything BtuTupleMakerEpKsPi


talkto BtuTupleMakerEKsPi {
ntupleName set EKsPi
#-------------------- Event Information 
---------------------------------------
   eventBlockContents set "EventID CMp4 BeamSpot"
   eventTagsBool      set "BGFMultiHadron"
   eventTagsInt       set "nTracks"
   eventTagsFloat set "R2All xPrimaryVtx yPrimaryVtx zPrimaryVtx"
   writeEveryEvent set false
#-------------------- MC truth info 
-------------------------------------------
    fillMC set false
   #write all cands info
   checkClones set false
#-------------------- -------------------------------------------------
#..Now the particle blocks...
#===========================================
    listToDump set myDcToEtaPiKs
#===========================================
    ntpBlockConfigs set "D+        Dc  3       50"
    ntpBlockContents set "Dc   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#-------------------- K_S 
-----------------------------------------------------
    ntpBlockConfigs set "K_S0        K_S  2       50"
    ntpBlockContents set "K_S   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(Ks_Pid)"
#-------------------- eta 
-----------------------------------------------------
    ntpBlockConfigs set "eta        eta  2       50"
    ntpBlockContents set "eta   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#-------------------- Single Particles 
----------------------------------------
    ntpBlockConfigs set "pi+            pi      0       50"
    ntpBlockContents set "pi: CMMomentum Momentum Doca DocaXY Poca"

#..Want to save all CalorNeutrals in the gamma block
    ntpBlockConfigs set "gamma   gamma  0      90"
    ntpBlockContents set "gamma: CMMomentum Momentum"
    gamExtraContents set EMC

#..TRK block. Save all of them as well.
    fillAllCandsInList set "TRK ChargedTracks"
    ntpBlockToTrk    set "pi"
    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,TracksMap"
    trkExtraContents set HOTS:detailSVT,detailDCH
    trkExtraContents set Eff:ave, charge
    trkExtraContents set Dirc
    ntpBlockContents set "TRK: Momentum Doca DocaXY"
}

#

talkto BtuTupleMakerEpKsPi {
ntupleName set EpKsPi

#-------------------- Event Information 
---------------------------------------
   eventBlockContents set "EventID CMp4 BeamSpot"
   eventTagsBool      set "BGFMultiHadron"
   eventTagsInt       set "nTracks"
   eventTagsFloat set "R2All xPrimaryVtx yPrimaryVtx zPrimaryVtx"
   writeEveryEvent set false
#-------------------- MC truth info 
-------------------------------------------
    fillMC set false
   #write all cands info
   checkClones set false
#--------------------------------------------------------------------
#..Now the particle blocks...
#===========================================
    listToDump set myDcToEta_pPiKs
#===========================================
    ntpBlockConfigs set "D+        Dc  3       50"
    ntpBlockContents set "Dc   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#-------------------- K_S 
-----------------------------------------------------
    ntpBlockConfigs set "K_S0        K_S  2       50"
    ntpBlockContents set "K_S   :  Mass CMMomentum Momentum Vertex VtxChi2 UsrData(Ks_Pid)"
#-------------------- eta' -------------------------------------------------
    ntpBlockConfigs set "eta'        etaP  3       50"
    ntpBlockContents set "etaP   : Mass CMMomentum Momentum Vertex VtxChi2 UsrData(myetaP)"
#-------------------- eta 
-----------------------------------------------------
    ntpBlockConfigs set "eta        eta  2       50"
    ntpBlockContents set "eta   :  Mass CMMomentum Momentum Vertex VtxChi2 "
#-------------------- Single Particles 
----------------------------------------
    ntpBlockConfigs set "pi+            pi      0       50"
    ntpBlockContents set "pi: CMMomentum Momentum Doca DocaXY Poca"

#..Want to save all CalorNeutrals in the gamma block
    ntpBlockConfigs set "gamma   gamma  0      90"
    ntpBlockContents set "gamma: CMMomentum Momentum"
    gamExtraContents set EMC

#..TRK block. Save all of them as well.
    fillAllCandsInList set "TRK ChargedTracks"
    ntpBlockToTrk    set "pi"
    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,TracksMap"
    trkExtraContents set HOTS:detailSVT,detailDCH
    trkExtraContents set Eff:ave, charge
    trkExtraContents set Dirc
    ntpBlockContents set "TRK: Momentum Doca DocaXY"
}


#
#  Turn off some specialty items
#
module disable BtuMyAnalysis
module disable Psi2S3bodyEE
module disable Psi2S3bodyMuMu


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
