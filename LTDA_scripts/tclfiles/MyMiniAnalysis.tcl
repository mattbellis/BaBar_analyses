#------------------------------------------------------------------------------
# MyMiniAnalysis.tcl
# Modified to include the Workbook's QExample module
# and to run the job interactively.
# The workbook can be found on the web at:
#   http://www.slac.stanford.edu/BFROOT/www/doc/workbook/workbook.html
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

##
## Set the number of events to run. If this isn't set, all events in the
## input collections will be processed.
##
FwkCfgVar NEvent

## choose the flavor of ntuple to write (hbook or root) and the file name
##
FwkCfgVar BetaMiniTuple "root"
FwkCfgVar histFileName "MyMiniAnalysis.root"

##
##  You can enter input collections two ways: either append them to a list, or
##  explicitly enter them in the input module. Do one or the other, BUT NOT 
##  BOTH.
##  If inputList is set before executing btaMini.tcl, that will automatically
##  add the collections to the appropriate input module, otherwise make sure you
##  talk to the right one.
##
## lappend inputList collection1 collection2 ...
##
##  OR THE FOLLOWING (choose the correct one based on persistence)
##
## talkto BdbEventInput {
## talkto KanEventInput {
##    input add collection1
##    input add collection2
##    ...
## }

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
sourceFoundFile BetaMiniUser/btaMini.tcl
#sourceFoundFile BetaMiniUser/btaMiniPhysics.tcl
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

## Add Analysis module
##
path append Everything MyMiniAnalysis
path append Everything QExample

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

path list
