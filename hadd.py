import os, sys, glob
from optparse import OptionParser

def main():
   usage = "usage: %prog [options] arg"
   parser = OptionParser(usage)
   parser.add_option("-i", "--indir", dest="indir",
                     help="input directory with .root files")
   parser.add_option("-p", "--prefix",
                     help="new file prefix", default="", dest="prefix")
   parser.add_option("-o", "--outdir",
                     help="output directory", default=".", dest="outdir")
   (options, args) = parser.parse_args()

   indir = str(options.indir)
   outdir = options.outdir
   prefix = options.prefix

   print 'Input Directory is '+indir
   print 'Output Directory is '+outdir
   print 'New file prefix is '+prefix
   samples=glob.glob(indir+"/*_1.root") 
   print "samples:",samples

   for i in range(0,len(samples)):
        samples[i] = samples[i].replace('_1.root','')
        samples[i] = samples[i].replace(indir,'')
        print samples[i]
        os.system('hadd ' + outdir + '/' + prefix + samples[i] +'.root ' + indir + '/' + samples[i] + '_*' + '.root')
   
if __name__ == "__main__":
   main()
