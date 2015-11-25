#!/bin/bash

##Job settings                                                         
#PBS -q default
#PBS -o outFiles/"${jobName}".out                          
#PBS -e errFiles/"${jobName}".err                                       
#PBS -m a                                                
#PBS -M dsperka@cern.ch                            
             
##Job Configuration                                        
##Job Resources                                                     
#PBS -l walltime=5:59:00 
#PBS -l nodes=1:ppn=1                                                  
#PBS -l pmem=4gb 

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
cd ${CMSSWVER}/
#rm -rf lib/ src/ config/ python/
rm -rf ./*
cp -r -d ${curDir}/../${CMSSWVER}/* ./
cd src
rm ./*.DAT
rm ./*.dat
rm ./br.sm1
rm ./br.sm2
rm ./*.root
eval `scramv1 runtime -sh`
#eval `scramv1 setup mcfm >& tmp.out`
edmPluginRefresh -p ../lib/$SCRAM_ARCH

#fix mcfm issue
rm -rf Pdfdata
cp -r ${CMSSW_BASE}/src/ZZMatrixElement/MELA/data/Pdfdata ./
MCFM_LIBS_PATH=/scratch/osg/dsperka/Run2/HZZ4l/CMSSW_7_4_12_patch2/src/ZZMatrixElement/MELA/data/slc6_amd64_gcc491/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCFM_LIBS_PATH}
echo ${LD_LIBRARY_PATH}

export X509_USER_PROXY=/scratch/osg/dsperka/x509up_u130024

cp ${curDir}/${outDir}/cfg/${cfgFile} ./UFHZZAnalysisRun2/UFHZZ4LAna/python/  

echo "Job running on `hostname` at `date`"

##execute job

cmsRun ./UFHZZAnalysisRun2/UFHZZ4LAna/python/${cfgFile}

ls -l ./*
cp *.root ${curDir}/${outDir}/


echo "Job ended at `date`"                              
