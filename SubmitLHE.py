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
    parser.add_option('-t', '--tag', dest='TAG', type='string',default='', help='string to tag your job')
    parser.add_option('-g', '--gridpack', dest='GRIDPACK', type='string',default='', help='gridpack you want to generate events from')
    parser.add_option('-n', '--njobs', dest='NJOBS', type=int, default=1, help='number of jobs')
    parser.add_option('-e', '--eventsperjob', dest='EVENTSPERJOB', type=int, default=1000, help='events per job')

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

def submitLHE():

    # parse the arguments and options
    global opt, args
    parseOptions()

    gridpack = opt.GRIDPACK
    if (gridpack==''):
        print 'No gridpack specified!!!'
        sys.exit()

    njobs = int(opt.NJOBS)
    eventsperjob = int(opt.EVENTSPERJOB)

    # save working dir
    currentDir = os.getcwd()

    tag = opt.TAG+'_'+time.strftime("%Y%m%d")
    outDir='resultsLHE_'+tag 

    if (not os.path.isdir(outDir)):
        cmd = 'mkdir '+outDir
        processCmd(cmd)

    outFilesDir = 'outFilesLHE_'+tag
    if not os.path.isdir(outFilesDir):
        cmd = 'mkdir '+outFilesDir
        processCmd(cmd)

    errFilesDir = 'errFilesLHE_'+tag
    if not os.path.isdir(errFilesDir):
        cmd = 'mkdir '+errFilesDir
        processCmd(cmd)

    # submit the jobs
    print '[Submitting jobs]'
    jobCount=0


    for job in range(1,njobs+1):
        
        jobName = 'jobLHE_'+str(int(job))             
        cmd = 'qsub -o '+outFilesDir+'/'+jobName+'.out -e '+errFilesDir+'/'+jobName+'.err -v jobName='+jobName+',curDir='+currentDir+',outDir='+outDir+',gridpack='+gridpack+',job='+str(int(job))+',eventsperjob='+str(eventsperjob)+' -N \"'+jobName+'\" submitFileLHE.pbs.sh' 
        #print cmd 

        output = processCmd(cmd) 
        while ('error' in output): 
            time.sleep(1.0); 
            output = processCmd(cmd) 
            if ('error' not in output):
                print 'Submitted after retry - job for observable '+str(observable) 

        jobCount += 1 
    
    print '[Submitted '+str(jobCount)+' jobs]'  

# run the submitLHE() as main() 
if __name__ == "__main__": 
    submitLHE() 
