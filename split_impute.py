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
		print 'Detected an gzipped {} , please wait while lines are being counted'.format(impute)
		wc_command = 'zcat '+impute+ ' | wc -l'
	else:
		wc_command = 'wc -l < '+impute
	wc_ = subprocess.Popen(wc_command, shell=True, stdout=PIPE, stderr=PIPE)
	stdout, stderr = wc_.communicate()
	if stderr:
		print 'error try again not a valid file or check directory for file'
	else:
		stdout_ = stdout.strip()
		return(stdout_)

def make_file(chunkid, chunk_n):
	global chunk_filename
	chunk_filename = chunkid+'_'+str(chunk_n)+'.impute'
	#chunk_write = open(chunk_filename, 'w')
	return(chunk_filename)

def main():
	import argparse 
	parser = argparse.ArgumentParser()
	parser.add_argument('-impute', help='A impute file in the gen format', required=True)
	parser.add_argument('-chunks', help='how many chunks you want to divide the files into', required=True)
	parser.add_argument('-chunkid', help='A string for chunkid', required=True)
	args=parser.parse_args()
	impute=args.impute ## the impute file
	chunks = int(args.chunks) ## no of chunks 
	chunkid = args.chunkid ## stringID for chunks
	
	line_num = int(get_wc(impute))
	lines_chunk = line_num/chunks
	print 'REQUESTED CHUNKS {} CALCULATED LINE LOAD PER CHUNK AS {} '.format(chunks, lines_chunk)
	#remainder = float(line_num) % float(chunks)
	if lines_chunk > line_num:
		raise ValueError('CHUNK_LINES GREATER THAN TOTAL LINE_NUM')

	processed_buf = 0
	line_track = 0
	chunk_track = 1
	lines_for_chunk =0


	outfile_name = make_file(chunkid, chunk_track)
	outfile = open(outfile_name, 'w')
	if 'gz' in impute:
		file_handle = gzip.open(impute, 'rb')
	else:
		file_handle = open(impute, 'r')
	
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
			outfile = open(outfile_name_new, 'w')
			outfile.write(line)
			lines_for_chunk = 1
		else:
			outfile.write(line)
			lines_for_chunk += 1
			
			
	outfile.close()
	file_handle.close()
	

if __name__ == "__main__": main()
