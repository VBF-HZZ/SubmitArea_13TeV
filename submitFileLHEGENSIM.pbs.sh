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
curl -s --insecure https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/HIG-RunIIWinter15wmLHE-00130 --retry 2 --create-dirs -o Configuration/GenProduction/python/fragment_LHE.py 

sed -i "s~/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/powheg/V2/ZZ_4L_NNPDF30_13TeV/v1/ZZ_4L_NNPDF30_13TeV_tarball.tar.gz~${gridpack}~g" Configuration/GenProduction/python/fragment_LHE.py
scram b

cmsDriver.py Configuration/GenProduction/python/fragment_LHE.py --fileout file:${tag}_LHE_${job}.root --mc --eventcontent LHE --datatier LHE --conditions MCRUN2_71_V1::All --step LHE --python_filename LHE_cfg.py -n ${eventsperjob} --no_exec

echo "process.RandomNumberGeneratorService.generator.initialSeed = 123456${job}" >> LHE_cfg.py
echo "process.RandomNumberGeneratorService.externalLHEProducer.initialSeed = 234${job}" >> LHE_cfg.py

cat LHE_cfg.py

echo "LHE Job running on `hostname` at `date`"

cmsRun LHE_cfg.py

cp ${gensimfragment} Configuration/GenProduction/python/fragment_GENSIM.py 
scram b

cmsDriver.py Configuration/GenProduction/python/fragment_GENSIM.py --filein "file:${tag}_LHE_${job}.root" --fileout file:${tag}_GENSIM_${job}.root --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --datatier GEN-SIM --conditions MCRUN2_71_V1::All --beamspot Realistic50ns13TeVCollision --step GEN,SIM --magField 38T_PostLS1 --python_filename GENSIM_cfg.py -n -1 

ls -l ./*

#cp ${tag}_LHE_${job}.root ${curDir}/${outDir}/
cp ${tag}_GENSIM_${job}.root ${curDir}/${outDir}/

echo "Job ended at `date`"                              
