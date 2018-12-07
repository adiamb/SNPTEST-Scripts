import re
import subprocess
from subprocess import PIPE
import sys
import time
import argparse
import gzip




def get_wc(impute):
	global stdout_
	if '.gz' in impute:
		print 'DETECTED AN GZIPPED {} , PLEASE WAIT WHILE LINES ARE BEING COUNTED'.format(impute)
		wc_command = 'zcat '+impute+ ' | wc -l'
	else:
		wc_command = 'wc -l < '+impute
	wc_ = subprocess.Popen(wc_command, shell=True, stdout=PIPE, stderr=PIPE)
	stdout, stderr = wc_.communicate()
	if stderr:
		print 'ERROR TRY AGAIN NOT A VALID FILE OR CHECK DIRECTORY FOR FILE'
	else:
		stdout_ = stdout.strip()
		return(stdout_)

def make_file(chunkid, chunk_n):
	global chunk_filename
	chunk_filename = chunkid+'_'+str(chunk_n)+'.gen'
	#chunk_write = open(chunk_filename, 'w')
	return(chunk_filename)

def main():
	import argparse 
	parser = argparse.ArgumentParser()
	parser.add_argument('-impute', help='A impute file in the gen format', required=True)
	parser.add_argument('-chunks', help='how many chunks you want to divide the files into', required=True)
	parser.add_argument('-chunkid', help='A string for chunkid', required=True)
	parser.add_argument('-gz', choices=['1', '0'], help='Should the output be gzipped? (1 -yes or 0 -no)', required=False)

	args=parser.parse_args()
	impute=args.impute ## the impute file
	chunks = int(args.chunks) ## no of chunks 
	chunkid = args.chunkid ## stringID for chunks
	gzipped = int(args.gz)
	print args

	line_num = int(get_wc(impute))
	lines_chunk = line_num/chunks
	print 'REQUESTED {} CHUNKS CALCULATED  {} AS LINE LOAD PER CHUNK  '.format(chunks, lines_chunk)
	#remainder = float(line_num) % float(chunks)
	if lines_chunk > line_num:
		raise ValueError('CHUNK_LINES GREATER THAN TOTAL LINE_NUM')

	processed_buf = 0
	line_track = 0
	chunk_track = 1
	lines_for_chunk =0


	outfile_name = make_file(chunkid, chunk_track)
	
	if 'gz' in impute and gzipped == 1:
		print 'REQUESTED OUTPUT IN GZIP FORMAT'
		file_handle = gzip.open(impute, 'rb')
		outfile = gzip.open(outfile_name+'.gz', 'w')
	else:
		file_handle = open(impute, 'r')
		outfile = open(outfile_name, 'w')
	
	for line in file_handle:
		line_track += 1
		#lines_for_chunk += 1
		if line_track == 10000:
			processed_buf += 10000
			PercentProcessed ='{0:.1f}'.format((float(processed_buf)/float(line_num))*100)
			print ' <<<<<  {}  PROCESSED LINES  {} % percent done from {} >>>>>'.format(processed_buf, PercentProcessed, impute)
			line_track = 1
		if lines_for_chunk == lines_chunk:
			outfile.close()
			chunk_track += 1
			outfile_name_new=make_file(chunkid =chunkid, chunk_n =chunk_track)
			if 'gz' in impute and gzipped == 1:
				outfile = gzip.open(outfile_name_new+'.gz', 'w')
			else:
				outfile = open(outfile_name_new, 'w')
			outfile.write(line)
			lines_for_chunk = 1
		else:
			outfile.write(line)
			lines_for_chunk += 1
			
			
	outfile.close()
	file_handle.close()
	
#		if chunk_track == chunks/2:
#			print '<<<<<<< PROGRESS - 50% DONE >>>>>>>'

if __name__ == "__main__": main()
