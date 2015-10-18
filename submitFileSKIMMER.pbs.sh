#!/bin/bash

##Job settings                                                         
#PBS -q default
#PBS -o outFiles/"${jobName}".out                          
#PBS -e errFiles/"${jobName}".err                                       
#PBS -m a                                                
#PBS -M dsperka@cern.ch                            
             
##Job Configuration                                        
##Job Resources                                                     
#PBS -l walltime=8:00:00 
#PBS -l nodes=1:ppn=1                                                  
#PBS -l pmem=8gb 

##Create Work Area
CMSSWVER=CMSSW_7_4_12_patch2
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
pwd

cp ${skimtemplate} ./skimmer.py
sed -i "s~INPUTFILENAME~${inputfile}~g" skimmer.py
cat skimmer.py
python skimmer.py

ls -l ./*
cp *.root ${curDir}/${outDir}/

echo "Job ended at `date`"                              
