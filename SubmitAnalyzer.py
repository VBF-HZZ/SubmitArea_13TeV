#!/usr/bin/python
#-----------------------------------------------
# Latest update: 2014.09.14
#-----------------------------------------------
import sys, os, pwd, commands
import optparse, shlex, re
import time
from time import gmtime, strftime
import math

#define function for parsing options
def parseOptions():
    global observalbesTags, modelTags, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # input options
    parser.add_option('-t', '--tag', dest='TAG', type='string',default='', help='tag to be appended to the results, default is an empty string')
    parser.add_option('-d', '--datasets', dest='DATASETS', type='string', default='datasets_Spring15_50ns.txt', help='txt file with datasets to run over')
    parser.add_option('-c', '--cfg', dest='CONFIGFILE', type='string', default='/scratch/osg/dsperka/Run2/HZZ4l/CMSSW_7_4_5/src/UFHZZAnalysisRun2/UFHZZ4LAna/python/templateMC_cfg.py', help='configuration template')
    parser.add_option('-f', '--filesperjob', dest='FILESPERJOB', type=int, default=5, help='configuration template')
    parser.add_option('-r', '--resubmit', dest='RESUBMIT', action='store_true', help='resubmit only jobs in resubmit.txt')

    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

# define function for processing the external os commands
def processCmd(cmd, quite = 0):
    #    print cmd
    status, output = commands.getstatusoutput(cmd)
    if (status !=0 and not quite):
        print 'Error in processing command:\n   ['+cmd+']'
        print 'Output:\n   ['+output+'] \n'
    return output

def submitAnalyzer():

    # parse the arguments and options
    global opt, args
    parseOptions()

    filesperjob = int(opt.FILESPERJOB)
    cfgtemplate = opt.CONFIGFILE

    # save working dir
    currentDir = os.getcwd()

    tag = opt.TAG+'_'+time.strftime("%Y%m%d")
    outDir='resultsAna_'+tag 

    if (not os.path.isdir(outDir)):
        cmd = 'mkdir '+outDir
        processCmd(cmd)
        cmd = 'mkdir '+outDir+'/cfg/'
        processCmd(cmd)
    #else:
    #    if (not opt.RESUBMIT):
    #        print 'Directory '+outDir+' already exists. Exiting...'
    #        sys.exit()

    outFilesDir = 'outFilesAna_'+tag
    if not os.path.isdir(outFilesDir):
        cmd = 'mkdir '+outFilesDir
        processCmd(cmd)

    errFilesDir = 'errFilesAna_'+tag
    if not os.path.isdir(errFilesDir):
        cmd = 'mkdir '+errFilesDir
        processCmd(cmd)

    # get the datasets
    print '[Gathering Dataset Information]'
    datasets = []
    cross_section = {}
    nfiles = {}
    nevents = {}
    datasetfiles = {}

    with open(opt.DATASETS, "r") as datasetfile:
        for line in datasetfile:

            if (line.startswith('#')): continue

            #if (not 'WZTo2L2Q' in line): continue
            #if (not 'ZZ' in line): continue
            #if ('2L2Q' in line): continue
            #if ('2L2Nu' in line): continue
            #if (not '2015C' in line): continue

            dataset = line.split()[0]
            dataset = dataset.rstrip()
            dataset = dataset.lstrip()

            datasets.append(dataset)
            cross_section[dataset] = float(line.split()[1])

            cmd = './das_client.py --query="file dataset='+dataset+'" --limit=0 | grep ".root"'
            output = processCmd(cmd)
            while ('error' in output):
                time.sleep(1.0);
                output = processCmd(cmd)
            datasetfiles[dataset] =  output.split()
            nfiles[dataset] = len(datasetfiles[dataset])
 
            cmd = './das_client.py --query="dataset dataset='+dataset+' | grep dataset.nevents" --limit=0'
            output = processCmd(cmd)
            while ('error' in output):
                time.sleep(1.0);
                output = processCmd(cmd)
            nevents[dataset] = output

            print dataset,'xs:',cross_section[dataset],'nfiles:',nfiles[dataset],'nevents:',nevents[dataset]


    # submit the jobs
    print '[Submitting jobs]'
    jobCount=0

    for dataset in datasets:

        njobs = math.ceil(float(nfiles[dataset])/float(filesperjob))

        for job in range(1,int(njobs)+1):

            filename = dataset.split('/')[1]+'_'+dataset.split('/')[2]+'_'+str(job)

            if (opt.RESUBMIT):
                resubmit=False
                with open('resubmit.txt','r') as f:
                    for x in f:
                        fail = x.rstrip()
                        if filename==fail: resubmit=True
                    f.seek(0)
                if (not resubmit): continue

            print 'Submitting job '+str(job)+' out of '+str(njobs)+' for dataset '+dataset

            cfgfile = dataset.lstrip('/')
            cfgfile = cfgfile.replace('/','_')+'_'+str(job)+'.py'

            cmd = 'cp '+cfgtemplate+' '+outDir+'/cfg/'+cfgfile
            output = processCmd(cmd)

            filelist = ''
            for f in range((job-1)*filesperjob,job*filesperjob):
                if ((f+1)>nfiles[dataset]): continue
                filelist += '"'
                if (os.path.isfile('/cms/data'+datasetfiles[dataset][f])):
                    filelist += 'file:/cms/data'
                filelist += datasetfiles[dataset][f]
                filelist += '",'
            filelist = filelist.rstrip(',')

            cmd = "sed -i 's~DUMMYFILELIST~"+filelist+"~g' "+outDir+'/cfg/'+cfgfile
            output = processCmd(cmd)

            filename = dataset.split('/')[1]+'_'+dataset.split('/')[2]+'_'+str(job)
            cmd  = "sed -i 's~DUMMYFILENAME~"+filename+"~g' "+outDir+'/cfg/'+cfgfile
            output = processCmd(cmd)

            cmd  = "sed -i 's~DUMMYCROSSSECTION~"+str(cross_section[dataset])+"~g' "+outDir+'/cfg/'+cfgfile
            output = processCmd(cmd)

            if ('PromptReco-v4' in cfgfile):
                cmd = "sed -i 's~\"PAT\"~\"RECO\"~g' "+outDir+'/cfg/'+cfgfile
                output = processCmd(cmd)

            jobName = filename             
            cmd = 'qsub -o '+outFilesDir+'/'+jobName+'.out -e '+errFilesDir+'/'+jobName+'.err -v jobName='+jobName+',curDir='+currentDir+',outDir='+outDir+',cfgFile='+cfgfile+' -N \"'+jobName+'\" submitFileAna.pbs.sh' 
            #print cmd 

            output = processCmd(cmd) 
            while ('error' in output): 
                time.sleep(1.0); 
                output = processCmd(cmd) 
                if ('error' not in output):
                    print 'Submitted after retry - job for observable '+str(jobCount+1) 

            jobCount += 1 
    
    print '[Submitted '+str(jobCount)+' jobs]'  

# run the submitAnalyzer() as main() 
if __name__ == "__main__": 
    submitAnalyzer() 
