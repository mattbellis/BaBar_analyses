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
#### Do SimpleComposition
seq create SmpMyD_mup
seq create SmpMyD_ep
seq create SmpMyD_mum
seq create SmpMyD_em

# muon+
mod clone SmpMakerDefiner myD_mup
seq append SmpMyD_mup myD_mup
catch { setProduction myD_mup }

# muon-
mod clone SmpMakerDefiner myD_mum
seq append SmpMyD_mum myD_mum
catch { setProduction myD_mum }

# electron+
mod clone SmpMakerDefiner myD_ep
seq append SmpMyD_ep myD_ep
catch { setProduction myD_ep }

# electron-
mod clone SmpMakerDefiner myD_em
seq append SmpMyD_em myD_em
catch { setProduction myD_em }

#####################################################################
# Set up the Smp stuff
# mu+
talkto myD_mup {
    debug              set f
    verbose            set f
    decayMode          set "D+ -> Lambda0 mu+"
    daughterListNames  set "LambdaDefault"
    daughterListNames  set "muCombinedVeryLooseFakeRate"

    fittingAlgorithm   set "TreeFitter"
    fitConstraints     set "Geo"
    fitSettings        set "InvalidateFit"
    preFitSelectors    set "Mass 1.7:2.0"
    preFitSelectors    set "CmsP 2.0:"

    createUsrData  set t
}

# mu-
talkto myD_mum {
    debug              set f
    verbose            set f
    decayMode          set "D- -> Lambda0 mu-"
    daughterListNames  set "LambdaDefault"
    daughterListNames  set "muCombinedVeryLooseFakeRate"

    fittingAlgorithm   set "TreeFitter"
    fitConstraints     set "Geo"
    fitSettings        set "InvalidateFit"
    preFitSelectors    set "Mass 1.7:2.0"
    preFitSelectors    set "CmsP 2.0:"

    createUsrData  set t
}

# electron+
talkto myD_ep {
    debug              set f
    verbose            set f
    decayMode          set "D+ -> Lambda0 e+"
    daughterListNames  set "LambdaDefault"
    daughterListNames  set "eCombinedSuperLoose"

    fittingAlgorithm   set "TreeFitter"
    fitConstraints     set "Geo"
    fitSettings        set "InvalidateFit"
    preFitSelectors    set "Mass 1.7:2.0"
    preFitSelectors    set "CmsP 2.0:"

    createUsrData  set t
}

# electron-
talkto myD_em {
    debug              set f
    verbose            set f
    decayMode          set "D- -> Lambda0 e-"
    daughterListNames  set "LambdaDefault"
    daughterListNames  set "eCombinedSuperLoose"

    fittingAlgorithm   set "TreeFitter"
    fitConstraints     set "Geo"
    fitSettings        set "InvalidateFit"
    preFitSelectors    set "Mass 1.7:2.0"
    preFitSelectors    set "CmsP 2.0:"

    createUsrData  set t
}

#####################################################################
## Add Analysis module
##
path append Everything SmpMyD_mup
path append Everything SmpMyD_ep
path append Everything SmpMyD_mum
path append Everything SmpMyD_em

mod  clone  BtuTupleMaker BtuTupleMaker_mup
path append Everything    BtuTupleMaker_mup

mod  clone  BtuTupleMaker BtuTupleMaker_mum
path append Everything    BtuTupleMaker_mum

mod  clone  BtuTupleMaker BtuTupleMaker_ep
path append Everything    BtuTupleMaker_ep

mod  clone  BtuTupleMaker BtuTupleMaker_em
path append Everything    BtuTupleMaker_em
#####################################################################
# mu+
talkto BtuTupleMaker_mup {
  
    ntupleName set ntp1_Lambda0mup
    listToDump set myD_mup

    fillMC set true

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsInt       set "nTracks nGoodTrkLoose"
    eventTagsFloat     set "R2All"

    mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    ntpBlockConfigs set "D+         D             2   100"
    ntpBlockConfigs set "Lambda0    Lambda0       2   20"
    ntpBlockConfigs set "mu+        mu            0   30"
    ntpBlockConfigs set "p+         p             0   20"
    ntpBlockConfigs set "pi+        pi            0   30"

    ntpBlockContents set "D         : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(myD_mup) ShapeVars"
    ntpBlockContents set "Lambda0   : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 Flight FlightBS"
    ntpBlockContents set "pi        : Momentum CMMomentum MCIdx"
    ntpBlockContents set "p         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "mu        : Momentum CMMomentum MCIdx"
    ntpBlockContents set "TRK       : MCIdx"

    ntpBlockToTrk   set "p mu pi "
  
    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    trkExtraContents set HOTS:detailSVT

    show
}

# mu-
talkto BtuTupleMaker_mum {
  
    ntupleName set ntp2_Lambda0mum
    listToDump set myD_mum

    fillMC set true

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsInt       set "nTracks nGoodTrkLoose"
    eventTagsFloat     set "R2All"

    mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    ntpBlockConfigs set "D-         D             2   100"
    ntpBlockConfigs set "Lambda0    Lambda0       2   20"
    ntpBlockConfigs set "mu+        mu            0   30"
    ntpBlockConfigs set "p+         p             0   20"
    ntpBlockConfigs set "pi+        pi            0   30"

    ntpBlockContents set "D         : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(myD_mum) ShapeVars"
    ntpBlockContents set "Lambda0   : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 Flight FlightBS"
    ntpBlockContents set "pi        : Momentum CMMomentum MCIdx"
    ntpBlockContents set "p         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "mu        : Momentum CMMomentum MCIdx"
    ntpBlockContents set "TRK       : MCIdx"

    ntpBlockToTrk   set "p mu pi "
  
    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    trkExtraContents set HOTS:detailSVT

    show
}

#########################
# e+
talkto BtuTupleMaker_ep {
  
    ntupleName set ntp3_Lambda0ep
    listToDump set myD_ep

    fillMC set true

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsInt       set "nTracks nGoodTrkLoose"
    eventTagsFloat     set "R2All"

    mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    ntpBlockConfigs set "D+         D             2   100"
    ntpBlockConfigs set "Lambda0    Lambda0       2   20"
    ntpBlockConfigs set "e+         e             0   30"
    ntpBlockConfigs set "p+         p             0   20"
    ntpBlockConfigs set "pi+        pi            0   30"

    ntpBlockContents set "D         : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(myD_ep) ShapeVars"
    ntpBlockContents set "Lambda0   : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 Flight FlightBS"
    ntpBlockContents set "pi        : Momentum CMMomentum MCIdx"
    ntpBlockContents set "p         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "e         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "TRK       : MCIdx"

    ntpBlockToTrk   set "p e pi "

    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    trkExtraContents set HOTS:detailSVT

    show
}

#########################
# e-
talkto BtuTupleMaker_em {
  
    ntupleName set ntp4_Lambda0em
    listToDump set myD_em

    fillMC set true

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsInt       set "nTracks nGoodTrkLoose"
    eventTagsFloat     set "R2All"

    mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    ntpBlockConfigs set "D-         D             2   100"
    ntpBlockConfigs set "Lambda0    Lambda0       2   20"
    ntpBlockConfigs set "e+         e             0   30"
    ntpBlockConfigs set "p+         p             0   20"
    ntpBlockConfigs set "pi+        pi            0   30"

    ntpBlockContents set "D         : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(myD_em) ShapeVars"
    ntpBlockContents set "Lambda0   : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 Flight FlightBS"
    ntpBlockContents set "pi        : Momentum CMMomentum MCIdx"
    ntpBlockContents set "p         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "e         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "TRK       : MCIdx"

    ntpBlockToTrk   set "p e pi "

    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    trkExtraContents set HOTS:detailSVT

    show
}
#####################################################################
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
