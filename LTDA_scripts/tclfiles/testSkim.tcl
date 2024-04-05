ErrLoggingLevel trace

#create any configuration vars here
#name of the skim output file
FwkCfgVar OutputColl "test"

#This is the Framework
sourceFoundFile BetaMiniSequences/BetaMiniSequence.tcl
sourceFoundFile BetaMiniSequences/BetaMiniPhysicsSequence.tcl
#setup other modules, sequences here

path delete AllPath
path create MyPath BetaMiniSequence BetaMiniPhysicsSequence

sequence create MySeq

module clone TagFilterByName MyTagFilter
module talk MyTagFilter
  andList set BFlav_Final
  andList set B0ToDstarPi_KPi
  andList set B0ToDstarPi_FinalBFlav
  assertIfMissing set true
  show
exit
sequence append BetaMiniReadSequence -a KanEventUpdateTag MyTagFilter

source BasSmpComp.tcl
path append MyPath basSmpComp

sequence create basTaggingSequence
sourceFoundFile CompositionSequences/CompV0Sequence.tcl
sequence append basTaggingSequence CompV0Sequence
sourceFoundFile BTaggingSequences/BtsTaggingSequence.tcl
sequence append basTaggingSequence BtsTaggingSequence
talkto BtsTaggingDispatch {
	BRecList      set basB0toDstarPi_vtx
	Y4SList       set basB0toDstarPi_vtxY4S
	show   }
path append MyPath basTaggingSequence
path append MyPath MySeq

lappend CandBranches "Pion   pi+   pi-      p4"
lappend CandBranches "Kaon   K+    K-       p4"
lappend CandBranches "B0     B0    anti-B0  p4 vtx"

sourceFoundFile UsrTools/UsrDataProcs.tcl

set CandBlocks ""
set EventBlocks ""
#setup the event level UsrData
#appendUsrEventMaker MySeq Event "beamE"
#lappend EventBlocks Event

#set the candidate level UsrData
appendUsrCandMaker MySeq basB0toDstarPi_vtx basB0toDstarPi_vtx "DeltaZ DeltaZCov DeltaT DeltaTCov"
lappend CandBlocks basB0toDstarPi_vtx

#store the branches
foreach branch $CandBranches { lappend opt cndStoreOpt=$branch }
lappend opt trkFitType=All
#write the skim
writeSkim MyPath MySkim $OutputColl "deepCopyMicro" "basB0toDstarPi_vtx" $CandBlocks $EventBlocks "" $opt

action enable SumTimeAction
talkto EvtCounter { printFreq set 1000 }
path list
#loop over the events
ev begin -nev $NEvent
exit