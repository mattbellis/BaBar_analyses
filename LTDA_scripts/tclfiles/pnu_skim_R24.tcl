#..pnu_skim_R24.tcl
#  B -> p nu (BNV) first-pass skim + flat ntuple.
#  Derived from basicPID_pi0_R24.tcl. Changes:
#    * proton CM-momentum window applied in a SmpSubLister (pHighCmsP)
#    * pHighCmsP is the listToDump and writeEveryEvent is false, so only events
#      with >=1 proton in the window are written
#    * every charged track (ChargedTracks) goes in the TRK block with the PID
#      selector bitmaps, so the "tag" side and the e/mu counts can be built from
#      TRK and do not depend on which PID lists a track landed in
#    * optional BGFMultiHadron tag-bit filter (off by default)
#
#  Kinematics: p* = (mB^2 - mp^2)/(2 mB) = 2.556 GeV in the B frame.
#  With p_B ~ 0.325 GeV in the Y(4S) frame, the proton CM momentum lies in
#  about 2.39 - 2.73 GeV before resolution. The 2.0 - 3.2 GeV window leaves
#  sidebands on both sides.

#..General setup needed in all jobs
sourceFoundFile ErrLogger/ErrLog.tcl
sourceFoundFile FrameScripts/FwkCfgVar.tcl
sourceFoundFile FrameScripts/talkto.tcl

#-------------- FwkCfgVars needed to control this job ---------------------
set ProdTclOnly true

FwkCfgVar BetaMiniReadPersistence Kan
FwkCfgVar levelOfDetail "cache"

#..allowed values of ConfigPatch are "Run2" or "MC". MUST match the input.
FwkCfgVar ConfigPatch "Run2"
#FwkCfgVar ConfigPatch "MC"

FwkCfgVar FilterOnTag   "true"
FwkCfgVar PrintFreq 1000

FwkCfgVar BetaMiniTuple "root"
FwkCfgVar histFileName "pnu_skim.root"

FwkCfgVar NEvents 0

#..Proton CM-momentum window (GeV). Loose enough to keep sidebands.
FwkCfgVar pCmsPMin 2.0
FwkCfgVar pCmsPMax 3.2

#..Set to true to also require the BGFMultiHadron tag bit. Measure its
#  signal-MC efficiency per lepton class before turning it on.
FwkCfgVar UseBGFMultiHadron false

#--------------------------------------------------------------------------
ErrLoggingLevel warning

sourceFoundFile BetaMiniUser/btaMiniPhysics.tcl

#..Optional tag-bit prefilter (same pattern as testSkim.tcl). It runs before
#  any composition, so it saves CPU as well as disk.
if { $UseBGFMultiHadron } {
    mod clone TagFilterByName BGFFilter
    talkto BGFFilter {
        andList         set BGFMultiHadron
        assertIfMissing set true
    }
    sequence append BetaMiniReadSequence -a KanEventUpdateTag BGFFilter
}

#--------------------------------------------------------------------------
#..Signal-proton candidates: PID'd protons within the CM momentum window.
#  A SubLister copies pointers and does no fitting, so this is cheap.
mod clone SmpSubListerDefiner pHighCmsP
talkto pHighCmsP {
    unrefinedListName set pCombinedSuperLoose
    selectors         set "CmsP $pCmsPMin:$pCmsPMax"
}
path append Everything pHighCmsP
path append Everything BtuTupleMaker

#--------------------------------------------------------------------------
talkto BtuTupleMaker {

    eventBlockContents set "EventID CMp4 BeamSpot"
    eventTagsFloat     set "R2 R2All xPrimaryVtx yPrimaryVtx zPrimaryVtx probPrimaryVtx thrustMag thrustMagAll thrustCosTh thrustCosThAll thrustPhi thrustPhiAll sphericityAll"
    eventTagsInt       set "nTracks nGoodTrkLoose nChargedTracks"
    eventTagsBool      set "BGFMultiHadron"

    fillMC             set true

    #..Only events with >=1 candidate on this list are written.
    listToDump         set pHighCmsP
    writeEveryEvent    set f

    #..Signal proton candidate(s)
    ntpBlockConfigs  set "p+     p       0   20"
    ntpBlockContents set "p :  MCIdx Momentum CMMomentum Doca DocaXY"

    #..Every charged track, with PID bitmaps: use these for the tag side
    #  and for counting e/mu.
    ntpBlockContents   set "TRK  : MCIdx Momentum CMMomentum"
    fillAllCandsInList set "TRK ChargedTracks"
    ntpBlockToTrk      set "p"
    trkExtraContents   set "BitMap:pSelectorsMap,KSelectorsMap,piSelectorsMap,muSelectorsMap,eSelectorsMap,TracksMap"
    wantATrkBlock      set true

    #..Optional per-species blocks. Everything in them is also in TRK, so
    #  leave them off unless you want the extra PID-list candidates.
    #ntpBlockConfigs    set "mu-    mu      0   100"
    #ntpBlockContents   set "mu : MCIdx CMMomentum"
    #fillAllCandsInList set "mu muCombinedVeryLooseFakeRate"
    #ntpBlockConfigs    set "e-     e       0   100"
    #ntpBlockContents   set "e :  MCIdx CMMomentum"
    #fillAllCandsInList set "e eCombinedSuperLoose"

    #..Neutrals
    ntpBlockConfigs    set "gamma      gamma         0   256"
    ntpBlockContents   set "gamma     : MCIdx CMMomentum"
    gamExtraContents   set EMC
    fillAllCandsInList set "gamma CalorNeutral"

    ntpBlockConfigs    set "pi0   pi0    2 256"
    ntpBlockContents   set "pi0  : Mass VtxChi2 MCIdx CMMomentum"
    ntpAuxListContents set "pi0 : pi0LooseMass : _unc_ : Mass CMMomentum"
    fillAllCandsInList set "pi0   pi0Loose"

    show
}

#-----------------------------------------------------------------------
#..Keep the job log: with writeEveryEvent false, the EvtCounter total is
#  the only record of how many events were processed (needed for
#  normalization and skim-efficiency bookkeeping).
mod talk EvtCounter
  printFreq set $PrintFreq
exit

path list

if { $NEvents>=0 } {
    ev beg -nev $NEvents
    exit
}
