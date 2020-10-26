#include "TTree.h"
#include "TChain.h"
#include "TFile.h"
#include "TString.h"
#include "TROOT.h"

//void select_some_events(string);

void copytree3_require_proton(TString filename) {

	printf("%s\n", filename);

	TFile* file = TFile::Open(filename);

	file->ls();

	TTree* originalTree = (TTree*)file->Get("ntp1"); 
	//originalTree->Print();
	Long64_t nentries = originalTree->GetEntries();

	int np = 0;
	int ne = 0;
	int nmu = 0;
	float pp3[64];
	float ep3[64];
	float mup3[64];
	originalTree->SetBranchAddress("np",&np);
	originalTree->SetBranchAddress("ne",&ne);
	originalTree->SetBranchAddress("nmu",&nmu);
	originalTree->SetBranchAddress("pp3",&pp3);
	originalTree->SetBranchAddress("ep3",&ep3);
	originalTree->SetBranchAddress("mup3",&mup3);


	TString outfilename = filename.ReplaceAll(".root","_SKIMMED.root");
	//TFile* output = TFile::Open("TESTskim.root","RECREATE");
	TFile* output = TFile::Open(outfilename,"RECREATE");
	printf("%s\n",outfilename);
	//TTree* selectedTree = originalTree->CopyTree("np>0 && ne>0 && nmu>0");
	TTree *newtree = originalTree->CloneTree(0);

	for (Long64_t i=0;i<nentries; i++) {
		originalTree->GetEntry(i);

		bool copyflag_prot = false;
		bool copyflag_e = false;
		bool copyflag_mu = false;

		if (np > 0 && np < 64) { 
			for (Int_t j=0;j<np;j++) {
				if (pp3[j] > 2.0)
					copyflag_prot = true;
			}
		}

		/*
		if (ne > 0 && ne < 64) { 
			for (Int_t j=0;j<ne;j++) {
				if (ep3[j] > 2.0)
					copyflag_e = true;
			}
		}

		if (nmu > 0 && nmu < 64) { 
			for (Int_t j=0;j<nmu;j++) {
				if (mup3[j] > 2.0)
					copyflag_mu = true;
			}
		}
		*/


		if (copyflag_prot)
			newtree->Fill();
		//event->Clear();
	}
	newtree->Print();
	newtree->AutoSave();
	delete file;
	delete output;

}

