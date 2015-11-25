###### 2leptons ########
#python SubmitAnalyzer.py -d "datasets_Run2015.txt" -c "/scratch/osg/dsperka/Run2/HZZ4l/CMSSW_7_4_12_patch2/src/UFHZZAnalysisRun2/UFHZZ4LAna/python/templateData_cfg.py" -f 2 --tag "Data"
#python SubmitAnalyzer.py -d "datasets_Spring15_25ns_MiniAODv2.txt" -c "/scratch/osg/dsperka/Run2/HZZ4l/CMSSW_7_4_12_patch2/src/UFHZZAnalysisRun2/UFHZZ4LAna/python/templateMC_cfg.py" -f 5 --tag "MC"
######## Z4l ###########
#python SubmitAnalyzer.py -d "datasets_Run2015.txt" -c "/scratch/osg/dsperka/Run2/HZZ4l/CMSSW_7_4_12_patch2/src/UFHZZAnalysisRun2/UFHZZ4LAna/python/templateData_Z4l_cfg.py" -f 2 --tag "Data_Z4l"
python SubmitAnalyzer.py -d "datasets_Spring15_25ns_MiniAODv2_Z4l.txt" -c "/scratch/osg/dsperka/Run2/HZZ4l/CMSSW_7_4_12_patch2/src/UFHZZAnalysisRun2/UFHZZ4LAna/python/templateMC_Z4l_cfg.py" -f 5 --tag "MC_Z4l"
