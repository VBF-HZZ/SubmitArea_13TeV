#!/bin/bash

##Job settings                                                         
#PBS -q default
#PBS -o outFiles/"${jobName}".out                          
#PBS -e errFiles/"${jobName}".err                                       
#PBS -m a                                                
#PBS -M dsperka@cern.ch                            
             
##Job Configuration                                        
##Job Resources                                                     
#PBS -l walltime=24:00:00 
#PBS -l nodes=1:ppn=1                                                  
#PBS -l pmem=8gb 

##Create Work Area
CMSSWVER=CMSSW_7_4_1_patch2
export SCRAM_ARCH=slc6_amd64_gcc491
export OSG_APP=/osg/app                                         
export VO_CMS_SW_DIR=${OSG_APP}/cmssoft/cms                               
export CMS_PATH=${VO_CMS_SW_DIR}

. ${CMS_PATH}/cmsset_default.sh
cd $TMPDIR
scram list CMSSW
eval `scramv1 project CMSSW ${CMSSWVER}`
cd ${CMSSWVER}/src
eval `scramv1 runtime -sh`

#export X509_USER_PROXY=$HOME/private/personal/voms_proxy.cert
export X509_USER_PROXY=/scratch/osg/dsperka/x509up_u130024

cmsDriver.py step1 --filein file:${inputfile} --fileout file:${tag}_GENSIMRAW_${job}.root --pileup_input "dbs:/MinBias_TuneCUETP8M1_13TeV-pythia8/RunIIWinter15GS-MCRUN2_71_V1-v1/GEN-SIM" --mc --eventcontent RAWSIM --pileup 2015_25ns_Startup_PoissonOOTPU --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --datatier GEN-SIM-RAW --conditions MCRUN2_74_V9 --step DIGI,L1,DIGI2RAW,HLT:@frozen25ns --magField 38T_PostLS1  --python_filename GENSIMRAW_cfg.py -n -1 --no_exec

sed -i 's~/store/mc~file:/cms/data/store/mc~g' GENSIMRAW_cfg.py
cat GENSIMRAW_cfg.py
cmsRun GENSIMRAW_cfg.py

cmsDriver.py step2 --filein file:${tag}_GENSIMRAW_${job}.root --fileout file:${tag}_AOD_${job}.root --mc --eventcontent AODSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --datatier AODSIM --conditions MCRUN2_74_V9 --step RAW2DIGI,L1Reco,RECO,EI --magField 38T_PostLS1 --python_filename AOD_cfg.py -n -1

cmsDriver.py step3 --filein file:${tag}_AOD_${job}.root --fileout file:${tag}_MINIAOD_${job}.root --mc --eventcontent MINIAODSIM --runUnscheduled --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --datatier MINIAODSIM --conditions MCRUN2_74_V9 --step PAT --python_filename MINIAD_cfg.py -n -1

ls -l ./*

#cp ${tag}_GENSIMRAW_${job}.root ${curDir}/${outDir}/
cp ${tag}_AOD_${job}.root ${curDir}/${outDir}/
cp ${tag}_MINIAOD_${job}.root ${curDir}/${outDir}/

echo "Job ended at `date`"                              
