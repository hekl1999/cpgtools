#!/usr/bin/env python
"""
#=========================================================================================
Convert Beta-value into M-value or vice versa
#=========================================================================================
"""


import sys,os
import collections
import numpy as np
from scipy import stats
from optparse import OptionParser
from cpgmodule import ireader
from cpgmodule.utils import *

__author__ = "Liguo Wang"
__copyright__ = "Copyleft"
__credits__ = []
__license__ = "GPL"
__version__="0.1.4"
__maintainer__ = "Liguo Wang"
__email__ = "wang.liguo@mayo.edu"
__status__ = "Development"

	
def main():
	usage="%prog [options]" + "\n"
	parser = OptionParser(usage,version="%prog " + __version__)
	parser.add_option("-i","--input-file",action="store",type="string",dest="input_file",help="Data file with the 1st row containing sample IDs (must be unique) and the 1st column containing CpG positions or probe IDs (must be unique). This file can be a regular text file or compressed file (*.gz, *.bz2) or accessible url.")
	parser.add_option("-d","--dtype",action="store",type='string', dest="data_type",help="Data type either \"Beta\" or \"M\".")
	parser.add_option("-o","--output",action="store",type='string', dest="out_file",help="Output file.")
	(options,args)=parser.parse_args()
	
	print ()

	if not (options.input_file):
		print (__doc__)
		parser.print_help()
		sys.exit(101)
	if not (options.data_type):
		print (__doc__)
		parser.print_help()
		sys.exit(101)				
	if not (options.out_file):
		print (__doc__)
		parser.print_help()
		sys.exit(103)	
	
	FOUT = open(options.out_file, 'w')		
	
	if options.data_type.lower() == "beta":
		printlog("Convert Beta-value file \"%s\" into M-value file \"%s\" ..." % (options.input_file, options.out_file))
	elif options.data_type.lower() == "m":
		printlog("Convert M-value file \"%s\" into Beta-value file \"%s\" ..." % (options.input_file, options.out_file))
	else:
		print ("Data type must be \"Beta\" or \"M\"", file=sys.stderr)
		sys.exit(0)
		
	line_num = 1
	for l in ireader.reader(options.input_file):
		f = l.split()
		if line_num == 1:
			print (l, file=FOUT)
		else:
			probe_ID = f[0]
			input_values = f[1:]
			output_values = []
			for iv in input_values:
				#deal with non-numerical values
				try:
					if options.data_type.lower() == "beta":
						ov = np.log2(float(iv)/(1.0 - float(iv)))
					elif options.data_type.lower() == "m":
						ov = (2**float(iv))/(2**float(iv) + 1)
				except:
					ov = np.nan
				output_values.append(ov)
			print (probe_ID + '\t' + '\t'.join([str(i) for i in output_values]), file=FOUT)
		line_num += 1

	FOUT.close()
	
if __name__=='__main__':
	main()				
					
					
					
					
					
					
					
					
					
					
					
					