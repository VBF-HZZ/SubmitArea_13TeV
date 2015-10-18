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
    parser.add_option('-i', '--inputdir', dest='INDIR', type='string',default='', help='directory with GEN-SIM files for input')

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

def submitMINIAOD():

    # parse the arguments and options
    global opt, args
    parseOptions()

    indir = opt.INDIR
    if (indir==''):
        print 'No input directory with GEN-SIM files specified!!!'
        sys.exit()

    inputfiles = glob.glob(indir+"/*.root")

    njobs = int(len(inputfiles))

    # save working dir
    currentDir = os.getcwd()

    tag = opt.TAG+'_'+time.strftime("%Y%m%d")

    outDir='resultsMINIAOD_'+tag 
    if (not os.path.isdir(outDir)):
        cmd = 'mkdir '+outDir
        processCmd(cmd)

    outFilesDir = 'outFilesMINIAOD_'+tag
    if not os.path.isdir(outFilesDir):
        cmd = 'mkdir '+outFilesDir
        processCmd(cmd)

    errFilesDir = 'errFilesMINIAOD_'+tag
    if not os.path.isdir(errFilesDir):
        cmd = 'mkdir '+errFilesDir
        processCmd(cmd)

    # submit the jobs
    print '[Submitting jobs]'
    jobCount=0

    for job in range(1,njobs+1):
        
        if (job<=10): continue

        jobName = 'jobMINIAOD_'+str(int(job))             
        cmd = 'qsub -o '+outFilesDir+'/'+jobName+'.out -e '+errFilesDir+'/'+jobName+'.err -v jobName='+jobName+',curDir='+currentDir+',outDir='+outDir+',inputfile='+inputfiles[int(job)-1]+',job='+str(int(job))+',tag='+opt.TAG+' -N \"'+jobName+'\" submitFileMINIAOD.pbs.sh' 
        #print cmd 

        output = processCmd(cmd) 
        while ('error' in output): 
            time.sleep(1.0); 
            output = processCmd(cmd) 
            if ('error' not in output):
                print 'Submitted after retry - job for observable '+str(observable) 

        jobCount += 1 
    
    print '[Submitted '+str(jobCount)+' jobs]'  

# run the submitLHEGENSIM() as main() 
if __name__ == "__main__": 
    submitMINIAOD() 
