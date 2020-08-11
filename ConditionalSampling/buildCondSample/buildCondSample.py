import re,sys
import math
import sys
import time
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from multiprocessing import Pool
import pandas
import numpy as np
import pickle
import random
import argparse

sampleSize = 10000
TABLE_CARD = 581012 #forest data

np.random.seed(0)


def getQuerror(trueCardinality, estimatedCardinality):
	if estimatedCardinality == 0 and trueCardinality == 0:
		return 1
	elif estimatedCardinality == 0 or trueCardinality == 0: 
		return max(estimatedCardinality, trueCardinality)
	return max(estimatedCardinality/trueCardinality, trueCardinality/estimatedCardinality)

def getHits(pred_list, df_sample):
	conj_part = True
	plan_sel= []
	for p_num in pred_list:
		conj_part_single = (df_sample["column_"+ query_part[p_num*3]] >= float(query_part[p_num*3+1])) & \
						   (df_sample["column_"+ query_part[p_num*3]] <= float(query_part[p_num*3+2]))
		conj_part = conj_part & conj_part_single
		plan_sel.append([len(df_sample.loc[conj_part_single]),p_num])
	plan_sel.sort(key = lambda x: x[0])
	plan = [x[1] for x in plan_sel]
	return len(df_sample[conj_part]),plan


def buildConditionalSample(query_part,df_table, true_card, n_preds = 5, mod = "best"): 
#mod [best|random] determines whether to use index on random or most selective predicate 
	conj_part_list = []
	single_sel_list  = []
	for pred in range(n_preds):
		conj_part_list.append((df_table["column_"+ query_part[pred*3]] >= float(query_part[pred*3+1])) & \
							  (df_table["column_"+ query_part[pred*3]] <= float(query_part[pred*3+2])))

		single_sel_list.append(len(df_table.loc[conj_part_list[-1]])/TABLE_CARD)


	if mod != "random": # take most selective predicate
		indexed_predicate = single_sel_list.index(min(single_sel_list))
	else: # take random predicate
		indexed_predicate = random.randint(0,n_preds-1)
	idx_pred_conj = conj_part_list[indexed_predicate]
	conditional_tids = df_table.loc[idx_pred_conj].index
	
	if len(conditional_tids) > sampleSize: #sample from conditional tids
		conditional_tids = np.random.choice(conditional_tids, sampleSize, replace = False)
	conditional_sample = df_table.loc[conditional_tids]
	conditional_sample.index = range(len(conditional_sample.index))

	all_idx = [pred for pred in range(n_preds)]
	all_idx.pop(indexed_predicate)
	all_bv = []
	bv_conditional = np.ones(len(conditional_sample), dtype=bool) #unit vector
	for idx in all_idx:
		conj_part_cond_sample = (conditional_sample["column_"+ query_part[idx*3]] >= float(query_part[idx*3+1])) & \
		 (conditional_sample["column_"+ query_part[idx*3]] <= float(query_part[idx*3+2])) 
		cond_sample_res = conditional_sample.loc[conj_part_cond_sample]
		for i in range(len(conditional_sample)):
			if i not in cond_sample_res.index:
				bv_conditional[i] = 0

	# random sample
	random_tids = np.random.choice(range(TABLE_CARD), sampleSize, replace = False)
	random_sample = df_table.loc[random_tids]
	random_sample.index = range(len(random_sample.index))
	full_conjunct = True
	for conj_part in conj_part_list:
		full_conjunct = full_conjunct & conj_part
	random_sample_res = random_sample.loc[full_conjunct]
	bv_random = np.zeros(len(random_sample), dtype=bool)
	for i in random_sample_res.index:
		bv_random[i] = 1


	return [bv_random,bv_conditional,single_sel_list[indexed_predicate], true_card]


def _buildConditionalSample_(param_list):
	query_list = param_list[0]
	true_card_list = param_list[1]
	df_table = param_list[2]
	n_preds = param_list[3]
	mod = "best"
	offset = 0
	if len(param_list)>4 :
		mod = param_list[4]
	if len(param_list)>5 :
		offset = param_list[5]
	bv_and_sel_all = []
	for num, query_part in enumerate(query_list):
		print("num", num+offset)
		bv_and_sel_all.append(buildConditionalSample(query_part, df_table,  \
							 true_card_list[num], n_preds, mod))
	return bv_and_sel_all 

if __name__ == "__main__":

	
	names = ["column_"+str(colID) for colID in range(55)]
	df_table = pandas.read_csv('forest.csv',  header = None, names = names)
	df_sample = np.zeros(sampleSize)

	query_list = []
	bv_and_sel_all = []

	parser = argparse.ArgumentParser(description='Build conditional sampling on forest data.')
	parser.add_argument('--n_preds',  type=int,
                    help='number of predicates in the conjunction')

	parser.add_argument('--random', dest='enumerate', action='store_const',
                    const="random", default="best",
                    help='choose which predicate uses the index (default: predicate with smalles selectivity)')


	args = parser.parse_args()
	n_preds = 5

	if args.n_preds not in [3,5,7]:
		print("invalid number of predicates, --pred_n [3|5|7]")
		exit()

	if os.path.isfile("cond_sample_"+str(args.n_preds)+"q.pkl"):
		print("cond_sample_"+str(args.n_preds)+"q.pkl already exists")
		exit()

	print("sample will be saved as ", "cond_sample_"+str(args.n_preds)+"q.pkl")

	mod = args.enumerate
	

	path_to_query = "forest_qu5"
	if n_preds== 3:
		 	path_to_query = "forest_qu3"
	elif n_preds == 7:
			path_to_query = "forest_qu7"

	true_card_list = [] #only needed for evalCondSample.py!

	print("building 10000 test samples, this may take while...")
	with open(path_to_query,"r") as query_file:
		for line in query_file:
			line_split = line.split("  ")
			query_part = line_split[-1]
			cardinaltiy_part = line_split[-2]
			cardinaltiy_part = cardinaltiy_part.split(" ")
			true_card_list.append(int(cardinaltiy_part[-1]))
			query_part = query_part.split(" ")
			query_list.append(query_part)


	param_list =  [[query_list[0:2000], true_card_list[0:2000], df_table,n_preds, mod,0],\
				  [query_list[2000:4000], true_card_list[2000:4000], df_table,n_preds, mod, 2000],\
				  [query_list[4000:6000], true_card_list[4000:6000], df_table,n_preds, mod, 4000],\
				  [query_list[6000:8000], true_card_list[6000:8000], df_table,n_preds, mod, 6000],\
				  [query_list[8000:10000], true_card_list[8000:10000], df_table, n_preds,mod, 8000]]

	p = Pool(5)

	sample_parts = p.map(_buildConditionalSample_, param_list)
	for cond_sample in sample_parts:
		bv_and_sel_all+=cond_sample


	with open(args.output, "wb") as fb:
		pickle.dump(bv_and_sel_all, fb)


	query_file.close()

