#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 15/02/2019
@author: lorenzo

questo plto manc a1urn che viene -infintio

ps:(0.1,0.2,0.3) è un bel colore

aggiunta funzionalità per calcolare scatterplots coi nuovi nuovi folding rates

23/11 aggiunto valore di gc calcolato da me: lo chiamo gcc (come 'Gc calcolato')
la nomenclatura si sta facendo confuzionaria in questo file

5/12 LINE 87: CAMBIATO file folding_rates con folding_rates3
    salva il plot direttamente in locale
    v2: aggiunti folding rates ancora diversi (vedi log, guarda come correla)

15/02/2019
    versione con i nuovi dati dopo l´ottimizzazione
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#%% OPTIMIZATION FOLDING RATES

ffreq_optimization =pd.Series({"1aps":0.411670691,"1bzp":0.955675397,"1fkb":0.678795108,"1hrc":0.936458749,"1ubq":0.916828216,"1urn":0.395686832,"2ci2":0.968503251, "2abd":0.981407616})
ln_ffreq_optimization = np.log(ffreq_optimization)
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
#%% NEW DATA from optimized FF runs: NEW FOLDING FREQUENCIES

f=open("/data/isilon/signorini/da/folding_stats.dat")
lines=f.readlines()
f.close()
n=0
estim_index_equi=[]
estim_index_old=[]
estim_index_msd=[]
ln_ffreq_new_equi=[]
ln_ffreq_new_old=[]
ln_ffreq_new_msd=[]
ffreq_new_equi = []   # questi 3 variano in base a come calcoli  il threshold per lrmsd (vedi efr4_forcluster.py)
ffreq_new_old = []
ffreq_new_msd = []

mean_time_new_old = []
mean_rate_new_old = []
ln_mean_rate_new_old = []
median_time_new_old = []
median_rate_new_old = []
ln_median_rate_new_old = []

for line in lines:
    if n<3:
        n+=1
    if n>=3:        
        print(line.split())
        thr=line.split()[1]
        if thr.startswith("equi"): 
            estim_index_equi.append(line.split()[0][:4])
            ln_ffreq_new_equi.append(str(round(float(line.split()[4]), 3)))
            ffreq_new_equi.append(round(float(line.split()[3]), 3)) 

        elif thr.startswith("old"): 
            estim_index_old.append(line.split()[0][:4])
            ln_ffreq_new_old.append(round(float(line.split()[4]), 3))
            ffreq_new_old.append(round(float(line.split()[3]), 3)) 
            
            mean_time_new_old.append(round(float(line.split()[3]), 3)) 
            mean_rate_new_old.append(round(float(line.split()[6]), 3))
            ln_mean_rate_new_old.append(round(float(line.split()[7]), 3))
            median_time_new_old.append(round(float(line.split()[8]), 3))    
            median_rate_new_old.append(round(float(line.split()[9]), 3))
            ln_median_rate_new_old.append(round(float(line.split()[10]), 3))

        elif thr.startswith("msd"): 
            estim_index_msd.append(line.split()[0][:4])
            ln_ffreq_new_msd.append(round(float(line.split()[4]), 3))
            ffreq_new_msd.append(round(float(line.split()[3]), 3)) 
            
ln_ffreq_new_equi=pd.Series(data=ln_ffreq_new_equi, index=estim_index_equi).sort_index()
ln_ffreq_new_old=pd.Series(data=ln_ffreq_new_old, index=estim_index_old).sort_index()
ln_ffreq_new_msd=pd.Series(data=ln_ffreq_new_msd, index=estim_index_msd).sort_index()

ffreq_new_equi=pd.Series(data=ffreq_new_equi, index=estim_index_equi).sort_index()
ffreq_new_old=pd.Series(data=ffreq_new_old, index=estim_index_old).sort_index()
ffreq_new_msd=pd.Series(data=ffreq_new_msd, index=estim_index_msd).sort_index()

mean_time_new_old = pd.Series(data=mean_time_new_old, index=estim_index_old).sort_index()
mean_rate_new_old = pd.Series(data=mean_rate_new_old, index=estim_index_old).sort_index()
ln_mean_rate_new_old = pd.Series(data=ln_mean_rate_new_old, index=estim_index_old).sort_index()
median_time_new_old = pd.Series(data=median_time_new_old, index=estim_index_old).sort_index()
median_rate_new_old = pd.Series(data=median_rate_new_old, index=estim_index_old).sort_index()
ln_median_rate_new_old = pd.Series(data=ln_median_rate_new_old, index=estim_index_old).sort_index()


print(mean_time_new_old, mean_rate_new_old, ln_mean_rate_new_old)   
#%%
########################
# OLD estimated folding rates (now called efolding frequency):

f=open("/data/isilon/signorini/da/old_log/folding_rates3")

n=0
estim_index=[]
estim_data=[]
ffreq_old = []
for line in f.readlines():
    if n<1:
        n+=1
    if n>=1:
        estim_index.append(line.split()[0])
        estim_data.append(round(float(line.split()[3]), 3))
        ffreq_old.append(round(float(line.split()[2]), 3))

f.close()
ln_ffreq_old=pd.Series(data=estim_data, index=estim_index).sort_index()
ffreq_old=pd.Series(data=ffreq_old, index=estim_index).sort_index()


print(ffreq_old)    

#%% old median and mean stuffs.
################################
# real estimated FR using MEDIAN
#
#       WARNING: 
#         IN LINE 107 (f = open("/home/lo.../log/*_folding_rates_highest_benc", "r"))
#    IF CALCULATING WITH MEAN: USE FILE 'real_folding_rates_highest_bench'
#    IF CALCULATING WITH MEDIAN: USE FILE 'MEDIAN_real_folding_rates_highest_bench'

f=open("/data/isilon/signorini/da/old_log/median_real_folding_rates_highest_bench", "r")

FR_index=[]
FR_data=[]
for line in f.readlines():
    if line.startswith("#"):
        continue
    else:
        FR_index.append(line.split("\t\t")[0])
        FR_data.append(round(float(line.split()[3]), 3))
f.close()
ln_medianFR_old=pd.Series(data=FR_data, index=FR_index).sort_index()
################################
# real estimated FR using MEAN

f=open("/data/isilon/signorini/da/old_log/real_folding_rates_highest_bench", "r")

FR_index=[]
FR_data=[]
for line in f.readlines():
    if line.startswith("#"):
        continue
    else:
        FR_index.append(line.split("\t\t")[0])
        FR_data.append(round(float(line.split()[3]), 3))
f.close()
ln_meanFR_old=pd.Series(data=FR_data, index=FR_index).sort_index()
print(ln_meanFR_old, ln_meanFR_old.shape)
#%%
###################
# topological coso:
topo = pd.Series([0.77,1.62,0.27,0.27,0.47,0.4,0.84,0.96,0.56,0.54,0.5,0.3,0.39,0.49,0.47,0.71,0.67,0.61,0.47,1.15,0.72,0.33,0.6,0.68,0.3,0.86], index=ffreq_old.index).to_frame()
#####################
# calculated Gc: gcc
gcc = pd.Series([0.707, 1.487, 0.237, 0.256, 0.429, 0.384, 0.744, 0.839, 0.429, 0.509, 0.414, 0.29, 0.327, 0.439, 0.392, 0.654, 0.593, 0.527, 0.41, 1.038, 0.59, 0.313, 0.502, 0.588, 0.293, 0.55], index=ffreq_old.index).to_frame()
#%% CUT NEEDED DF ACCORDING TO NEW INDEXES THAT YOU HAVEopti_est_freq_vs_topo
# ONLY DO THIS PER ORA CHE NON HAI TUTTE LE PROTEINE SU
ffreq_old = pd.Series(data= [ffreq_old[i] for i in ffreq_new_old.index], index=ffreq_new_old.index)
ln_ffreq_old = pd.Series(data= [ln_ffreq_old[i] for i in ffreq_new_old.index], index=ffreq_new_old.index)

print(ffreq_old, ln_ffreq_old)


#%%   NEW GRAPHS CON LE NUOVE VARIABBOLS  ffreq_new
ffreq_old_vs_new = ffreq_old.to_frame()
ffreq_old_vs_new = ffreq_old_vs_new.merge(ffreq_new_old.to_frame(), right_index=True, left_index=True)

ln_ffreq_old_vs_new = ln_ffreq_old.to_frame()
ln_ffreq_old_vs_new = ln_ffreq_old_vs_new.merge(ln_ffreq_new_old.to_frame(), right_index=True, left_index=True)

# 1. ffreq_new CONTRO I TRE COSi
est_vs_obs_ln_freq = ln_ffreq_new_old.to_frame() # la x
est_vs_obs_ln_freq = est_vs_obs_ln_freq.merge(observed_ln_freq.to_frame(), right_index=True, left_index=True) #la y

est_freq_vs_topo = ln_ffreq_new_old.to_frame()
est_freq_vs_topo = est_freq_vs_topo.merge(topo, right_index=True, left_index=True)

est_freq_vs_gcc = ln_ffreq_new_old.to_frame()
est_freq_vs_gcc = est_freq_vs_gcc.merge(gcc, right_index=True, left_index=True)
#%%
# 2. ln(mean_rate)_new CONTRO I TRE COSI
ln_meanFR_vs_obs_FR = ln_mean_rate_new_old.to_frame()
ln_meanFR_vs_obs_FR = ln_meanFR_vs_obs_FR.merge(observed_ln_freq.to_frame(), right_index=True, left_index=True)

ln_meanFR_vs_topo = ln_mean_rate_new_old.to_frame()
ln_meanFR_vs_topo = ln_meanFR_vs_topo.merge(topo, right_index=True, left_index=True)

ln_meanFR_vs_gcc = ln_mean_rate_new_old.to_frame()
ln_meanFR_vs_gcc = ln_meanFR_vs_gcc.merge(gcc, right_index=True, left_index=True)

# 3. ln(median_rate)_new contro i tre cosi
ln_medianFR_vs_obs_FR = ln_median_rate_new_old.to_frame()
ln_medianFR_vs_obs_FR = ln_medianFR_vs_obs_FR.merge(observed_ln_freq.to_frame(), right_index=True, left_index=True).dropna()

ln_medianFR_vs_topo = ln_median_rate_new_old.to_frame()
ln_medianFR_vs_topo = ln_medianFR_vs_topo.merge(gcc, right_index=True, left_index=True).dropna()

ln_medianFR_vs_gcc = ln_median_rate_new_old.to_frame()
ln_medianFR_vs_gcc = ln_medianFR_vs_gcc.merge(gcc, right_index=True, left_index=True).dropna()
#%%
# NUOVO RISPETTO A TESI: mean_time, median_time, mean_rate, median_rate rispetto ai tre cosi
meanFR_vs_obs_FR = mean_rate_new_old.to_frame()
meanFR_vs_obs_FR = meanFR_vs_obs_FR.merge(observed_ln_freq.to_frame(), right_index=True, left_index=True)

meanFR_vs_topo = mean_rate_new_old.to_frame()
meanFR_vs_topo = meanFR_vs_topo.merge(topo, right_index=True, left_index=True)

meanFR_vs_gcc = mean_rate_new_old.to_frame()
meanFR_vs_gcc = meanFR_vs_gcc.merge(gcc, right_index=True, left_index=True)

# 3. ln(median_rate)_new contro i tre cosi
medianFR_vs_obs_FR = median_rate_new_old.to_frame()
medianFR_vs_obs_FR = medianFR_vs_obs_FR.merge(observed_ln_freq.to_frame(), right_index=True, left_index=True)

medianFR_vs_topo = median_rate_new_old.to_frame()
medianFR_vs_topo = medianFR_vs_topo.merge(gcc, right_index=True, left_index=True).dropna()

medianFR_vs_gcc = median_rate_new_old.to_frame()
medianFR_vs_gcc = medianFR_vs_gcc.merge(gcc, right_index=True, left_index=True)


#%% NEW GRAPHS FFREQ CON QUELLi secchi dei 16 forcefields  DELL OPTIMIZATION

ffreq_old_vs_new = ffreq_old.to_frame()
ffreq_old_vs_new = ffreq_old_vs_new.merge(ffreq_optimization.to_frame(), right_index=True, left_index=True)

ln_ffreq_old_vs_new = ln_ffreq_old.to_frame()
ln_ffreq_old_vs_new = ln_ffreq_old_vs_new.merge(ln_ffreq_optimization.to_frame(), right_index=True, left_index=True)

# 1. ffreq_new CONTRO I TRE COSi
opt_est_vs_obs_ln_freq = ln_ffreq_optimization.to_frame() # la x
opt_est_vs_obs_ln_freq = opt_est_vs_obs_ln_freq.merge(observed_ln_freq.to_frame(), right_index=True, left_index=True) #la y

opt_est_freq_vs_topo = ln_ffreq_optimization.to_frame()
opt_est_freq_vs_topo = opt_est_freq_vs_topo.merge(topo, right_index=True, left_index=True)

opt_est_freq_vs_gcc = ln_ffreq_optimization.to_frame()
opt_est_freq_vs_gcc = opt_est_freq_vs_gcc.merge(gcc, right_index=True, left_index=True)

#%%
### plots

np.random.seed(123456)
random_colors = [(np.random.uniform(), np.random.uniform(), np.random.uniform()) for i in range(30)]

markers =  [(np.random.randint(3,7), np.random.randint(0,3), 0) for marker in range(30)]    

#%% PLOTTER GENERALE PER UN DATASET SOLO

# 1 select dataset to use, and relative labels for axes
all_mean_median_datasets = [(ln_meanFR_vs_obs_FR , "ln($\\bar{R}$)", "ln($F_{exp}$)", "ln_meanFR_vs_obs_FR.png"),\
                            (ln_meanFR_vs_topo, "ln($\\bar{R}$)" , "$|G'|_c$ (as in Baiesi et al., 2017)","ln_meanFR_vs_topo.png"),\
                            (ln_meanFR_vs_gcc, "ln($\\bar{R}$)", "$<|G'|_c>$","ln_meanFR_vs_gcc.png"),\
                            (ln_medianFR_vs_obs_FR , "ln($\\widetilde{R}$)", "ln($F_{exp}$)", "ln_medianFR_vs_obs_FR.png"),\
                            (ln_medianFR_vs_topo, "ln($\\widetilde{R}$)" , "$|G'|_c$ (as in Baiesi et al., 2017)","ln_medianFR_vs_topo.png"),\
                            (ln_medianFR_vs_gcc, "ln($\\widetilde{R}$)", "$<|G'|_c>$","ln_medianFR_vs_gcc.png"),\
                            
                            
        
        ] 
# est_vs_obs_ln_freq , "ln($F$)", "ln($F_{exp}$)", "est_vs_obs_ln_freq.png"

# est_freq_vs_topo, "ln($F$)", "$|G'|_c$ (as in Baiesi et al., 2017)", "est_freq_vs_topo.png"
#  est_freq_vs_gcc, "ln($F$)", "$<|G'|_c>$", "est_freq_vs_gcc.png"


#dataset, x ,y, name = est_freq_vs_gcc.drop(['1urn']), "ln($F$)", "$<|G'|_c>$", "opt_est_freq_vs_gcc.png"  # .drop(['1urn'])

for dataset, x, y, name in all_mean_median_datasets:

    # 2 Plot them
    fig, ax = plt.subplots()
    
    i=0
    for protein, row in dataset.iterrows():  #cambia qui, poi la riga sotto, e poi il nome del grafico
        ax.plot(row[0], row[1], linestyle='', marker= markers[i], ms=6, label=protein, color = random_colors[i])  # color = colors_of[protein], marker="o"
        i+=1 # this index is used for the colors
    ax.set_position([0.1,0.2,0.4,0.7])
    plt.ylabel(y)
    plt.xlabel(x)   
    ax.legend(ncol=2, bbox_to_anchor=(2.2, 1), shadow= True, numpoints = 1) # numpoints = 1 sono il numero di punti per ogni item della legenda. se no me ne metteva due pallini invece che uno. nosense, ma vbb
    ax.grid()
    #plt.xlim(0,1.8)
    #plt.ylim(0,1.8)
    ffreq_old=ffreq_old.sub(ffreq_new_old).dropna()
    
    # determine correlation:
    # this is somewhat ambiguous, becuase of the usual -inf datum. I choose to not take it into acocunt
    
    corcoeff=np.corrcoef(np.array(dataset['0_x']), np.array(dataset['0_y']))[1][0]        
    line="Pearson's Correlation coefficient: " + str(round(corcoeff, 3))
    fig.text(0.5,0.1, line)
    
    #bisect=np.linspace(-5,ffreq_old_vs_new.max()[1]+0.2,200)
    #plt.plot(bisect,bisect, color= "0.5", linewidth=0.8, linestyle='dashed')
    plt.show()
    #plt.savefig("/data/isilon/signorini/da/correlations/"+name)    #WARNING : CHANGE QUI IL NOME DEL FILE DI OUTPUT!! ATTENTO A NON SOVRASCRIVERE NULLA!
    plt.close()