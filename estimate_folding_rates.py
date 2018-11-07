#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 16:06:52 2018

@author: lorenzo

vesrsion 2.0
Calculates estimated folding rate of proteins.

what is called 'estimated folding rate' or 'folding rate' here, is now called 'folding frequency'

FOLDING FREQUENCY (ON THIS SCRIPT KNOWN AS FOLDING RATES): ARE DEFINED AS THE FREQUENCY WITH WHICH OUR PROTEINS
FOLD.

what is known here as 'real folding rate' is now simply 'folding rate.


REAL FOLDING RATES (folding rates from now on)
are defined to be FR = 1/mean(#steps_to_f),
were #steps_to_f is the number of steps needed to drop the RMSD <= the equilibrium RMSD

il file avrà 4 colonne:
    1: nome
    2: benchmark_rmsd
    3: folding rate
    4: ln(folding rate)

VERSION 2.0:

UNSUCCESSFUL FOLDINGS ARE NOT TAKEN INTO t.


--------------------------------------------------------
occhio a non confonderti, nulla può andare storto


"""

# todo: folding rates plots, salvateli, e salv alen
import os
import numpy as np
import matplotlib.pyplot as plt

###################################################
#   NEW FUNCTIONS TO CALCUALTE REAL FOLDING RATES #
###################################################

def real_folding_rate(protein, protein_path, benchmark_rmsd):
    print("--------------------------------------------------\n\nCalculating Folding Rate")
    list_of_n_steps= []
    os.chdir(protein_path)
    ##############################
    # LOOP OVER ALL SIMULATIONS
    for direct in os.listdir():
        if direct.startswith("run_"):
            run_number=direct.split("_")[1]
            rmsd=open(protein_path+"/"+direct+"/msd_"+run_number+".dat") 
            for line in rmsd.readlines():
                spl_line=line.split()
                if float(spl_line[1]) <= benchmark_rmsd:
                    list_of_n_steps.append(int(spl_line[0]))
                    break
    print(len(list_of_n_steps))
    plt.hist(list_of_n_steps)    
    #################################
    # CALCULATE REAL FR
    real_FR = 1/np.mean(list_of_n_steps)
    print("and the FR:", real_FR)
    ln_real_folding_rate = np.log(real_FR)
    ################################
    # PRINT INTO FILE
    f=open("/home/lorenzo.signorini/tirocinio/log/real_folding_rates_highest_bench", "a")
    f.write(protein+"\t\t"+str(benchmark_rmsd)+"\t\t"+str(real_FR)+"\t\t"+str(ln_real_folding_rate)+"\n")
    f.close()

    return

###############################################################################

    
    
def benchmark_rmsd(protein, protein_path, method="last"):
    "extracts last line of the msd file in one readchain1 run"
    print("--------------------------------------------------\n\nfinding benchmark")
    os.chdir(protein_path+"/readchain1")
    first_folder = True
    lastline = float   # to be used if method == last
    highestline = 0  # to be used if method == highest
    for folder in os.listdir():
        if first_folder == True:
            first_folder = False
            os.chdir(protein_path+"/readchain1/"+folder)
            for file in os.listdir():
                if file.startswith("msd"):
                    f=open(file)
                    for line in f.readlines():
                        lastline=line
                        if float(line.split()[1]) > highestline:
                                 highestline = float(line.split()[1])
                    f.close()
    if method =="last":
        return float(lastline.split()[1])
    else:
        print("method = highest")
        return highestline
        
   

def folding_rate(protein, protein_path, benchmark_rmsd):
    "extracts rmsd of every run, and calculates total folding rate"
    log = open("/home/lorenzo.signorini/tirocinio/log/lancio_simulazioni_complete")
    total_folded_simulations = 0
    total_simulations = 0
    for line in log.readlines():
        split_line = line.split()
        if len(split_line) > 8:   # guarda solo le lines che non sono blank
            if split_line[1].startswith(protein): #guarda solo le lines di quella proteina
                total_simulations += 1
                temp_rmsd=split_line[7]
                if float(temp_rmsd) <= benchmark_rmsd:
                    total_folded_simulations += 1
    folding_rate = total_folded_simulations/total_simulations
    ln_folding_rate = np.log(folding_rate)
    f=open("/home/lorenzo.signorini/tirocinio/log/folding_rates", "a")
    f.write(protein+"\t\t"+str(benchmark_rmsd)+"\t\t"+str(folding_rate)+"\t\t"+str(ln_folding_rate)+"\n")
    f.close()
    return

def main():
    sim_folder = "/home/lorenzo.signorini/tirocinio/simulations"  # da cambiare 
    os.chdir(sim_folder) 
    proteins = os.listdir()
    print(proteins)
    for protein in proteins:
         full_path_to_protein_folder = sim_folder+"/"+protein
         os.chdir(full_path_to_protein_folder)
         print("--------------------------------------------------\n\nPROCESSING", protein,':\n\n')
         bench_rmsd = benchmark_rmsd(protein, full_path_to_protein_folder, method="highest")
         bench_rmsd = float(bench_rmsd)
    #     folding_rate(protein, full_path_to_protein_folder, bench_rmsd)
         real_folding_rate(protein, full_path_to_protein_folder, bench_rmsd)    
    return
main()

