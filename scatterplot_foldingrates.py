#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 12:54:53 2018

@author: lorenzo

questo plto manc a1urn che viene -infintio

ps:(0.1,0.2,0.3) è un bel colore

aggiunta funzionalità per calcolare scatterplots coi nuovi nuovi folding rates
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


data = """0.6
1.47
6.63
6.95
11.12
6.54
6.61
1.38
8.75
4.1
7.28
11.01
5.66
2.69
1.17
4.54
1.06
3.48
7.35
2.5
0.41
12.2
6.56
4.03
9.67
7.48"""
data = data.split()
baiesi_data = [float(dato) for dato in data]
baiesi_data[1] = -1.47
baiesi_index = """1afi
1aps
1aye
1bnz_a
1bzp
1csp
1div.n
1fkb
1hrc
1hz6_a
1imq
1lmb3
1pgb
1poh
1psf
1shf_a
1ten
1tit
1ubq
1urn
1wit
256b
2abd
2ci2
2pdd
2vik""".split()
observed_ln_freq=pd.Series(data=baiesi_data, index = baiesi_index).sort_index()
print(len(observed_ln_freq))

########################
# estimated folding rates (now called efolding frequency):

f=open("/home/lorenzo.signorini/tirocinio/log/folding_rates")
estimated_ln_freq=f.readlines()
f.close()
n=0
estim_index=[]
estim_data=[]
for line in estimated_ln_freq:
    if n<3:
        n+=1
    if n>=3:
        estim_index.append(line.split()[0])
        estim_data.append(round(float(line.split()[3]), 3))
estimated_ln_freq=pd.Series(data=estim_data, index=estim_index).sort_index()

print(estimated_ln_freq)    



################################
# real estimated FR:
#
#       WARNING: 
#         IN LINE 107 (f = open("/home/lo.../log/*_folding_rates_highest_benc", "r"))
#    IF CALCULATING WITH MEAN: USE FILE 'real_folding_rates_highest_bench'
#    IF CALCULATING WITH MEDIAN: USE FILE 'MEDIAN_real_folding_rates_highest_bench'

f=open("/home/lorenzo.signorini/tirocinio/log/median_real_folding_rates_highest_bench", "r")
estimated_ln_FR=f.readlines()
f.close()
FR_index=[]
FR_data=[]
for line in estimated_ln_FR:
    if line.startswith("#"):
        continue
    else:
        FR_index.append(line.split("\t\t")[0])
        FR_data.append(round(float(line.split()[3]), 3))
estimated_ln_FR=pd.Series(data=FR_data, index=FR_index).sort_index()


###################
# topological coso:
topo = pd.Series([0.77,1.62,0.27,0.27,0.47,0.4,0.84,0.96,0.56,0.54,0.5,0.3,0.39,0.49,0.47,0.71,0.67,0.61,0.47,1.15,0.72,0.33,0.6,0.68,0.3,0.86], index=estimated_ln_FR.index).to_frame()
 
                 
# merge series in dataframe
ln_frequencies = estimated_ln_freq.to_frame() # la x
ln_frequencies = ln_frequencies.merge(observed_ln_freq.to_frame(), right_index=True, left_index=True) #la y

est_freq_vs_topo = estimated_ln_freq.to_frame()
est_freq_vs_topo = est_freq_vs_topo.merge(topo, right_index=True, left_index=True)

est_vs_obs_FR = estimated_ln_FR.to_frame()
est_vs_obs_FR = est_vs_obs_FR.merge(observed_ln_freq, right_index=True, left_index=True)

real_FR_vs_topo = estimated_ln_FR.to_frame()
real_FR_vs_topo = real_FR_vs_topo.merge(topo, right_index=True, left_index=True)

##############################
### plot

#plt.style.use('_classic_test')
#plt.rcParams te li mostra tti

fig, ax = plt.subplots()

# create a lst of 26 random colors
random_colors = [(np.random.uniform(), np.random.uniform(), np.random.uniform()) for i in range(30)]

#or:
# color plot by length:

#     1 order proteins from the shortest to the longest:
#
#length_of = {'1afi':72,'1aps':98, '1aye':80, '1bnz_a':64, '1bzp':153, '1csp':67,
#'1div.n':56, '1fkb':107, '1hrc':104,'1hz6_a':62, '1imq':86, '1lmb3':80,'1pgb':56,'1poh':85,'1psf':69,'1shf_a':59,'1ten':89,'1tit':89,'1ubq':76,'1urn':96, '1wit':93,'256b':106,'2abd':86,'2ci2':64,'2pdd':41, '2vik':126}
##     2 create color mapping
#
#cmap= plt.get_cmap('Reds')
#colors_of = { protein:cmap(np.e**(protein_length)) for protein,protein_length in length_of.items()} # crea dizionario che mappa nomi di proteine a un colore formato RGB nella cmap desiderata 


# create plot
    # o così
i=0
for protein, row in est_freq_vs_topo.iterrows():  #cambia qui, poi la riga sotto, e poi il nome del grafico
    ax.plot(row[0], row[1], linestyle='', marker=(np.random.randint(3,7), np.random.randint(0,3), 0) ,ms=6, label=protein, color = random_colors[i])  # color = colors_of[protein], marker="o"
    i+=1 # this index is used for the colors
    
    # oppure: fai:
#plt.scatter(est_freq_vs_topo['0_x'],est_freq_vs_topo['0_y'])

# add labels, legend, other stuff
ax.set_position([0.1,0.2,0.4,0.7])
plt.ylabel("Observed ln(Folding Rate)")
plt.xlabel("Estimated ln(Folding Rate)")
ax.legend(ncol=2, bbox_to_anchor=(2.2, 1), shadow= True, numpoints = 1) # numpoints = 1 sono il numero di punti per ogni item della legenda. se no me ne metteva due pallini invece che uno. nosense, ma vbb
ax.grid()

# determine correlation:
# this is somewhat ambiguous, becuase of the usual -inf datum. I choose to not take it into acocunt

corcoeff=np.corrcoef(np.array(est_freq_vs_topo['0_x'].drop(['1urn'])), np.array(est_freq_vs_topo['0_y'].drop(['1urn'])))[1][0]    # aggiungi .drop(['1urn']) a entrami , per droppare 1urn, SOLO nel caso tu stia calcolando le folding_frequencies (estimated_folding_rates vecchi, il primissimo coso)
line="Pearson's Correlation coefficient: " + str(round(corcoeff, 3))
fig.text(0.5,0.1, line)

plt.savefig("/home/lorenzo.signorini/tirocinio/analyses/scatterplot_temp_ff_vs_topo_CC_hb.pdf")    #WARNING : CHANGE QUI IL NOME DEL FILE DI OUTPUT!! ATTENTO A NON SOVRASCRIVERE NULLA!
plt.close()
