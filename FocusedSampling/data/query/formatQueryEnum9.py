import re,sys
import math
import pandas
import random 
import numpy as np
from scipy import optimize
from scipy.stats import beta
import sys
import time
import string
import pickle 

#>>> string.ascii_lowercase
#'abcdefghijklmnopqrstuvwxyz'


alphabet = list(string.ascii_uppercase)
print(alphabet)





# table name #query num # cardinality # starting from B att and range 

relName = "forest_format.csv"
outfile = open("query_frt_qu9_format.txt", "w")
query_file = open("forest_qu9", "r")
min_v = 0
for query_num, line in enumerate(query_file):
	if query_num == 10000:break

	lPlan = [0,1,2,3,4,5,6,7,8]
	random.shuffle(lPlan)
	print(lPlan)
	#exit()
	#print(line)
	line_split = line.split("  ")[-1].split()
	int_line = [int(x) for x in line_split]
	if min(int_line)< min_v:
		min_v = min(int_line)
	lPredParts = []
	line_format = ""
	sPredPart = ""
	for num, x in enumerate(line_split):
		if num%3 == 0:
			if num != 0:
				lPredParts.append(sPredPart)
			sPredPart = ""
		if num % 3 == 0:
			line_format += alphabet[int(num/3)+1]+ " "
			sPredPart += alphabet[int(num/3)+1]+ " "
			line_format += str(int(x)+1)
			sPredPart += str(int(x)+1)
		else:
			line_format += str(int(x)+173)
			sPredPart += str(int(x)+173)
		line_format += " "
		sPredPart += " "
	lPredParts.append(sPredPart)
	line_format  = line_format[:-1]
	print(lPredParts)
	print(line_format)
	line_format_enum = ""
	for p in lPlan:
		line_format_enum += lPredParts[p]
	#exit()
	print(min_v)
	outfile.write(relName + " " + str(query_num) + " " + str(int(line.split("  ")[-2].split()[-1])) + " 9 " + line_format_enum[:-1]+"\n")


print(min_v)