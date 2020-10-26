//##########################################################################
// Define subroutines that are loaded during ROOT initialization.
//
// File: $Id: RooAlias.C,v 1.16 2006/03/15 18:20:59 steinke Exp $
// Authors:
//   DK, David Kirkby, Stanford University, kirkby@hep.stanford.edu
//   AT, Alexandre (Sasha) Telnov, UC Berkeley/LBNL, avtelnov@lbl.gov
// History:
//   10-Dec-1999 DK  Created initial version
//   19-Apr-2000 DK  Add the BABARLabel function
//   05-Dec-2000 AT  Added BABARSmartLabel() that produces pretty output 
//     independent of the ratio of pad's width and height. Kept BABARLabel()
//     to avoid breaking existing macros that use it. 
//   07-Dec-2000 AT  Added help and second line of text options to 
//     BABARSmartLabel().
//   19-Feb-2001 AT  Made BABARSmartLabel() work with older versions of
//     ROOT; added left-edge justification; added more online help.
//##########################################################################

// Load the shared library for an SRT package into a ROOT session.
// The usage is:
//
//   loadSrtLib("<package>")  // for a ROOT library
//      or
//   loadLib("<package>")  // for a "regular" Shared library
//
// The library for <package> is assumed to have the name:
//
//   lib<package>_root.so  // for a ROOT library
//      or
//   lib<package>_$(BFCURRENT).so  // for a "regular" Shared library
//
// The library will be loaded without an explicit path and so
// must exist somewhere in the search path (which includes the
// current test and production release directories when using
// .rootrc from workdir).

void loadSrtLib(const char* packageName) {
  char buffer[512];
  //  const char *current= gSystem->Getenv("BFCURRENT");
  sprintf(buffer, "lib%s_root.so", packageName);
  gSystem->Load(buffer);
}

void loadLib(const char* packageName) {
  char buffer[512];
  const char *current= gSystem->Getenv("BFCURRENT");
  sprintf(buffer, "lib%s_%s.so", packageName, current);
  gSystem->Load(buffer);
}

// (DK) Generate the label "BABAR" for approved plots. The optional parameters specify
// the lower-left corner of the label in normalized coordinates (0,1)x(0,1) and a
// scale factor to apply to the label size. The defaults put the label in the
// recommended location (top-right corner) with the recommended size.

void BABARLabel(Double_t xpos= 0.73, Double_t ypos= 0.85, Double_t scale= 1.0) {
  TText *babar = new TText();
  babar->SetNDC(kTRUE);
  babar->SetTextFont(32);
  babar->SetTextSize(0.10*scale);
  babar->DrawText(xpos,ypos,"B");
  babar->SetTextSize(0.075*scale);
  babar->DrawText(xpos+0.042*scale,ypos,"A");
  babar->SetTextSize(0.10*scale);
  babar->DrawText(xpos+0.078*scale,ypos,"B");
  babar->SetTextSize(0.075*scale);
  babar->DrawText(xpos+0.120*scale,ypos,"AR");
  delete babar;
}
// (AT) Since ROOT sets font size as a fraction of the smaller side of the pad, 
// BABARSmartLabel() treats the cases of "vertical" and "horizontal" pads separately.
// In addition, the label nicely positions itself in the upper-right corner of your plot.
// The function takes three optional parameters: the x and the y coordinates of the
// label's TOP-RIGHT corner and the label's relative size.
//    Note, however, that the "BaBar" label will still get screwed up if you manually resize
// the pad after drawing the label.
//    Also note that what you see on the screen may not look perfect: I tried optimizing the 
// way the label looks on paper. It goes without saying that your ROOT session should have 
// TrueType font support turned on.  

void BABARSmartLabel(Double_t xpos=0.9, Double_t ypos=0.9, Double_t scale=1.0, TString str="null", Double_t scale2=0.5, TString align="R") {
  // Making -1 a placeholder for function's default value 
  if (xpos == -1) xpos = 0.9;
  if (ypos == -1) ypos = 0.9;
  if (scale == -1) scale = 1; 
  if (str == "-1") str = "null"; 
  if (scale2 == -1) scale2 = 0.5; 
  if (align == "-1") align = "R"; 
  // -2 as the first parameter triggers printing comamnd options
  if (xpos == -2) {
   cout 
      << "\n  USAGE: BABARSmartLabel(xpos,ypos,scale,\"str\",scale2,\"align\");\n"
      << "  Prints the official BaBar label on the active ROOT pad\n"
      << "      xpos    X position of the \"BaBar\" label\'s top right corner, 0 < xpos < 1, defaults to 0.9\n" 
      << "      ypos    Y position of the \"BaBar\" label\'s top right corner, 0 < ypos < 1, defaults to 0.9\n"
      << "      scale   relative size of the label, defaults to 1\n" 
      << "      str     LaTeX-style text that goes under the BaBar label. Use # instead of \\\n"
      << "      scale2  relative size of the second line of text, defaults to 0.5\n"
      << "      align   R or L: str is aligned to the right (default) or left edge of the \"BaBar\" label\n"
      << "    By default, the second line of text is printed in Helvetica (a sans-serif font).\n"
      << "  You can use the #font[] command to change the font. Refer to ROOT documentation for\n"
      << "  more information on use of text in ROOT.\n"; 
   cout
      << "    \"Magic\" options: \n"
      << "      xpos = -2 displays BABARSmartLabel() help\n"
      << "      -1 can be used as a place holder to use the default value of any of the parameters\n"
      << "      There are a few predefined values of str that start with a ~ (tilde):\n"
      << "        \"~1\"       =          \"preliminary\"      \n"
      << "        \"~2\"       =          \"very preliminary\" \n"
      << "        \"~2000\"    =          \"year 2000 preliminary\" \n"
      << "        \"~2001\"    =          \"year 2001 preliminary\" \n"
      << "        \"~25\"      =          \"25 fb^{-1}\" \n"     
      << "        \"~B->fcp\"  =           a big formula you should have seen before\n"     
      << "    Examples: \n"
      << "      BABARSmartLabel(); \n"
      << "      BABARSmartLabel(-1,-1,-1,\"preliminary\"); \n"
      << "      BABARSmartLabel(0.9,0.8,1.2,\"~25\"); \n"
      << "      BABARSmartLabel(0.9,0.7,1.2,\"25 fb^{-1} preliminary\",0.6); \n"
      << "      BABARSmartLabel(0.9,0.5,-1,\"~B->fcp\",0.25); \n\n";
    return();
  }
  // A few predefined labels to go to the second line of text
  if (str == "~1") str = "preliminary"; 
  if (str == "~2") str = "very preliminary"; 
  if (str == "~2000") str = "year 2000 preliminary"; 
  if (str == "~2001") str = "year 2000 preliminary"; 
  if (str == "~25") str = "25 fb^{-1}";
  if (str == "~B->fcp") str = "#font[12]{#Gamma#font[132]{(}B^{#font[12]{0}}_{#font[132]{phys}}#font[132]{(}t#font[132]{)} #rightarrow f_{CP}#font[132]{)} = #left|A_{f_{CP}}#right|^{#font[132]{2}} e^{-#Gamma t} #left[#frac{1+|#lambda_{f_{CP}}|^{#font[132]{2}}}{#font[132]{2}} + #frac{#font[132]{1}-|#lambda_{f_{CP}}|^{#font[132]{2}}}{#font[132]{2}} #font[132]{cos}#font[132]{(}#DeltaMt#font[132]{)} - #font[132]{Im }#lambda_{f_{CP}}#font[132]{sin}#font[132]{(}#DeltaMt#font[132]{)}#right]}";

  // Draw the label 
  TLatex *babar = new TLatex();
  Double_t cheburashkaFactorX=1, cheburashkaFactorY=1, padSizeX=500, padSizeY=500, xpos2, ypos2, xposL;
  babar->SetNDC(kTRUE);
  babar->SetTextFont(32); // Bold-Italic Times
  babar->SetTextAlign(31); // Right-Bottom
  padSizeX = gPad->GetWw()*gPad->GetWNDC(); // Get pad's dimensions
  padSizeY = gPad->GetWh()*gPad->GetHNDC();
  if (padSizeX>padSizeY) cheburashkaFactorX=padSizeY/padSizeX;
  if (padSizeX<padSizeY) cheburashkaFactorY=padSizeX/padSizeY;
//xpos2=xpos-0.185*scale*cheburashkaFactorX;
  xpos2=xpos-0.188*scale*cheburashkaFactorX;
  ypos2=ypos-0.0620*scale*cheburashkaFactorY;
  xposL=xpos-0.253*scale*cheburashkaFactorX;
  babar->SetTextSize(0.10*scale); // Beginning to draw "BaBar"
  babar->DrawText(xpos2,ypos2,"B");
  babar->SetTextSize(0.075*scale);
  babar->DrawText(xpos2+0.039*scale*cheburashkaFactorX,ypos2,"A");
  babar->SetTextSize(0.10*scale);
  babar->DrawText(xpos2+0.1015*scale*cheburashkaFactorX,ypos2,"B");
  babar->SetTextSize(0.075*scale);
  babar->DrawText(xpos2+0.1875*scale*cheburashkaFactorX,ypos2,"AR");
  if (str == "null") return();    // Beginning to draw the second line of text
  babar->SetTextFont(42); // Helvetica (medium, upright) 
  babar->SetTextSize(0.1*scale2);
  if (align == "L") then {
    babar->SetTextAlign(13); // Left-Top
    babar->DrawLatex(xposL,ypos2-0.02*scale2*cheburashkaFactorY,str);
  }
  else {
    babar->SetTextAlign(33); // Right-Top
    babar->DrawLatex(xpos,ypos2-0.02*scale2*cheburashkaFactorY,str);
  }
  delete babar;
}


