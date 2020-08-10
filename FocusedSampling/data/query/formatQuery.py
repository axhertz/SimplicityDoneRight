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
#>>> string.ascii_lowercase
#'abcdefghijklmnopqrstuvwxyz'


alphabet = list(string.ascii_uppercase)
print(alphabet)



true_card = []
with open("forest_qu9_cardinality.txt", "r") as file:
	for line in file:
		true_card.append(int(line))


# table name #query num # cardinality # starting from B att and range 

relName = "forest_format.csv"
outfile = open("query_frt_qu9_format.txt", "w")
query_file = open("forest_qu9.txt", "r")
min_v = 0
for query_num, line in enumerate(query_file):
	print(line)
	line_split = line.split()
	int_line = [int(x) for x in line_split]
	if min(int_line)< min_v:
		min_v = min(int_line)

	line_format = ""
	for num, x in enumerate(line_split):
		if num % 3 == 0:
			line_format += alphabet[int(num/3)+1]+ " "
			line_format += str(int(x)+1)
		else:
			line_format += str(int(x)+173)
		line_format += " "
	line_format  = line_format[:-1]

#	print(line_format)


	outfile.write(relName + " " + str(query_num) + " " + str(true_card[query_num]) + " 9 " + line_format+"\n")

print(min_v)