import pandas as pd
import sys, os 
import psycopg2
import re
import glob
import numpy as np
import pickle
import math


"""
CREATE FUNCTION count_estimate(query text) RETURNS integer AS
$func$
DECLARE
    rec   record;
    rows  integer;
BEGIN
    FOR rec IN EXECUTE 'EXPLAIN ' || query LOOP
        rows := substring(rec."QUERY PLAN" FROM ' rows=([[:digit:]]+)');
        EXIT WHEN rows IS NOT NULL;
    END LOOP;

    RETURN rows;
END
$func$ LANGUAGE plpgsql;
"""



def q_error(val1,val2):
	return max(max(val1,1)/max(val2,1),max(val2,1)/max(val1,1) )

#Primary keys of the join order benchmark.
pks = ["at.id","cct1.id","cct2.id","cc.id", "mc.id", "mc1.id", "mc2.id", "ct.id","cn.id","cn1.id",\
		 "cn2.id", "ml.id", "t.id", "t1.id", "t2.id","mk.id", "k.id", "lt.id", "kt.id", "kt1.id",\
		  "kt2.id","chn.id", "mi.id", "ci.id","mi_idx.id", "mi_idx1.id", "mi_idx2.id", "rt.id",\
		  "an.id", "an1.id", "a1.id", "n.id", "n1.id", "pi.id", "it.id", "it1.id", "it2.id", "it3.id", "miidx.id"]

#Foreign keys of the join order benchmark.
fks = ["at.movie_id", "cc.subject_id", "cc.status_id", "cc.movie_id", "mc.movie_id", "mc1.movie_id", "mc2.movie_id",\
		"mc.company_type_id","mc1.company_type_id","mc2.company_type_id","mc.company_id","mc1.company_id","mc2.company_id",\
		"ml.movie_id", "ml.link_type_id", "ml.linked_movie_id", "t.kind_id","t1.kind_id", "t2.kind_id", "mk.movie_id",\
		"mk.keyword_id", "mi.movie_id", "mi.info_type_id",	"mi_idx.movie_id","mi_idx1.movie_id","mi_idx2.movie_id",\
		"mi_idx.info_type_id","mi_idx1.info_type_id", "mi_idx2.info_type_id","ci.movie_id", "ci.person_id",\
		"ci.role_id","ci.person_role_id","an.person_id", "an1.person_id", "a1.person_id","pi.person_id",\
		"pi.info_type_id","miidx.movie_id", "miidx.info_type_id", "it3.info", "cct1.kind", "cct2.kind"]

#Frequency of single most frequent value. This is independent of the query and might actually be stored in the database.
MF_dict = {"mc":151,"mc1": 151, "mc2": 151,"ml":569, "ml.linked_movie_id": 131, "ml.link_type_id": 8593, \
	"mi": 2997, "mi_idx":4, "miidx": 4,  "mi_idx1":4,  "mi_idx2":4,"cc":2, "at":47, "mk":976, "mk.keyword_id": 88282,\
	"ci":1724, "pi":1772, "an": 85 , "an1":85, "a1": 85, "ci.person_id": 14969, "mi.info_type_id":5433157,\
	"mi_idx.info_type_id":789155, "miidx.info_type_id":789155, "mi_idx1.info_type_id":789155,\
	"mi_idx2.info_type_id":789155, "pi.info_type_id":903867, "mc.company_id":71942 , "mc.company_type_id":2909468,\
	"cc.status_id":110494, "cc.subject_id":85941, "ci.role_id": 20490752,"ci.person_role_id": 2140172 }



impl_dir = input("path to implicit queries: ")
if not os.path.isdir(impl_dir):
	print("invalid directory", impl_dir)
	exit()
if impl_dir[-1] != "/":
	impl_dir += "/"
out_dir = input("save explicit queries to: ")
if not os.path.isdir(out_dir):
	print("invalid directory", out_dir)
	exit()
if out_dir[-1] != "/":
	out_dir += "/"

print("#Postgres Connection")
host= input("host: ")
db = input("database: ")
usr = input("user: ")
pwd = input("password: ")


query_list = glob.glob(impl_dir+"*.sql")
query_list = [q.split("/")[-1] for q in query_list]


for query_file in query_list:
	print("rewriting", query_file)
	with open(impl_dir+query_file, "r") as file:
		data = file.read()

	
	#################### Start Parsing Query #################################

	select_clause = data.split("FROM")[0]
	select_target = re.findall( r'MIN\((.*?)\)',select_clause)

	from_clause = data.split("FROM")[1].split("WHERE")[0]

	rel_names =[]

	for relation_string in from_clause.split(","):
		rel_names.append(relation_string.split(" ")[-1].replace("\n",""))

	where_clause = data.split("WHERE")[-1]
	where_string = where_clause.split("\n")
	where_string = [s.replace("AND", "",1).replace("  "," ") for s in where_string if s != ""]
		
	dict_rel_filter = {}
	filters = []
	join_filters = []


	for w_r in where_string:
		test_rels = []
		for sub_string in w_r.split(" "):
			if "." in sub_string:
				test_rels.append(sub_string.split(".")[0]+".id")	
		if len(set(test_rels).intersection(set(pks)))==1:
			rel = w_r.lstrip().rstrip().split(".")
			rel[0] = rel[0].replace("(","").replace(")","")
			if not rel[0] in dict_rel_filter.keys():
				dict_rel_filter[rel[0]] = [w_r.lstrip().rstrip()]
			else:
				dict_rel_filter[rel[0]].append(w_r.lstrip().rstrip())
			filters.append(w_r.lstrip().rstrip())
		else:
			join_filters.append(w_r.lstrip().rstrip())

	select_smts = []

	for rel in dict_rel_filter.keys():
		for relation_string in from_clause.split(","):
			if len(set([rel]).intersection(set(relation_string.lstrip().rstrip().split(" ")))) == 1:
				select_smt = "select count(*) from "+ relation_string.lstrip() + " where "
				for num, fltr in enumerate(dict_rel_filter[rel]):
					if num == 0:
						select_smt += " "+fltr
					else:
					 select_smt += " AND "+fltr
				select_smts.append(select_smt+";")			
				break

	for rel in rel_names:
		if rel not in dict_rel_filter.keys():
			for relation_string in from_clause.split(","):
				if len(set([rel]).intersection(set(relation_string.lstrip().rstrip().split(" ")))) == 1:
					select_smts.append("select count(*) from "+ relation_string.lstrip() +";")
					break


	fk_edges = []
	for fk in fks:
		for pk in pks:
			if (" "+fk + " = " +pk+ " " in data or " "+pk + " = " + fk +" " in data)\
			or (" "+fk + " = " +pk+ "\n" in data or " "+pk + " = " + fk +"\n" in data)\
			or (" "+fk + " = " +pk+ ";" in data or " "+pk + " = " + fk +";" in data): 
				fk_edges.append([fk.split(".")[0] ,pk.split(".")[0]])

	if len(fk_edges)!= data.count(".id"):
		print("fk edges: ",len(fk_edges), fk_edges)
		print("Failure, inconsistent number of joins.")
		exit()

	#################### End Parsing Query #################################


	#################### Start Statistic requests  #########################
	connection = psycopg2.connect(host=host, database=db, user=usr, password=pwd)
	
	rel_dict = {}
	#get filter selectivity estimates
	cursor = connection.cursor()
	for stm in select_smts:
		stm_est = stm.replace("count(*)","*").replace("\'","\'\'").replace(";","")
		stm_est = "select count_estimate(\'{}\');".format(stm_est)
		cursor.execute(stm_est)
		for query in cursor:
			for rel in rel_names:
				if " "+rel+ " " in stm or " " +rel+"\n" in stm or " "+rel+";"in stm:
					rel_dict[rel] = math.ceil(query[0])

	rel_dict_copy = rel_dict.copy()
	connection.close()
	#################### End Statistic requests  #########################
	

	#################### Start Upper Bound Of PK-FK Joins  ##############
	fk_fk_rel = []
	fk_fk_target = []

	for rel in rel_names:
		if " "+rel + "." +"movie_id" in data or  " "+rel + "." + "linked_movie_id" in data :
			fk_fk_target.append(rel)

	fk_fk_target= list(set(fk_fk_target))

	sub_join_rel_dict = {}
	for r in fk_fk_target:
		sub_join_rel_dict[r] = []
		for jf in join_filters:
			jf_test =[]
			jf_t1 = jf.replace(";","").split(" ")
			for j in jf_t1:
				for k in j.split("."):
					jf_test.append(k)
			if r in jf_test:
				sub_join_rel_dict[r].append(list(set(rel_names).intersection(set(jf_test))- set([r]))[0])


	# get upper bound of fk-pk joins and handle synonyms
	person_id_list = [ "an", "pi", "an1", "a1"]
	for key in fk_fk_target:
		intermediate = rel_dict[key]
		if key not in MF_dict.keys():
			 print("error: rel" ,key, "not in MF_dict", fk_fk_target)
			 exit()

		for rel in sub_join_rel_dict[key]:
			if rel in fk_fk_target: continue
			if rel in ['t', 'n', 'n1']: continue
			if rel in ["it", "it1", "it2", "it3"] and key in ["miidx", "mi_idx", "mi_idx1","mi_idx2","mi"]:
				intermediate = min( min(intermediate/MF_dict[key+".info_type_id"], rel_dict[rel]) * MF_dict[key+".info_type_id"], intermediate)
			elif rel in["cn","cn1","cn2"] and key in ["mc","mc1","mc2"]:
				intermediate = min( min(intermediate/MF_dict["mc.company_id"], rel_dict[rel]) * MF_dict["mc.company_id"], intermediate)
			elif rel == "ct" and key in ["mc","mc1","mc2"]:
				intermediate = min( min(intermediate/MF_dict["mc.company_type_id"], rel_dict[rel]) * MF_dict["mc.company_type_id"], intermediate)
			elif rel == "lt" and key == "ml":
				intermediate = min( min(intermediate/MF_dict["ml.link_type_id"], rel_dict[rel]) * MF_dict["ml.link_type_id"], intermediate)
			elif rel == "t2" and key == "ml":
				intermediate = min( min(intermediate/MF_dict["ml.linked_movie_id"], rel_dict[rel]) * MF_dict["ml.linked_movie_id"], intermediate)
			elif rel in ["k"] and key == "mk":
				intermediate = min( min(intermediate/MF_dict["mk.keyword_id"], rel_dict[rel]) * MF_dict["mk.keyword_id"], intermediate)
			elif rel in ["rt"] and key == "ci":
				intermediate = min( min(intermediate/MF_dict["ci.role_id"], rel_dict[rel]) * MF_dict["ci.role_id"], intermediate)
			elif rel == "chn" and key == "ci":
				intermediate = min( min(intermediate/MF_dict["ci.person_role_id"], rel_dict[rel]) * MF_dict["ci.person_role_id"], intermediate)
			elif rel in ["cct1", "cct2"] and key == "cc":
				if rel+".id = cc.status_id" in data:
					intermediate = min( min(intermediate/MF_dict["cc.status_id"], rel_dict[rel]) * MF_dict["cc.status_id"], intermediate)
				else:
					intermediate = min( min(intermediate/MF_dict["cc.subject_id"], rel_dict[rel]) * MF_dict["cc.subject_id"], intermediate)
			elif rel not in person_id_list:
				intermediate = min( min(intermediate/MF_dict[key], rel_dict[rel]) * MF_dict[key], intermediate)
			else:
				sub_join_rel_dict[rel] = [rel] 
		rel_dict[key] = math.ceil(intermediate)


	# decide n, n1
	n_tar = None
	min_n_rel = None
	if "ci" in rel_dict.keys():
		min_n_card = 10**100
	
		if "n" in sub_join_rel_dict["ci"]:
			n_tar = "n"
		if "n1" in sub_join_rel_dict["ci"]:
			n_tar = "n1"
		if n_tar:
			for pk_id_tar in person_id_list:
				if pk_id_tar in sub_join_rel_dict.keys():
					cur_card = min(rel_dict[pk_id_tar], MF_dict[pk_id_tar] * rel_dict[n_tar])
					if cur_card < min_n_card:
						min_n_rel = pk_id_tar
						min_n_card = cur_card
		if n_tar:
			if  min_n_rel == "ci" or not min_n_rel:
				rel_dict["ci"] = min( min(rel_dict["ci"]/MF_dict["ci.person_id"], rel_dict[n_tar]) * MF_dict["ci.person_id"], rel_dict["ci"])
			elif min_n_rel is not None and min_n_rel != "ci":
				rel_dict[min_n_rel] = min( min(rel_dict[min_n_rel]/MF_dict[min_n_rel], rel_dict[n_tar]) * MF_dict[min_n_rel], rel_dict[min_n_rel])
				sub_join_rel_dict[min_n_rel].append(n_tar)
				sub_join_rel_dict["ci"] = list(set(sub_join_rel_dict["ci"])- set([n_tar]))

	# apply pk-fk join with title only to smallest n:m candidate
	use_ci = False
	if "t" in rel_dict.keys():
		t_rel = None
		min_card = 10**100
		for key in fk_fk_target:
			if not "t" in sub_join_rel_dict[key]: continue
			cur_card = min(rel_dict[key], MF_dict[key] * rel_dict["t"])
			if cur_card < min_card:
				min_card = cur_card
				t_rel = key
		for pk_id_tar in person_id_list:
			if pk_id_tar in sub_join_rel_dict.keys():
				if rel_dict[pk_id_tar] <= min_card:
					use_ci = True
					break
		if not use_ci:
			rel_dict[t_rel] = min_card


	if "ci" in sub_join_rel_dict.keys():
		fk_fk_target += list(set(person_id_list).intersection(set(sub_join_rel_dict["ci"])))
		sub_join_rel_dict["ci"] = list(set(sub_join_rel_dict["ci"])- set(person_id_list))

	if "it3.id = pi.info_type_id" in data:
		if min_n_rel == "pi" and rel_dict["it3"]< rel_dict[n_tar]:
			sub_join_rel_dict["pi"] = [n_tar] + ["it3", "pi"]
		elif min_n_rel == "pi":
			sub_join_rel_dict["pi"] =  ["it3"] + [n_tar] + ["pi"]
		else:	
			sub_join_rel_dict["pi"] = ["it3", "pi"]
		rel_dict["pi"] = min(rel_dict["pi"]/MF_dict["pi.info_type_id"], rel_dict["it3"])*MF_dict["pi.info_type_id"]
	if "it.id = pi.info_type_id" in data:
		if min_n_rel == "pi" and rel_dict["it"]< rel_dict[n_tar]:
			sub_join_rel_dict["pi"] = [n_tar] + ["it", "pi"]
		elif min_n_rel == "pi":
			sub_join_rel_dict["pi"] =  ["it"] + [n_tar] + ["pi"]
		else:	
			sub_join_rel_dict["pi"] = ["it", "pi"]
		rel_dict["pi"] = min(rel_dict["pi"]/MF_dict["pi.info_type_id"], rel_dict["it"])*MF_dict["pi.info_type_id"]
	min_card = sys.maxsize
	best_rel = None

	# prepare dictionary of n:m join candidates 
	for r in list(set(fk_fk_target)- set(person_id_list)):
		if rel_dict[r] < min_card:
			best_rel = r
			min_card = rel_dict[r]
	if use_ci: best_rel = "ci"
	hit_t = False
	hit_t1 = False
	hit_t2 = False
	sub_join_rel_dict_clean = {}
	for key in sub_join_rel_dict.keys():
		filter_exp = list(set(sub_join_rel_dict[key]) - set(fk_fk_target))
		if key != best_rel: 
			filter_exp = list(set(filter_exp) - set(sub_join_rel_dict[best_rel]))
		card_rel = [( rel_dict[rel],i) for i,rel in enumerate(filter_exp)]
		card_rel.sort(reverse = True)

		filter_exp_sorted = [filter_exp[i] for _, i in card_rel]
		filter_exp_sorted = filter_exp_sorted+ [key]

		# hard coded handling of synonyms 
		if "t" in filter_exp_sorted and "kt.id = t.kind_id" in data and not hit_t:
			filter_exp_sorted = ["kt"] + filter_exp_sorted
			hit_t = True
		if "t1" in filter_exp_sorted and "kt1.id = t1.kind_id" in data and not hit_t1:
			filter_exp_sorted = ["kt1"] + filter_exp_sorted
			hit_t1 = True

		if "t2" in filter_exp_sorted and "kt2.id = t2.kind_id" in data and not hit_t2:
			filter_exp_sorted = ["kt2"] + filter_exp_sorted
			hit_t2 = True
		sub_join_rel_dict_clean[key] = filter_exp_sorted
	#################### End Upper Bound Of PK-FK Joins  ##############
	

	#################### Start Greedy Enumeration  ####################
	all_candidates = fk_fk_target.copy()
	best_candidate_position = 0
	visited_candidates = np.zeros(len(fk_fk_target))
	visited_candidates_n = []
	greedy_plan = []
	max_frequency = 1
	current_size = 1
	unroll_rel =[]

	# Greedy join enumeration according to n:m candidates
	for join_num in range(len(fk_fk_target)):
		best_cost = 10**100
		best_frequency = 1
		best_rel = None
		for position, rel in enumerate(all_candidates):
			is_ml = False
			if visited_candidates[position] != 0 :
				continue
			if len(set(person_id_list).intersection(set(visited_candidates_n))) and rel not in person_id_list and rel != "ci" and "ci" not in visited_candidates_n:
				continue 
			if rel in person_id_list and "ci" not in visited_candidates_n and  len(set(person_id_list).intersection(set(visited_candidates_n))) < len(visited_candidates_n):
				continue 
			if rel == "it3" and "pi" not in visited_candidates_n:
				continue
			if not np.count_nonzero(visited_candidates):
				current_cost = rel_dict[rel]
			else:
				current_cost = min(current_size/max_frequency, rel_dict[rel]/MF_dict[rel])*MF_dict[rel] * max_frequency
			if current_cost <= best_cost:
				best_candidate_position = position
				best_cost = current_cost
				best_frequency = MF_dict[rel]*max_frequency
				best_rel = rel

		# decide whether to employ sub-query on n:m join candidate
		greedy_plan.append(fk_fk_target[best_candidate_position])
		if len(sub_join_rel_dict_clean[fk_fk_target[best_candidate_position]]) > 1 and join_num != 0:
			if best_rel not in rel_dict.keys():
				print(best_rel, "not in", rel_dict)
			if rel_dict_copy[best_rel] == rel_dict[best_rel]: #no sub-query since pk-fk join may not shrink intermediate 
				unroll_rel.append(fk_fk_target[best_candidate_position])

	
		visited_candidates[best_candidate_position] = True
		visited_candidates_n.append(all_candidates[best_candidate_position])
		max_frequency = best_frequency
		current_size = best_cost


	######## Resemble Explict SQL According to Plans ################
	def get_sub_join(sub_join_list, set_marker = False , delay = False):
		first_sf = False
		remove =[]
		visited_jf = []
		delayed_stmt = ""
		join_stmt = ""
		for r_num, r in enumerate(sub_join_list):
			if join_stmt != "":
				join_stmt += "\njoin "
			for relation_string in from_clause.split(","):
				if r == relation_string.split(" AS ")[-1].replace("\n", "").replace(",","").replace(";",""):
					join_stmt +=  relation_string.rstrip().lstrip() + " "
			if set_marker and r_num == 0: join_stmt+="#"
			if r_num != 0: join_stmt += "on ("
			found_hit_in_on = False
			filter_stmt = ""
			for sf in filters:
				for sf_sp in sf.split(" "):
					if len(set([r]).intersection(set(sf_sp.split(".")))) and sf not in remove:
						if not found_hit_in_on:
							filter_stmt += sf
							found_hit_in_on = True 
						else:
							filter_stmt +=  " AND "+ sf
						remove.append(sf)
					if len(set([r]).intersection(set(sf_sp.split(".")))) and sf not in remove:
						if not found_hit_in_on:
							filter_stmt  +=    sf
							found_hit_in_on = True 
						else:
							filter_stmt += " AND "+ sf
						remove.append(sf)
			if found_hit_in_on and r_num == 0:
				first_sf = True
			if r_num == 0 and delay:
				delayed_stmt += filter_stmt
			else:
				join_stmt+=filter_stmt
			for jf in join_filters:
				if r_num == 0: continue
				if r_num >= len(sub_join_list)+1: continue
				jf_test =[]
				jf_split = jf.split(" ")
				for jfs in jf_split:
					for jfss in jfs.split("."):
						jf_test.append(jfss)
				visited_jf = list(set(visited_jf+[sub_join_list[r_num], sub_join_list[r_num-1]]))
				for rr_num in range(r_num):
					if sub_join_list[r_num] in jf_test and  sub_join_list[rr_num] in jf_test and jf not in remove:
						if not found_hit_in_on:
							join_stmt +=  jf 
							found_hit_in_on = True
						else:
							join_stmt +=  " AND "+ jf
						remove.append(jf)
			if delayed_stmt != "" and delay and r_num == 1:
				join_stmt += " and "+ delayed_stmt +")" 
			elif r_num != 0 or (first_sf and not delay):
				join_stmt += ")"

		return join_stmt, first_sf

	join_stmt = ""
	previous_is_subquery = False
	visited_sub_join = []
	is_subquery =[]
	last_fk_fk = ""
	last_fk_fk_pos=0
	rename_rel = []
	
	for pos, tar in enumerate(greedy_plan):

		first_on = False
		sub_sel = False
		if pos == 0  or len(sub_join_rel_dict_clean[tar]) == 1 or tar in unroll_rel:
			if pos != 0: join_stmt += "\nJOIN "
			sub_join_list =  sub_join_rel_dict_clean[tar].copy()
			sub_join_list.reverse()
			join_append, first_on = get_sub_join(sub_join_list,pos != 0, pos ==0)
			join_stmt+= join_append
			is_subquery.append(False)
		else:
			sub_sel = True
			select_tar = "movie_id"
			if tar in person_id_list:
				select_tar = "person_id"
			if tar == "ml":
				select_tar = "linked_movie_id, movie_id"
			if tar == "ci":
				select_tar = "person_id, movie_id"
			if tar == "it3":
				select_tar = "id"
			join_stmt += "\njoin\n (select " + select_tar + " from "
			sub_join_list =  sub_join_rel_dict_clean[tar].copy()
			sub_join_list.reverse()
			join_append, first_on = get_sub_join(sub_join_list, delay = True)
			join_stmt+= join_append
			join_stmt+= ") as "+"t_"+tar +"#"
			is_subquery.append(True)
		
		
		if pos == 0:
			visited_sub_join.append(tar)
			if tar in ["ci", "mc", "mi", "mc1", "mc2", "ml","mi_idx", "mi_idx2", "mi_idx1", "mk","cc", "miidx", "at"]:
				last_fk_fk = tar
				last_fk_fk_pos = 0

			continue
	
		join_fin = ""
		stem1 = ""
		stem2 = ""

		if is_subquery[-1]: 
			stem1 = "t_"
			rename_rel.append(tar)
		if "t_"+last_fk_fk+"." in join_stmt:
			stem2 = "t_"
		if tar in person_id_list: 
			if tar == "pi" and last_fk_fk == "mk" and "an.person_id = t_ci.person_id" in join_stmt:
				join_fin += stem1+tar+".person_id = " + "t_ci.person_id"
			elif tar == "an" and last_fk_fk == "cc" and "ci" in visited_sub_join[0]:
				join_fin += stem1+tar+".person_id = " + "ci.person_id"
			elif tar == "pi" and last_fk_fk == "mk" and "ci" in visited_sub_join[0]:
				join_fin += stem1+tar+".person_id = " + "ci.person_id" 
			else:
				join_fin += stem1+tar+".person_id = " +stem2+visited_sub_join[-1]+".person_id"
		elif tar == "it3" and "pi" in visited_sub_join:
			 join_fin += stem1+tar+".id = " +"pi.person_id"
		elif tar == "n":
			 join_fin += stem1+tar+".id = " +"pi.person_id"
		elif tar == "n":
			join_fin += stem1+tar+".linked_movie_id = " +stem2+last_fk_fk+".movie_id"
		elif visited_sub_join[-1] == "ml" and ".linked_movie_id" in data and\
			 (tar+".movie_id = " + last_fk_fk+".linked_movie_id" in data or \
			  last_fk_fk+".linked_movie_id = " + tar+".movie_id" in data):
			join_fin += stem1+tar+".movie_id = " +stem2+last_fk_fk+".linked_movie_id"
		elif tar == "mc2" and "ml.movie_id = mc1.movie_id" in data and "ml" == visited_sub_join[0]:
			join_fin += stem1+tar+".movie_id = ml.linked_movie_id"
		elif tar == "ml" and "ci.movie_id = ml.linked_movie_id" in data and last_fk_fk == "ci": 
			join_fin += stem1+"ml.linked_movie_id = "+stem2+"ci.movie_id"
		elif tar == "mc1" and "ml.linked_movie_id = mc2.movie_id" in data and "ml" in visited_sub_join[0]:
			join_fin += stem1+tar+".movie_id = ml.movie_id"
		elif tar == "mi_idx1" and "ml.movie_id = mi_idx1.movie_id" in data and "ml" in visited_sub_join[0]:
			join_fin += stem1+tar+".movie_id = ml.movie_id"
		elif tar == "mi_idx2" and "ml.linked_movie_id = mi_idx2.movie_id" in data and "ml" in visited_sub_join[0]:
			join_fin += stem1+tar+".movie_id = ml.linked_movie_id"
		elif tar == "ci" and len(set(person_id_list).intersection(set(visited_sub_join))):
			pk_fk_tar = visited_sub_join[-1]
			join_fin += stem1+tar+".person_id = " +stem2+pk_fk_tar +".person_id"
		else:
			join_fin += stem1+tar+".movie_id = " +stem2+last_fk_fk+".movie_id"
		if first_on and not is_subquery[-1]:
			join_stmt = join_stmt.replace("#", " \non("+join_fin+" and ")
		else:
			join_stmt = join_stmt.replace("#", " \non("+join_fin+")")
		visited_sub_join.append(tar)

		if tar in ["ci", "mc", "mi", "mc1", "mc2", "ml","mi_idx", "mi_idx2", "mi_idx1", "mk", "cc", "miidx", "at"]:
			last_fk_fk = tar
			last_fk_fk_pos = pos

	
	join_stmt = join_stmt.replace("on ()", "")
	join_stmt = "select count(*) from \n" +join_stmt
	if not "(select person_id from aka_name" in join_stmt:
		join_stmt = join_stmt.replace("t_an.", "an.")
	join_stmt = join_stmt.replace(";", "")


	with open(out_dir+query_file,"w") as outfile:
			outfile.write(join_stmt +";")
