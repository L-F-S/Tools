#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 14:08:57 2018

@author: lorenzo

scatterplot, mean, max, min, var, and outlyers greater than 2sigma, for
the G value of the readchain1 simulation(s) of every protein

"""

import matplotlib.pyplot as plt
import pandas  as pd
import numpy as np
import os

#%%
# prova for single protein:

def scatter_altro(protein):
# funzione definita per fare gli scatter sulle run mergiate di proteine con più runu a rc1
    df = pd.read_csv("/home/lorenzo.signorini/tirocinio/temp/r1/G_"+protein+"_rc1_"+"m.dat", sep ="\t", header= None)
#TODO : AGGIUNGERE UNITA DI MISURA TIMESTEP
    plt.figure()
    plt.scatter(df[0],df[1], facecolors = 'gray', color='black', s = 1)
    plt.xticks(fontsize = 8)
    plt.xlabel("timestep")  # IN CHE UNIT??
    plt.ylabel("|G'c|")
    plt.savefig("/home/lorenzo.signorini/tirocinio/analyses/"+protein+"/G_"+protein+"_m.pdf")
    plt.close()
    
    plt.figure()
    plt.hist(df[1], color='black', bins = 40, weights=np.ones_like(df[1])/float(len(df[1])))
    plt.xticks(fontsize = 8)
    plt.xlabel("|G'c|")
    plt.savefig("/home/lorenzo.signorini/tirocinio/analyses/"+protein+"/G_hist"+protein+"_m.pdf")
    plt.close()
    return df

def scatter_of(protein,run):

    df = pd.read_csv("/home/lorenzo.signorini/tirocinio/temp/r1/G_"+protein+"_rc1_"+run+"_0.dat", sep ="\t", header= None)
#TODO : AGGIUNGERE UNITA DI MISURA TIMESTEP
#    plt.figure()
#    plt.scatter(df[0],df[1], facecolors = 'gray', color='black', s = 1)
#    plt.xticks(fontsize = 8)
#    plt.xlabel("timestep")  # IN CHE UNIT??
#    plt.ylabel("|G'c|")
#    plt.savefig("/home/lorenzo.signorini/tirocinio/analyses/"+protein+"/G_"+protein+"_"+run+".pdf")
#    plt.close()
    
    plt.figure()
    plt.hist(df[1], color='black', bins = 40, weights=np.ones_like(df[1])/float(len(df[1])))
    plt.xticks(fontsize = 8)
    plt.xlabel("|G'c|")
    plt.savefig("/home/lorenzo.signorini/tirocinio/analyses/"+protein+"/G_hist"+protein+"_"+run+".pdf")
    plt.close()
    return df

#%%
def find_outlyers(protein, run, df):
    print(df[1].max(), df[1].min(),df[1].mean(), df[1].std())
#    f=open("/home/lorenzo.signorini/tirocinio/analyses/"+protein+"/G_"+protein+"_"+run+"r1_out")
#    header = "# G values for readchain1 simulation of protein " + protein+"\n"
#    cols= "# max\tmin\tmean\tvariance\tN samples"
#    data
# controlla outòliers (RMSD, come sono fatti)
    return
#%%
def main():
    
    g_folder = "/home/lorenzo.signorini/tirocinio/temp/r1"  # da cambiare 
    os.chdir(g_folder)
    double = True
    proteins = ['1afi', '1aps', '1bnz_a', '1bzp', '1csp', '1fkb', '1hrc', '1imq', '1pgb', '1poh', '1psf']#['1afi', '1aps', '1aye', '1bnz_a', '1bzp', '1csp', '1div.n', '1fkb', '1hrc', '1hz6_a', '1imq', '1lmb3', '1pgb', '1poh', '1psf', '1shf_a', '1ten', '1tit', '1ubq', '1urn', '1wit', '2abd', '2ci2', '2pdd', '2vik', '256b']
    for g in os.listdir():
        if g.startswith("G"):
            if double == True:
                if g.endswith('m.dat'):
                    for protein in proteins:
                    # è una traiettoria di G. che proteina?
                        if g.lstrip("G_").startswith(protein):
                             print(protein)
                             df = scatter_altro(protein)
#                             find_outlyers(protein, run, df)                   
                    
            else:
                for protein in proteins:
                # è una traiettoria di G. che proteina?
                    if g.lstrip("G_").startswith(protein):
                         print(protein)
                         tbls1="G_" 
                         tbls2 = protein + "_"
                         tbls3="rc1"
                         tbls4="_"
                         tbrs = "0.dat"
                         tbrs2 = "_"
                         run = g.rstrip(tbrs).rstrip(tbrs2).lstrip(tbls1).lstrip(tbls2).lstrip(tbls3).lstrip(tbls4)
                         if not run.startswith('r'):
                             run = 'r' +run
                         print(run)
                         df = scatter_of(protein, run)
                         find_outlyers(protein, run, df)                   
                     
    return

main()
#%%