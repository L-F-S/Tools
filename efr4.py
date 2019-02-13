#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 16:06:52 2018

@author: lorenzo

v4: 12/02/2019:
    cambiare il modo di calcolare mean e median per calcoalrle meglio
v 3.1: 06/02/2019:
    aggeggiata per le cartelle al Max Plank
    make sure you eliminated crashed runs before launching this
    folding_rates function cambiata con folding_freq
        aggiunta funzione has_folded(run)
    benchmark rmsd cambiato per la sintassi di qui
    all output printed to one file

vesrsion 3.0
Calculates estimated folding rate of proteins.

version 3:
NEW VERSION OF (real) folding rate:
    uses median instead of mean: 
        we shall call this median_fr
        
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
from sys import argv

###################################################
#   NEW FUNCTIONS TO CALCUALTE REAL FOLDING RATES #
###################################################
   
    
def real_folding_rate(protein, protein_path, benchmark_rmsd,median):
    print("--------------------------------------------------\n\nCalculating Folding Rate using method:  "+median)
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
#    plt.hist(list_of_n_steps)    
    ################################/#
    # CALCULATE REAL FR
    if median == "median":
        real_FR = round(1/np.mean(list_of_n_steps), 3)
    else:
        real_FR= round(1/np.median(list_of_n_steps), 3)
    print("Folding Rate:", real_FR)
    ln_real_folding_rate = round(np.log(real_FR), 3)
    ################################

    return str(real_FR)+"\t\t"+str(ln_real_folding_rate)

###############################################################################

def find_extreme_value(filename, method):
    if method == "highest":
        extreme_value = 0
    if method == "lowest":
        extreme_value = 999999999
   
    f=open(filename)
    for line in f.readlines():
        if method == "highest":
            if float(line.split()[1]) > extreme_value:
                     extreme_value = float(line.split()[1])
        if method == "lowest":
            if float(line.split()[1]) < extreme_value:
                     extreme_value = float(line.split()[1])
    f.close()
    return extreme_value

def benchmark_rmsd(protein):
    "extracts last line of the msd file in one readchain1 run"
    print("--------------------------------------------------\n\nfinding benchmark")
    just_protname = protein[4:]
    equi_protname = "equi"+just_protname
    equi_path = "/data/isilon/signorini/equi_runs"
    os.chdir(equi_path+"/"+equi_protname)
    first_folder = True
    for folder in os.listdir():
        if folder.startswith("run"):
            if first_folder == True:
                first_folder = False
                os.chdir(equi_path+"/"+equi_protname+"/"+folder)
                for filename in os.listdir():
                    if filename.startswith("msd"):                       
                        highest_value = find_extreme_value(filename,"highest")

    return round(highest_value,2)
        
def fermi_of(x,benchmark_rmsd):
    w=0.2
    return 1/(np.exp((x-benchmark_rmsd)/w)+1) #bench  rmsd for fermi dist  

def has_folded(run, benchmark_rmsd, protein_path, fermi):
    has_reached_nc = False

    for cosa in os.listdir():  
        if cosa.startswith("native"):
            os.chdir(protein_path+"/"+run+"/"+cosa)
            for dovrebbeesseresolounfile in os.listdir():
                nc_file = open(dovrebbeesseresolounfile)
                nc_values=nc_file.readlines()
                nc_file.close()                  
                if max([int(nc.split(" ")[1].rstrip()) for nc in nc_values]) == int(nc_values[0].split(" ")[2].rstrip()):
                     has_reached_nc = True

    if has_reached_nc:
        os.chdir("../")
        for cosa in os.listdir():   # faccio due volte lo stesso for to make sure che prima faccia l altro
            if cosa.startswith("msd_"):
                lowest_msd_of = find_extreme_value(cosa,"lowest")
                if fermi == False:
                    if lowest_msd_of <= benchmark_rmsd:
                        return 1
                    else:
                        return 0
                else:
                    return fermi_of(lowest_msd_of, benchmark_rmsd)
    return 0
        
        
def folding_freq(protein, protein_path, benchmark_rmsd, folded_runs_file):
    "extracts rmsd of every run, and calculates total folding rate"
    print("--------------------------------------------------\nEstimating Folding Frequency across all runs")
    os.chdir(protein_path)
    total_folded_simulations = 0
    total_simulations = 0 
    for run in os.listdir():
        if run.startswith("run"):
            os.chdir(protein_path+"/"+run)
            total_simulations += 1
            fermi = False
            this_much_folditude = has_folded(run, benchmark_rmsd, protein_path, fermi)

            total_folded_simulations += this_much_folditude 
            
            if fermi == False:
                folded_runs_file.write("run" + run + "\n")
                
    folding_rate = round(total_folded_simulations/total_simulations, 3)
    ln_folding_rate = round(np.log(folding_rate), 3)
    return str(folding_rate)+"\t\t"+str(ln_folding_rate)

###############################################################################

def user_input():
    if len(argv) <= 1:
        print("USAGE: python3 estimate_folding_rates_3.py protname(or \"all\") foldThresholdMethod(equi-msd0.9)")
        exit(1)
    else:
        return ["fold_"+argv[1]+"_optimized"] if not argv[1] == "all" else os.listdir(), argv[2] if argv[2] == "equi" else float(argv[2][3:])

def main():
    sim_folder = "/data/isilon/signorini/fold_runs"  # da cambiare 
    os.chdir(sim_folder) 
    proteins, threshold_method = user_input()
    for protein in proteins:
         full_path_to_protein_folder = sim_folder+"/"+protein
         os.chdir(full_path_to_protein_folder)
         print("--------------------------------------------------\n\nPROCESSING", protein,':\n\n')
         
         folded_runs_file=open(full_path_to_protein_folder+"/"+"folded_runs", "a")

         bench_rmsd = benchmark_rmsd(protein) if threshold_method == "equi" else threshold_method
         print("benchmark rmsd = " , bench_rmsd )
         
         folded_runs_file.write("benchmark rmsd = "+str(bench_rmsd)+"\n")
         folding_freqs = folding_freq(protein, full_path_to_protein_folder, bench_rmsd, folded_runs_file)
         print("Folding frequency and its natural logarithm:", folding_freqs)
         folded_runs_file.close()
         
         median_rates = real_folding_rate(protein, full_path_to_protein_folder, bench_rmsd, "median")    
         mean_rates = real_folding_rate(protein, full_path_to_protein_folder, bench_rmsd, "mean")  
         
         f=open("/data/isilon/signorini/da/folding_frequencies", "a")
         f.write(protein+"\t\t"+str(bench_rmsd)+"\t\t"+folding_freqs+"\t\t"+median_rates +"\t\t" + mean_rates+"\n")
         f.close()

    return

main()

#AGGIUNTOPERSBAGLIOSELEZIONANDOCOLMOUSE