#!/bin/bash

##Job settings                                                         
#PBS -q default
#PBS -o outFiles/"${jobName}".out                          
#PBS -e errFiles/"${jobName}".err                                       
#PBS -m a                                                
#PBS -M dsperka@cern.ch                            
             
##Job Configuration                                        
##Job Resources                                                     
#PBS -l walltime=0:20:00 
#PBS -l nodes=1:ppn=1                                                  
#PBS -l pmem=2gb 

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

cp /scratch/osg/dsperka/Run2/HZZ4l/CMSSW_7_4_12_patch2/src/UFHZZPlottingRun2/*.py ./
sed -i "s~PLOTTINGVARIABLE~${variable}~g" ZPlots.py
cat ZPlots.py
python ZPlots.py -l -q -b

ls -l ./*
cp *.pdf ${curDir}/${outDir}/

echo "Job ended at `date`"                              
