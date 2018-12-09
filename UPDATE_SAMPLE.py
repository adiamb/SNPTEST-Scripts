"""
platform:python 2.7
author:Aditya Ambati ambati@stanford.edu 

"""

import sys
import re
from collections import OrderedDict

""" A script to update the phenotypes and covariates for input to SNPTEST"""
def ParsePheno(PhenoFile):
	Dx={}
	CaseCount = 0
	ControlCount = 0
	with open(PhenoFile) as DxFile:
		for n, line in enumerate(DxFile):
			if n > 0:
				LineParse = line.strip().split(',')
				MakeKey = ' '.join(LineParse[:2])
				Pheno = LineParse[2]
				if Pheno == 'NMDAr':
					LineParse[2] = '1'
					CaseCount += 1
				else:
					LineParse[2]='0'
					ControlCount += 1
				PhenoCovs = ' '.join(LineParse[2:])
				if MakeKey in Dx:
					raise ValueError('Duplicate IDs? what are the fucking odds')
				else:
					Dx[MakeKey] = PhenoCovs
	print 'IDENTIFIED {} CASES AND {} CONTROLS '.format(CaseCount, ControlCount)
	return Dx

### update the Dx dictionary with missing data proportion
def ParseMissing(MissingFile, Dx):
	with open(MissingFile) as MisFile:
		for line in MisFile:
			if line:
				LineParse = line.strip().split(' ')
				MakeKey = ' '.join(LineParse[:2])
				Missing = LineParse[2]
				if MakeKey in Dx:
					GetSample = Dx.get(MakeKey)
					Dx[MakeKey] = GetSample+' '+Missing
				else:
					pass
	return Dx

def ParseSample(SampleFile, Dx):
	mds=OrderedDict()
	with open(SampleFile) as SampleIn:
		for n,line in enumerate(SampleIn):
			if n >1:
				LineParse= line.strip().split(' ')
				MakeKey=' '.join(LineParse[:2])
				if MakeKey in mds:
					raise ValueError('Duplicate samples what are the fucking odds ?')
				else:
					if MakeKey in Dx:
						GetDx = Dx.get(MakeKey)
						MakeValue = ' '.join(LineParse[2:6])+' '+GetDx
					else:
						MakeValue = ' '.join(LineParse[2:6])+str(' NA'*11)

					mds[MakeKey] = MakeValue
	print mds
	return mds

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-Sample', help='Orginal impute sample file to be modified', required=True)
	parser.add_argument('-PhenoFile', help='A textfile containing phenos', required=True)
	parser.add_argument('-MissingFile', help='A space delim file containing missing proportion', required=True)
	parser.add_argument('-OutFile', help ='A string as the output filename', required=True)
	Args=parser.parse_args()
	SampleFile = Args.Sample
	PhenoFile = Args.PhenoFile
	OutFile = Args.OutFile
	MissingFile = Args.MissingFile

	GetPhenoDict = ParsePheno(PhenoFile=PhenoFile)
	UpdatePhenoDict = ParseMissing(MissingFile=MissingFile, Dx=GetPhenoDict)
	SampleDict = ParseSample(SampleFile=SampleFile, Dx =UpdatePhenoDict)
	with open(OutFile, 'w') as OutF:
		OutF.write('ID_1 ID_2 missing father mother sex nmda COV1 COV2 COV3 COV4 COV5 COV6 COV7 COV8 COV9 FMISS'+'\n')
		OutF.write('0 0 0 D D D B C C C C C C C C C C'+'\n')
		for k, v in SampleDict.items():
			OutF.write(k+' '+v+'\n')
	print 'Done Writing to file {} '.format(OutFile)



if __name__ == '__main__':main()



# DX ={}
# with open(updated_dx) as Dx_in:
# 	for line in Dx_in:
# 		line_parse=line.strip().split(' ')
# 		if line_parse[1] == '-9':
# 			line_parse[1] = 'NA'
# 		else:
# 			pass
# 		if line_parse[0] not in DX:
# 			DX[line_parse[0]] = line_parse[1]

	

# sample=OrderedDict()
# sample_header=[]
# exclude=[]
# with open(sample_file) as sample_in:
# 	for n, line in enumerate(sample_in):
# 		if n > 1:
# 			line_parse=line.strip().split(' ')
# 			make_key=line_parse[1]
# 			if make_key in DX:
# 				get_DX = DX.get(make_key)
# 				line_parse[6] = str(get_DX)
# 			#if line_parse[6] == '1':
# 			#       line_parse[6] = str(0)
# 			#elif line_parse[6] == '2':
# 			#       line_parse[6] = str(1)
# 			else:
# 				line_parse[6] = 'NA'
			
# 			if make_key in mds:
# 				get_mds=mds.get(make_key)
# 				sample[make_key] = ' '.join(line_parse)+' '+get_mds
# 			else:
# 				sample[make_key]=' '.join(line_parse)+str(' NA'*9)
# 				exclude.append(make_key)
# 		else:
# 			sample_header.append(line.strip())

# with open(out_sample, 'w') as out_f:
# 	out_f.write(sample_header[0]+' COV1 COV2 COV3 COV4 COV5 COV6 COV7 COV8 COV9'+'\n')
# 	out_f.write(sample_header[1]+' C C C C C C C C C'+'\n')
# 	for key, value in sample.iteritems():
# 		out_f.write(value+'\n')

# with open('exclude_samples.txt', 'w') as f_out:
# 	for item in exclude:
# 		f_out.write(item+'\n')
