#include <iostream>
#include <set>

void removeDuplicates() {

    //TString filename = "rootfiles_Data_20150729/Data_Run2015B-PromptReco-v1.root";
    //TString filename = "rootfiles_Data_20151006/Data_Run2015D-PromptReco-v3.root";
    //TString filename = "rootfiles_Data_20151006/Data_Run2015C-23Sep2015-v1.root";
    TString filename = "rootfiles_Data_20151014/Data_Run2015D_new.root";

    std::cout<<filename<<std::endl;

    TFile *oldfile = new TFile(filename);
    TTree *oldtree = (TTree*)oldfile->Get("Ana/passedEvents");

    Long64_t nentries = oldtree->GetEntries();
    std::cout<<nentries<<" total entries."<<std::endl;
    ULong64_t Run, LumiSect, Event;
    oldtree->SetBranchAddress("Run",&Run);
    oldtree->SetBranchAddress("LumiSect",&LumiSect);
    oldtree->SetBranchAddress("Event",&Event);

    //Create a new file + a clone of old tree in new file
    TFile *newfile = new TFile("Data_NoDuplicates.root","recreate");
    TTree *newtree = oldtree->CloneTree(0);

    std::set<TString> runlumieventSet;
    int nremoved = 0;
    for (Long64_t i=0;i<nentries; i++) {
        if (i%1000==0) std::cout<<i<<"/"<<nentries<<std::endl;
        oldtree->GetEntry(i);

        TString s_Run  = std::to_string(Run);
        TString s_Lumi = std::to_string(LumiSect);
        TString s_Event = std::to_string(Event);
        TString runlumievent = s_Run+":"+s_Lumi+":"+s_Event;

        if (runlumieventSet.find(runlumievent)==runlumieventSet.end()) {
            runlumieventSet.insert(runlumievent);
            newtree->Fill();
        } else {
            nremoved++;
        }
        
    }

    std::cout<<nremoved<<" duplicates."<<std::endl;
    newtree->Print();
    newtree->AutoSave();
    //delete oldfile;
    delete newfile;
}

