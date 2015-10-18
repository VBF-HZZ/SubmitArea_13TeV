#!/bin/bash

##Job settings                                                         
#PBS -q default
#PBS -o outFiles/"${jobName}".out                          
#PBS -e errFiles/"${jobName}".err                                       
#PBS -m a                                                
#PBS -M dsperka@cern.ch                            
             
##Job Configuration                                        
##Job Resources                                                     
#PBS -l walltime=01:00:00 
#PBS -l nodes=1:ppn=1                                                  
#PBS -l pmem=8gb 

##Create Work Area
CMSSWVER=CMSSW_7_1_18
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

export X509_USER_PROXY=$HOME/private/personal/voms_proxy.cert

# this is a dummy fragment
curl -s --insecure https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/HIG-RunIIWinter15wmLHE-00130 --retry 2 --create-dirs -o Configuration/GenProduction/python/fragment.py 

sed -i "s~/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/powheg/V2/ZZ_4L_NNPDF30_13TeV/v1/ZZ_4L_NNPDF30_13TeV_tarball.tar.gz~${gridpack}~g" Configuration/GenProduction/python/fragment.py
#sed -i 's~uint32(5000)~uint32(${eventsperjob})~g' Configuration/GenProduction/python/fragment.py
#sed -i 's~cmsgrid_final~cmsgrid_final_${job}~g' Configuration/GenProduction/python/fragment.py
scram b
cmsDriver.py Configuration/GenProduction/python/fragment.py --fileout file:LHE_${job}.root --mc --eventcontent LHE --datatier LHE --conditions MCRUN2_71_V1::All --step LHE --python_filename LHE_cfg.py -n ${eventsperjob} --no_exec

echo "process.RandomNumberGeneratorService.generator.initialSeed = 123456${job}" >> LHE_cfg.py
echo "process.RandomNumberGeneratorService.externalLHEProducer.initialSeed = 234${job}" >> LHE_cfg.py

cat LHE_cfg.py

echo "Job running on `hostname` at `date`"

cmsRun LHE_cfg.py

ls -l ./*
cp LHE_${job}.root ${curDir}/${outDir}/

echo "Job ended at `date`"                              
