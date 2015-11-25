#include <iostream>
#include <set>

void removeDuplicates() {

    //TString filename = "rootfiles_Data_20150729/Data_Run2015B-PromptReco-v1.root";
    //TString filename = "rootfiles_Data_20151006/Data_Run2015D-PromptReco-v3.root";
    //TString filename = "rootfiles_Data_20151006/Data_Run2015C-23Sep2015-v1.root";
    //TString filename = "rootfiles_Data_Z4l_20151018/Data_2015_mZ24.root";
    //TString filename = "rootfiles_Data_Z4l_20151030/SingleLepton_Run2015.root";
    //TString filename = "rootfiles_Data_Z4l_20151111/SingleLepton_Run2015.root";
    TString filename = "rootfiles_Data_20151114/Data_2015.root";

    std::cout<<filename<<std::endl;

    TFile *oldfile = new TFile(filename);
    //TTree *oldtree = (TTree*)oldfile->Get("Ana/passedEvents");
    TTree *oldtree = (TTree*)oldfile->Get("passedEvents");

    Long64_t nentries = oldtree->GetEntries();
    std::cout<<nentries<<" total entries."<<std::endl;
    ULong64_t Run, LumiSect, Event;
    bool passedZ4lSelection;
    oldtree->SetBranchAddress("Run",&Run);
    oldtree->SetBranchAddress("LumiSect",&LumiSect);
    oldtree->SetBranchAddress("Event",&Event);
    oldtree->SetBranchAddress("passedZ4lSelection",&passedZ4lSelection);

    //Create a new file + a clone of old tree in new file
    //TFile *newfile = new TFile("Data_NoDuplicates.root","recreate");
    TFile *newfile = new TFile("Data_passedZ4l.root","recreate");
    TTree *newtree = oldtree->CloneTree(0);

    std::set<TString> runlumieventSet;
    int nremoved = 0;
    for (Long64_t i=0;i<nentries; i++) {
        if (i%10000==0) std::cout<<i<<"/"<<nentries<<std::endl;
        oldtree->GetEntry(i);

        /*
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
        */
        if (passedZ4lSelection) newtree->Fill();
    }

    std::cout<<nremoved<<" duplicates."<<std::endl;
    newtree->Print();
    newtree->AutoSave();
    //delete oldfile;
    delete newfile;
}

