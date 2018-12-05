#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 12:54:53 2018

@author: lorenzo

questo plto manc a1urn che viene -infintio

ps:(0.1,0.2,0.3) è un bel colore

aggiunta funzionalità per calcolare scatterplots coi nuovi nuovi folding rates

23/11 aggiunto valore di gc calcolato da me: lo chiamo gcc (come 'Gc calcolato')
la nomenclatura si sta facendo confuzionaria in questo file

5/12 LINE 87: CAMBIATO file folding_rates con folding_rates3
    salva il plot direttamente in locale
    v2: aggiunti folding rates ancora diversi (vedi log, guarda come correla)
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%%
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
baiesi_folding_rate = [float(dato) for dato in data]
baiesi_folding_rate[1] = -1.47
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
observed_ln_freq=pd.Series(data=baiesi_folding_rate, index = baiesi_index).sort_index()
print(len(observed_ln_freq))
#%%
########################
# estimated folding rates (now called efolding frequency):

f=open("/home/lorenzo.signorini/tirocinio/log/folding_rates3")
estimated_ln_freq=f.readlines()
f.close()
n=0
estim_index=[]
estim_data=[]
for line in estimated_ln_freq:
    if n<1:
        n+=1
    if n>=1:
        estim_index.append(line.split()[0])
        estim_data.append(round(float(line.split()[3]), 3))
estimated_ln_freq=pd.Series(data=estim_data, index=estim_index).sort_index()


print(estimated_ln_freq)    
#%% nuovo modo:
p=[-2.221, -2.737, -0.747, -1.017, -2.409, -1.834, -0.35, -1.716, -0.571, -0.591, -0.488, -0.191, -0.469, -1.244, -1.734, -1.898, -2.13, -0.766, -1.681, 2.867, -0.767, -0.193, -0.043, -0.711, -0.378, -0.433]
estimated_ln_fr = pd.Series(p, index=FR_index)
print(estimated_ln_fr)
print(p)

#%%
################################
# real estimated FR using MEDIAN
#
#       WARNING: 
#         IN LINE 107 (f = open("/home/lo.../log/*_folding_rates_highest_benc", "r"))
#    IF CALCULATING WITH MEAN: USE FILE 'real_folding_rates_highest_bench'
#    IF CALCULATING WITH MEDIAN: USE FILE 'MEDIAN_real_folding_rates_highest_bench'

f=open("/home/lorenzo.signorini/tirocinio/log/median_real_folding_rates_highest_bench", "r")
median_estimated_ln_FR=f.readlines()
f.close()
FR_index=[]
FR_data=[]
for line in median_estimated_ln_FR:
    if line.startswith("#"):
        continue
    else:
        FR_index.append(line.split("\t\t")[0])
        FR_data.append(round(float(line.split()[3]), 3))
median_estimated_ln_FR=pd.Series(data=FR_data, index=FR_index).sort_index()
################################
# real estimated FR using MEAN

f=open("/home/lorenzo.signorini/tirocinio/log/real_folding_rates_highest_bench", "r")
mean_estimated_ln_FR=f.readlines()
f.close()
FR_index=[]
FR_data=[]
for line in mean_estimated_ln_FR:
    if line.startswith("#"):
        continue
    else:
        FR_index.append(line.split("\t\t")[0])
        FR_data.append(round(float(line.split()[3]), 3))
mean_estimated_ln_FR=pd.Series(data=FR_data, index=FR_index).sort_index()
print(mean_estimated_ln_FR, mean_estimated_ln_FR.shape)
#%%
###################
# topological coso:
topo = pd.Series([0.77,1.62,0.27,0.27,0.47,0.4,0.84,0.96,0.56,0.54,0.5,0.3,0.39,0.49,0.47,0.71,0.67,0.61,0.47,1.15,0.72,0.33,0.6,0.68,0.3,0.86], index=median_estimated_ln_FR.index).to_frame()
#####################
# calculated Gc: gcc
gcc = pd.Series([0.707, 1.487, 0.237, 0.256, 0.429, 0.384, 0.744, 0.839, 0.429, 0.509, 0.414, 0.29, 0.327, 0.439, 0.392, 0.654, 0.593, 0.527, 0.41, 1.038, 0.59, 0.313, 0.502, 0.588, 0.293, 0.55], index=median_estimated_ln_FR.index).to_frame()
#%%   merge series in dataframes

# 1estimated folding  frequency
est_vs_obs_ln_freq = estimated_ln_freq.to_frame() # la x
est_vs_obs_ln_freq = est_vs_obs_ln_freq.merge(observed_ln_freq.to_frame(), right_index=True, left_index=True) #la y

est_freq_vs_topo = estimated_ln_freq.to_frame()
est_freq_vs_topo = est_freq_vs_topo.merge(topo, right_index=True, left_index=True)

est_freq_vs_gcc = estimated_ln_freq.to_frame()
est_freq_vs_gcc = est_freq_vs_gcc.merge(gcc, right_index=True, left_index=True)
#%%
#2 estimated folding rate (mean method)
mean_est_vs_obs_FR = mean_estimated_ln_FR.to_frame()
mean_est_vs_obs_FR = mean_est_vs_obs_FR.merge(observed_ln_freq.to_frame(), right_index=True, left_index=True)

mean_real_FR_vs_topo = mean_estimated_ln_FR.to_frame()
mean_real_FR_vs_topo = mean_real_FR_vs_topo.merge(topo, right_index=True, left_index=True)

mean_real_FR_vs_gcc = mean_estimated_ln_FR.to_frame()
mean_real_FR_vs_gcc = mean_real_FR_vs_gcc.merge(topo, right_index=True, left_index=True)
#%%
#3 estimated folding rate (median method)
median_est_vs_obs_FR = median_estimated_ln_FR.to_frame()
median_est_vs_obs_FR = median_est_vs_obs_FR.merge(observed_ln_freq.to_frame(), right_index=True, left_index=True)

median_real_FR_vs_topo = median_estimated_ln_FR.to_frame()
median_real_FR_vs_topo = median_real_FR_vs_topo.merge(topo, right_index=True, left_index=True)

median_real_FR_vs_gcc = median_estimated_ln_FR.to_frame()
median_real_FR_vs_gcc = median_real_FR_vs_gcc.merge(gcc, right_index=True, left_index=True)

#%%  gcc vs topo
gc_v_topo = gcc.merge(topo, right_index=True, left_index=True)
#%%
### plots

np.random.seed(123456)
random_colors = [(np.random.uniform(), np.random.uniform(), np.random.uniform()) for i in range(30)]

markers =  [(np.random.randint(3,7), np.random.randint(0,3), 0) for marker in range(30)]
#%%
#plt.style.use('_classic_test')
#plt.rcParams te li mostra tti
for (dataset, x, y) in [(est_vs_obs_ln_freq , "ln($F$)", "ln($F_{exp}$)"), (est_freq_vs_topo, "ln($F$)", "$|G'|_c$ (as in Baiesi et al., 2017)"),  (est_freq_vs_gcc, "ln($F$)", "$<|G'|_c>$"), (mean_est_vs_obs_FR, "ln($\\bar{R}$)", "ln($F_{exp}$)"),    (mean_real_FR_vs_topo, "ln($\\bar{R}$)" , "$|G'|_c$ (as in Baiesi et al., 2017)"),    (mean_real_FR_vs_gcc, "ln($\\bar{R}$)", "$<|G'|_c>$"), (median_est_vs_obs_FR, "ln($\\widetilde{R}$)", "ln($F_{exp}$)"),    (median_real_FR_vs_topo,"ln($\\widetilde{R}$)", "$|G'|_c$ (as in Baiesi et al., 2017)"), (median_real_FR_vs_gcc, "ln($\\widetilde{R}$)", "$<|G'|_c>$"), (gc_v_topo,"$<|G'|_c>$","$|G'|_c$ (as in Baiesi et al., 2017)")]:
    fig, ax = plt.subplots()

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

    i=0
    for protein, row in dataset.iterrows():  #cambia qui, poi la riga sotto, e poi il nome del grafico
        ax.plot(row[0], row[1], linestyle='', marker= markers[i], ms=6, label=protein, color = random_colors[i])  # color = colors_of[protein], marker="o"
        i+=1 # this index is used for the colors
            
    # add labels, legend, other stuff
    ax.set_position([0.1,0.2,0.4,0.7])
    plt.ylabel(y)
    plt.xlabel(x)
    ax.legend(ncol=2, bbox_to_anchor=(2.2, 1), shadow= True, numpoints = 1) # numpoints = 1 sono il numero di punti per ogni item della legenda. se no me ne metteva due pallini invece che uno. nosense, ma vbb
    ax.grid()
    
    # determine correlation:
    # this is somewhat ambiguous, becuase of the usual -inf datum. I choose to not take it into acocunt
    corcoeff=np.corrcoef(np.array(dataset['0_x']), np.array(dataset['0_y']))[1][0]        
    line="Pearson's Correlation coefficient: " + str(round(corcoeff, 3))
    print(line)
    fig.text(0.5,0.1, line)
#    
    name = x +"vs"+y+".pdf"
    plt.savefig("/home/lorenzo/tirocinio/tesi/analyses/collective_analyses/"+name)    #WARNING : CHANGE QUI IL NOME DEL FILE DI OUTPUT!! ATTENTO A NON SOVRASCRIVERE NULLA!
    plt.close()
#%% e  i topo che me li so scordati
    
fig, ax = plt.subplots()

i=0
for protein, row in gc_v_topo.iterrows():  #cambia qui, poi la riga sotto, e poi il nome del grafico
    ax.plot(row[0], row[1], linestyle='', marker= markers[i], ms=6, label=protein, color = random_colors[i])  # color = colors_of[protein], marker="o"
    i+=1 # this index is used for the colors
ax.set_position([0.1,0.2,0.4,0.7])
plt.ylabel("$|G'|_c$ (as in Baiesi et al., 2017)")
plt.xlabel("$<|G'|_c$>")
ax.legend(ncol=2, bbox_to_anchor=(2.2, 1), shadow= True, numpoints = 1) # numpoints = 1 sono il numero di punti per ogni item della legenda. se no me ne metteva due pallini invece che uno. nosense, ma vbb
ax.grid()
plt.xlim(0,1.8)
plt.ylim(0,1.8)

# determine correlation:
# this is somewhat ambiguous, becuase of the usual -inf datum. I choose to not take it into acocunt

#corcoeff=np.corrcoef(np.array(gc_v_topo['0_x'].drop(['1urn'])), np.array(gc_v_topo['0_y'].drop(['1urn'])))[1][0]    # aggiungi .drop(['1urn']) a entrami , per droppare 1urn, SOLO nel caso tu stia calcolando le folding_frequencies (estimated_folding_rates vecchi, il primissimo coso)

corcoeff=np.corrcoef(np.array(gc_v_topo['0_x']), np.array(gc_v_topo['0_y']))[1][0]        
line="Pearson's Correlation coefficient: " + str(round(corcoeff, 3))
fig.text(0.5,0.1, line)

name = "temp.pdf"
plt.plot(np.linspace(-0.1,gc_v_topo.max()[1]+0.2,100),np.linspace(-0.1,gc_v_topo.max()[1]+0.2,100), color= "0.5", linewidth=0.8, linestyle='dashed')
#plt.show()
plt.savefig("/home/lorenzo/tirocinio/tesi/analyses/collective_analyses/"+name)    #WARNING : CHANGE QUI IL NOME DEL FILE DI OUTPUT!! ATTENTO A NON SOVRASCRIVERE NULLA!
plt.close()
