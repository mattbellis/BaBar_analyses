#include "TTree.h"
#include "TChain.h"
#include "TFile.h"
#include "TString.h"
#include "TROOT.h"

//void select_some_events(string);

void select_some_events(char *filename) {

	printf("%s\n", filename);

	TFile* file = TFile::Open(filename);

	file->ls();

	TTree* originalTree = (TTree*)file->Get("ntp1"); 
	originalTree->Print();

	TFile* output = TFile::Open("TESTskim.root","RECREATE");
	//TTree* selectedTree = originalTree->CopyTree("np>0 && ne>0 && nmu>0");
	TTree* selectedTree = originalTree->CopyTree("np>0 && (ne>0 || nmu>0)");

	selectedTree->Write();
	output->Close();


}

