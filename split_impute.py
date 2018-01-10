import re
import subprocess
from subprocess import PIPE
import sys
import time



def get_wc(impute):
	global stdout_
	wc_ = subprocess.Popen('wc -l < '+impute, shell=True, stdout=PIPE, stderr=PIPE)
	stdout, stderr = wc_.communicate()
	if stderr:
		print 'error try again not a valid file or check directory for file'
	else:
		stdout_ = stdout.strip()
		return(stdout_)

def make_file(chunkid, chunk_n):
	global chunk_filename
	chunk_filename = chunkid+'_'+str(chunk_n)+'.impute2'
	#chunk_write = open(chunk_filename, 'w')
	return(chunk_filename)

def main(argv):
	impute=sys.argv[1] ## the impute file
	chunks = int(sys.argv[2]) ## no of chunks 
	chunkid = sys.argv[3] ## stringID for chunks
	
	line_num = int(get_wc(impute))
	lines_chunk = line_num/chunks
	remainder = float(line_num) % float(chunks)
	if lines_chunk > line_num:
		raise ValueError('CHUNK_LINES GREATER THAN TOTAL LINE_NUM')

	processed_buf = 1
	line_track = 1
	chunk_track = 1
	lines_for_chunk =1


	outfile_name = make_file(chunkid, chunk_track)
	outfile = open(outfile_name, 'wr')
	with open(impute) as in_file:
		for n, line in enumerate(in_file):
			line_track += 1
			#lines_for_chunk += 1
			if line_track == 10000:
				processed_buf += 10000
				print "PROCESSED LINES ", processed_buf, (float(processed_buf)/float(line_num))*100, " percent done FROM ", impute
				line_track = 1
			if lines_for_chunk == lines_chunk:
				chunk_track += 1
				outfile_name_new=make_file(chunkid =chunkid, chunk_n =chunk_track)
				outfile = open(outfile_name_new, 'wr')
				lines_for_chunk = 1
			else:
				outfile.write(line)
				lines_for_chunk += 1
	
#		if chunk_track == chunks/2:
#			print '<<<<<<< PROGRESS - 50% DONE >>>>>>>'

if __name__ == "__main__": main(sys.argv)
