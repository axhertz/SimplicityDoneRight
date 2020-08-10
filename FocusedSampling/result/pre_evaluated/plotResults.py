import re,sys
import csv
import pickle
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import random

import matplotlib.gridspec as gridspec

matplotlib.rc('pdf', fonttype=42)



fig, ax = plt.subplots(1, 3, figsize=(25, 10), sharey=True)
plt.subplots_adjust(wspace=-1, hspace=0)

for num, num_bool in enumerate(["3","5","7"]):
	trad_reuse_tids = []
	traditional = []
	foc_no_enum = []
	foc_enum =[]

	with open("TradSample_qu{}_reuse_TIDs.txt".format(num_bool),"r") as file:
		for line in file:
			line_split = line.split()
			trad_reuse_tids.append(int(line_split[1]))

	with open("TradSample_qu{}.txt".format(num_bool),"r") as file:
		for line in file:
			line_split = line.split()
			traditional.append(int(line_split[1]))

	with open("FocSample_qu{}_no_enum.txt".format(num_bool),"r") as file:
		for line in file:
			line_split = line.split()
			foc_no_enum.append(int(line_split[1]))

	with open("FocSample_qu{}_enum.txt".format(num_bool),"r") as file:
		for line in file:
			line_split = line.split()
			foc_enum.append(int(line_split[1]))




	x = np.linspace(0,10,100)

	handle_traditional, = ax[num].plot(x, np.array(traditional)/1000,color= "firebrick", alpha = 0.9,linestyle="--" , lw=2.5,label="traditional")
	handle_trad_reuse_tids, = ax[num].plot(x, np.array(trad_reuse_tids)/1000, 'black', alpha= 0.7, linestyle = ":" , lw = 4.5, label="trad. - fixed tids")
	handle_foc_no_enum, = ax[num].plot(x, np.array(foc_no_enum)/1000,'steelblue',linestyle="-." , alpha = 0.7, lw=4.5,label="foc. - w/o enum.")
	handle_foc_enum, = ax[num].plot(x, np.array(foc_enum)/1000,'forestgreen',linestyle="-", alpha = 0.8, lw=4.5,label="foc. - w/ enum.")


ax[1].set_xlabel('sample size'+ r"$= 10^3X$", fontsize=44)
ax[0].set_ylabel('runtime in ms'+  r"$= 10^3Y$" , fontsize=44)

plt.ylim(-0.2,4.5)
ax[0].set_xlim(-0.2, 10.2)
ax[1].set_xlim(-0.2, 10.2)
ax[2].set_xlim(-0.2, 10.2)


xticks = [1+i*1 for i in range(5)]

plt.sca(ax[0])
plt.xticks([0, 2,4, 6, 8, 10], ["1", "3", "5", "7", "9", "11"])
plt.sca(ax[1])
plt.xticks([ 2,4, 6, 8, 10], [ "3", "5", "7", "9", "11"])
plt.sca(ax[2])
plt.xticks([ 2,4, 6, 8, 10], [ "3", "5", "7", "9", "11"])


leg = ax[0].legend(handles = [handle_traditional, handle_trad_reuse_tids],fontsize=44,handlelength=1.2, loc="upper center") 

leg.get_lines()[0].set_linewidth(3.5)
leg.get_lines()[1].set_linewidth(6)

leg = ax[1].legend(handles = [handle_foc_no_enum, handle_foc_enum],fontsize=44,handlelength=1.2, loc="upper left") 
leg.get_lines()[0].set_linewidth(6)
leg.get_lines()[1].set_linewidth(6)

 
ax[0].tick_params(axis='both', labelsize=36)
ax[1].tick_params(axis='both', labelsize=36)
ax[2].tick_params(axis='both', labelsize=36)
ax[0].grid(which="both",ls="-",color ="lightgrey")
ax[1].grid(which="both",ls="-",color ="lightgrey")
ax[2].grid(which="both",ls="-",color ="lightgrey")

ax[0].set_title("3 predicates", fontsize=48)
ax[1].set_title("5 predicates", fontsize=48)
ax[2].set_title("7 predicates", fontsize=48)

fig.tight_layout() 
plt.savefig("focused_sampling_forest.pdf", bbox_inches='tight', transparent=False)
plt.show()



