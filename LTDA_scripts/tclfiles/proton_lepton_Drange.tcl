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
seq create SmpMyD_mu
seq create SmpMyD_e

# muon
mod clone SmpMakerDefiner myD_mu
seq append SmpMyD_mu myD_mu
catch { setProduction myD_mu }

# electron
mod clone SmpMakerDefiner myD_e
seq append SmpMyD_e myD_e
catch { setProduction myD_e }

#####################################################################
# Set up the Smp stuff
talkto myD_mu {
    debug              set f
    verbose            set f
    decayMode          set "D0 -> p+ mu-"
    daughterListNames  set "pCombinedSuperLoose"
    daughterListNames  set "muCombinedVeryLooseFakeRate"

    fittingAlgorithm   set "TreeFitter"
    fitSettings        set "InvalidateFit"
    fitConstraints     set "Geo"
    # Tight cut for now
    preFitSelectors    set "Mass 1.7:2.0"
    preFitSelectors    set "CmsP 2.0:"

    createUsrData  set t
}

# electron
talkto myD_e {
    debug              set f
    verbose            set f
    decayMode          set "D0 -> p+ e-"
    daughterListNames  set "pCombinedSuperLoose"
    daughterListNames  set "eCombinedSuperLoose"

    fittingAlgorithm   set "TreeFitter"
    fitSettings        set "InvalidateFit"
    fitConstraints     set "Geo"
    # Tight cut for now
    preFitSelectors    set "Mass 1.7:2.0"
    preFitSelectors    set "CmsP 2.0:"

    createUsrData  set t
}

#####################################################################
## Add Analysis module
##
path append Everything SmpMyD_mu
path append Everything SmpMyD_e

mod  clone  BtuTupleMaker BtuTupleMaker_mu
path append Everything    BtuTupleMaker_mu

mod  clone  BtuTupleMaker BtuTupleMaker_e
path append Everything    BtuTupleMaker_e
#####################################################################

talkto BtuTupleMaker_mu {
  
    ntupleName set ntp1_protonmu
    listToDump set myD_mu

    fillMC set true

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsInt       set "nTracks nGoodTrkLoose"
    eventTagsFloat     set "R2All"

    mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    ntpBlockConfigs set "D0         D             2   100"
    ntpBlockConfigs set "mu-        mu            0   30"
    ntpBlockConfigs set "p+         p             0   20"

    ntpBlockContents set "D         : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(myD_mu) ShapeVars"
    ntpBlockContents set "p         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "mu        : Momentum CMMomentum MCIdx"
    ntpBlockContents set "TRK       : MCIdx"

    ntpBlockToTrk   set "p mu "

    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    trkExtraContents set HOTS:detailSVT

    show
}

#########################
talkto BtuTupleMaker_e {
  
    ntupleName set ntp1_LambdaCe
    listToDump set myD_e

    fillMC set true

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsInt       set "nTracks nGoodTrkLoose"
    eventTagsFloat     set "R2All"

    mcBlockContents    set "Mass CMMomentum Momentum Vertex"

    ntpBlockConfigs set "D0         D             2   100"
    ntpBlockConfigs set "e-         e             0   30"
    ntpBlockConfigs set "p+         p             0   20"

    ntpBlockContents set "D         : Mass Momentum CMMomentum MCIdx Vertex VtxChi2 UsrData(myD_e) ShapeVars"
    ntpBlockContents set "p         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "e         : Momentum CMMomentum MCIdx"
    ntpBlockContents set "TRK       : MCIdx"

    ntpBlockToTrk   set "p e "

    trkExtraContents set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    trkExtraContents set HOTS:detailSVT

    show
}
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
