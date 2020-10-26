//##########################################################################
// Initialization code executed at the start of a ROOT session.
//
// File: $Id: RooLogon.C,v 1.16 2006/03/10 04:02:21 bechtle Exp $
// Authors:
//   DK, David Kirkby, Stanford University, kirkby@hep.stanford.edu
//   AT, Alexandre (Sasha) Telnov, UC Berkeley/LBNL, avtelnov@lbl.gov
// History:
//   10-Dec-1999 DK Created initial version
//   19-Apr-2000 DK Add BABAR style for approved plots
//   05-Dec-2000 AT Added mention of a BABARSmartLabel()
//   06-Apr-2004 C Heart, C Cheng minor changes for Root3 tutorial
//##########################################################################

{
  // use the 'plain' style for plots (white backgrounds, etc)
  cout << "...using style 'Plain'\n";
  gROOT->SetStyle("Plain");

  // check that we are running from a release working directory
  void* release= gSystem->OpenDirectory("RELEASE");
  if(0 == release) {
    printf("*** Cannot find RELEASE directory. Are you in a workdir?\n");
  }
  else {
    printf("...found RELEASE directory\n");
    gSystem->FreeDirectory(release);
  }
  void* parent= gSystem->OpenDirectory("PARENT");
  if(0 == parent) {
    printf("*** Cannot find PARENT directory. Are you in a workdir?\n");
  }
  else {
    printf("...found PARENT directory\n");
    gSystem->FreeDirectory(parent);
  }
  const char* current= gSystem->Getenv("BFCURRENT");
  if(0 == current) {
    printf("*** The BFCURRENT environment variable is not set!\n");
    printf("*** Will not be able to find shared libraries from a release");
  }
  else {
    printf("...running in release %s\n", current);
  }
  
  //-----------------------------------------------------------------
  // load shared libraries from the current release
  // (see comments for loadSrtLib in RooAlias.C)
  // ** instruction for RooFit v.191 with ROOT4 **
  //
  // ROOLOGON RECIPE FOR LIBRARIES BUILT WITH 
  // gmake RooFitXXX.root
  // 
  //  gSystem->Load("libMinuit") ;  // REQUIRED FOR ROOT4
  //  loadSrtLib("RooFitCore") ;
  //  loadSrtLib("RooFitModels") ;
  //  using namespace RooFit ;

  // ROOLOGON RECIPE FOR LIBRARIES BUILT WITH 
  // gmake RooFitXXX.rootlib ROPT=-Shared
  // 
  //  gSystem->Load("libMinuit") ;  // REQUIRED FOR ROOT4
  //  gSystem->Load("libRooFitCore") ;
  //  gSystem->Load("libRooFitModels") ;
  //  using namespace RooFit ;
  //-----------------------------------------------------------

  // Create the 'BABAR' style for approved plots. Note that this style may need
  // some fine tuning in your macro depending on what you are plotting, e.g.
  //
  //  gStyle->SetMarkerSize(0.75);  // use smaller markers in a histogram with many bins
  //  gStyle->SetTitleOffset(0.65,"y");  // bring y axis label closer to narrow values

  TStyle *babarStyle= new TStyle("BABAR","BaBar approved plots style");

  // use plain black on white colors
  babarStyle->SetFrameBorderMode(0);
  babarStyle->SetCanvasBorderMode(0);
  babarStyle->SetPadBorderMode(0);
  babarStyle->SetPadColor(0);
  babarStyle->SetCanvasColor(0);
  //babarStyle->SetTitleColor(0);
  babarStyle->SetStatColor(0);
  babarStyle->SetTitleFillColor(0);

  // set the paper & margin sizes
  babarStyle->SetPaperSize(20,26);
  babarStyle->SetPadTopMargin(0.05);
  babarStyle->SetPadRightMargin(0.05);
  babarStyle->SetPadBottomMargin(0.16);
  babarStyle->SetPadLeftMargin(0.12);

  // use large Times-Roman fonts
  babarStyle->SetTitleFont(132,"xyz");  // set the all 3 axes title font
  babarStyle->SetTitleFont(132," ");    // set the pad title font
  babarStyle->SetTitleSize(0.06,"xyz"); // set the 3 axes title size
  babarStyle->SetTitleSize(0.06," ");   // set the pad title size
  babarStyle->SetLabelFont(132,"xyz");
  babarStyle->SetLabelSize(0.05,"xyz");
  babarStyle->SetTextFont(132);
  babarStyle->SetTextSize(0.08);
  babarStyle->SetStatFont(132);

  // use bold lines and markers
  babarStyle->SetMarkerStyle(8);
  babarStyle->SetHistLineWidth(1.85);
  babarStyle->SetLineStyleString(2,"[12 12]"); // postscript dashes

  //..Get rid of X error bars
  babarStyle->SetErrorX(0.001);

  // do not display any of the standard histogram decorations
  babarStyle->SetOptTitle(0);
  babarStyle->SetOptStat(0);
  babarStyle->SetOptFit(0);

  // put tick marks on top and RHS of plots
  babarStyle->SetPadTickX(1);
  babarStyle->SetPadTickY(1);

  cout << "\n    For approved plots use: gROOT->SetStyle(\"BABAR\");\n";
  cout << "    To add a BABAR label use: BABARLabel();\n";
  cout << "    To add a better-scaling BABAR label use: BABARSmartLabel();\n";
  cout << "    Type \"BABARSmartLabel(-2);\" for options\n\n";

  // restore the plain style. Add tick marks and extra stats
  gROOT->SetStyle("Plain");
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);
  gStyle->SetOptStat(1111111);
}
