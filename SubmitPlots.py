#!/usr/bin/python
#-----------------------------------------------
# Latest update: 2014.09.14
#-----------------------------------------------
import sys, os, pwd, commands
import optparse, shlex, re, glob
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
    parser.add_option('-t', '--tag', dest='TAG', type='string',default='', help='string to tag your job')

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

def submitPlots():

    # parse the arguments and options
    global opt, args
    parseOptions()

    # save working dir
    currentDir = os.getcwd()

    tag = opt.TAG+'_'+time.strftime("%Y%m%d")

    outDir='resultsPlots_'+tag 
    if (not os.path.isdir(outDir)):
        cmd = 'mkdir '+outDir
        processCmd(cmd)

    outFilesDir = 'outFilesPlots_'+tag
    if not os.path.isdir(outFilesDir):
        cmd = 'mkdir '+outFilesDir
        processCmd(cmd)

    errFilesDir = 'errFilesPlots_'+tag
    if not os.path.isdir(errFilesDir):
        cmd = 'mkdir '+errFilesDir
        processCmd(cmd)

    # submit the jobs
    print '[Submitting jobs]'
    jobCount=0

    variables = ['massZ_2e','massZ_2mu',
                 'ptlep1_2e','ptlep1_2mu','etalep1_2e','etalep1_2mu',
                 'ptlep2_2e','ptlep2_2mu','etalep2_2e','etalep2_2mu',
                 'isolep1_2e','isolep1_2mu',
                 'isolep2_2e','isolep2_2mu',
                 'siplep1_2e','siplep1_2mu',
                 'siplep2_2e','siplep2_2mu',
                 'mvalep1_2e','mvalep2_2e',
                 'njets_2e','njets_2mu','njets_emu',
                 'ptjet1_2e','ptjet1_2mu','ptjet1_emu',
                 'etajet1_2e','etajet1_2mu','etajet1_emu',
                 'njets2p5_2e','njets2p5_2mu','njets2p5_emu',
                 'met_2e','met_2mu','met_emu',
                 'nVtx_2e','nVtx_2mu',#'nVtx_rw_2e','nVtx_rw_2mu'   
                 'allfsrPhotons_dR_2e','allfsrPhotons_dR_2mu',
                 'allfsrPhotons_iso_2e','allfsrPhotons_iso_2mu',
                 'allfsrPhotons_pt_2e','allfsrPhotons_pt_2mu',
                 'allfsrPhotons_dROpt2_2e','allfsrPhotons_dROpt2_2mu',
              ]


    job = 0
    for var in variables:

        job +=1

        jobName = 'jobPlots_'+str(int(job))             

        cmd = 'qsub -o '+outFilesDir+'/'+jobName+'.out -e '+errFilesDir+'/'+jobName+'.err -v jobName='+jobName+',curDir='+currentDir+',outDir='+outDir+',variable='+var+',job='+str(int(job))+',tag='+opt.TAG+' -N \"'+jobName+'\" submitFilePlots.pbs.sh' 
        #print cmd 

        output = processCmd(cmd) 
        while ('error' in output): 
            time.sleep(1.0); 
            output = processCmd(cmd) 
            if ('error' not in output):
                print 'Submitted after retry - job for observable '+str(observable) 

        jobCount += 1 
    
    print '[Submitted '+str(jobCount)+' jobs]'  

if __name__ == "__main__": 
    submitPlots() 
