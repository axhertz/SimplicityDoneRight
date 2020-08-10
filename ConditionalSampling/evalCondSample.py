import re,sys
import math
import sys
import time
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import pandas
import numpy as np
import pickle
import random
import argparse

TABLE_CARD = 581012 #forest data

def getQuerror(trueCardinality, estimatedCardinality):
	if estimatedCardinality == 0 and trueCardinality == 0:
		return 1
	elif estimatedCardinality == 0 or trueCardinality == 0: 
		return max(estimatedCardinality, trueCardinality)
	return max(estimatedCardinality/trueCardinality, trueCardinality/estimatedCardinality)




if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Evaluate conditional sampling on forest data.')

	parser.add_argument("--sample", help="path to output of buildCondSample.py", type=str, default="cond_sample.pkl" )
	parser.add_argument("--size", help="resize sample [1,...,10000], default is 5000", type=int)
	args = parser.parse_args()

	if not args.sample:
		parser.print_help()
		exit()
	if os.path.isfile( args.sample):
		with open(args.sample, "rb") as fb:
			bv_and_sel_all = pickle.load(fb)
	else:
		print("invalid path to conditional sample")	

	bv_and_sel_all = []
	with open(args.sample, "rb") as fb:
		bv_and_sel_all = pickle.load(fb)

	sampleSize = 5000
	if not args.size:
		print("no sample size specified, using default 5000")
	elif args.size > 0 and args.size <= 10000:
		sampleSize = args.size
	else:
		print("sample size out of range, using default 5000")

	for num in range(len(bv_and_sel_all)):
		q_error_conditional = -1
		q_error_traditional = -1

		#pos 0: random sample | pos 1: cond. sample | pos 2: single sel. | pos3: true card
		bv_random = bv_and_sel_all[num][0][:sampleSize]
		bv_conditional= bv_and_sel_all[num][1][:sampleSize]
		single_sel = bv_and_sel_all[num][2]
		true_card = bv_and_sel_all[num][3]

		if np.count_nonzero(bv_random) == 0: # 0-Tuple-Situation 
			omega =- math.log(0.0001)*(TABLE_CARD)/sampleSize
			q_error_traditional = getQuerror(omega**0.5, true_card)
		else:# k > 0
			trad_est = np.count_nonzero(bv_random)/sampleSize*single_sel
			q_error_traditional = getQuerror(trad_est*TABLE_CARD, true_card)

		if np.count_nonzero(bv_conditional) == 0: # 0-Tuple-Situation 
			omega =- math.log(0.0001)*(TABLE_CARD*single_sel)/sampleSize
			q_error_conditional = getQuerror(omega**0.5, true_card)
		else:# k > 0
			cond_est = np.count_nonzero(bv_conditional)/sampleSize*single_sel
			q_error_conditional = getQuerror(cond_est*TABLE_CARD, true_card)


		print("q-error query ", num,"\t\t conditional sampling ", q_error_conditional,\
			"\t\t traditional sampling ", q_error_traditional)