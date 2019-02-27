#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 26/02/2019  from efr4_forcluster.py

@author: lorenzo

uguale a efr4_forcluster, ma con la mediana solo sullle traiettorie che foldano.



"""
import os
import numpy as np
from sys import argv
import matplotlib.pyplot as plt
#import matplotlib.patches as mpatches   # questo per fare la legenda nell´hist dei tempi


###################################################
#   NEW FUNCTIONS TO CALCUALTE REAL FOLDING RATES #
###################################################

def real_folding_rate(list_of_n_steps, total_n_of_runs, ffreq, median):
    """ Returns folding time and folding rate (as 1/folding_time)
    of folding simulations.
    INPUTS:
        list_of_n_steps = a list of the timesteps at which each run has folded
        total_n_of_runs = total number of simulations (might not have folded)
        ffreq = folding rate (as in, folding frequency: foldend_runs/total_runs
        median = BOOL to tell which time to evaluate
        mean tsteps are calcukated on succesful runs. Median are calculated on all runs,
        so only runs with a ffreq >= 0.5 are counted
        """
        
    
#    print(list_of_n_steps)
  #  print("total steps",len(list_of_n_steps))
#    plt.hist(list_of_n_steps)    

    ################################/#
    # CALCULATE REAL FR
    time = np.mean(list_of_n_steps) if median == "mean" else np.median(list_of_n_steps)
    print(median, "timesteps: ", time)
    real_FR = 1/time
    ln_real_folding_rate = round(np.log(real_FR), 3)
    print(median, " folding Rate:", real_FR, ln_real_folding_rate)

    ################################

    return str(time),str(real_FR),str(ln_real_folding_rate)

###############################################################################

def histogram_times(list_of_n_steps,median_time,mean_time,protein_path):
    fig,ax = plt.subplots()
    ax.hist(list_of_n_steps, bins=100, color= 'black')
    
    #add mean and median lines:
    ax.axvline(float(mean_time), color = 'red', linestyle =  '--')
    if not median_time == 'nan':
       ax.axvline(float(median_time), color = 'pink', linestyle =  '--')
#    mean_patch = mpatches.Patch(color='red', label='Mean')
#    median_patch = mpatches.Patch(color='pink', label='Median')
#
#    plt.legend(handles=[mean_patch, median_patch])
    plt.savefig(protein_path+"/hist_timesteps.png")
    return


def find_extreme_value(filename, method,return_timestep, benchmark_rmsd):
    if method == "highest":
        extreme_value = 0
    if method == "lowest":
        extreme_value = 999999999
   
    f=open(filename)
    for line in f.readlines():
        if method == "highest":
            if float(line.split()[1]) > extreme_value:
                     extreme_value = float(line.split()[1])
                     tstep_of_extreme_value = float(line.split()[0])
        if method == "lowest":
            if float(line.split()[1]) < extreme_value:
                     extreme_value = float(line.split()[1])
                     tstep_of_extreme_value = float(line.split()[0])
                     if extreme_value <= benchmark_rmsd:
                         break                  
    f.close()
    return extreme_value, tstep_of_extreme_value

def benchmark_rmsd(protein):
    "extracts last line of the msd file in one readchain1 run"
    print("--------------------------------------------------\n\nfinding benchmark")
    just_protname = protein[:4]
    equi_protname = just_protname+"_optiequi"
    equi_path = "/ptmp/slor/equi"
    os.chdir(equi_path+"/"+equi_protname)
    first_folder = True
    for folder in os.listdir():
        if folder.startswith("run"):
            if first_folder == True:
                first_folder = False
                os.chdir(equi_path+"/"+equi_protname+"/"+folder)
                for filename in os.listdir():
                    if filename.startswith("msd"):                       
                        highest_value, tstepchenonmiservenonritornononfaccionulla = find_extreme_value(filename,"highest",False, 0)

    return round(highest_value,2)
        
def fermi_of(x,benchmark_rmsd):
    w=0.2
    return 1/(np.exp((x-benchmark_rmsd)/w)+1) #bench  rmsd for fermi dist  


def has_folded(run, benchmark_rmsd, protein_path, fermi, list_of_n_steps):
    has_reached_nc = False    
    for cosa in os.listdir():  
        if cosa.startswith("native"):
            os.chdir(protein_path+"/"+run+"/"+cosa)
            for dovrebbeesseresolounfile in os.listdir():
                nc_file = open(dovrebbeesseresolounfile)
                nc_values=nc_file.readlines()
                nc_file.close()                  
                if max([int(nc.split(" ")[1].rstrip()) for nc in nc_values]) >= round(0.95*int(nc_values[0].split(" ")[2].rstrip()), 0):
                     has_reached_nc = True
    if has_reached_nc:
        os.chdir("../")
        for cosa in os.listdir():   # faccio due volte lo stesso for to make sure che prima faccia l altro
            if cosa.startswith("msd_"):
                lowest_msd_of, timestep_of_lowest_msd = find_extreme_value(cosa,"lowest", True, benchmark_rmsd)
                if fermi == False:
                    if lowest_msd_of <= benchmark_rmsd:
                        list_of_n_steps.append(timestep_of_lowest_msd)
                        return 1, list_of_n_steps
                    else:
                        return 0, list_of_n_steps
                else:
                    return fermi_of(lowest_msd_of, benchmark_rmsd)
    return 0, list_of_n_steps
        
        
def folding_freq(protein_path, benchmark_rmsd, folded_runs_file):
    "extracts rmsd of every run, and calculates total folding rate"
    os.chdir(protein_path)
    total_folded_simulations = 0
    total_simulations = 0 

    list_of_n_steps= []  # to calculate median and mean times 
    for run in os.listdir():
        if run.startswith("run"):
            os.chdir(protein_path+"/"+run)
            total_simulations += 1
            fermi = False
            this_much_folditude, list_of_n_steps = has_folded(run, benchmark_rmsd, protein_path, fermi, list_of_n_steps)

            total_folded_simulations += this_much_folditude 
            
            if fermi == False and this_much_folditude == 1:
                folded_runs_file.write(run + "\n")
    list_of_n_steps.sort()
    folding_rate = round(total_folded_simulations/total_simulations, 3)
    ln_folding_rate = round(np.log(folding_rate), 3)
    print("Folding frequency (andi its log):", folding_rate, ln_folding_rate)
    mean_time, mean_rate, ln_mean_rate = real_folding_rate(list_of_n_steps, total_simulations, folding_rate, "mean")
    median_time, median_rate, ln_median_rate = real_folding_rate(list_of_n_steps, total_simulations, folding_rate, "median") 
    
    histogram_times(list_of_n_steps,median_time,mean_time,protein_path)

    return str(folding_rate)+"\t\t"+str(ln_folding_rate)+"\t\t"+str(mean_time)+"\t\t"+str(mean_rate)+"\t\t"+str(ln_mean_rate)+"\t\t"+str(median_time)+"\t\t"+str(median_rate)+"\t\t"+str(ln_median_rate)

###############################################################################

def user_input():
    if len(argv) <= 1:
        print("USAGE: python3 efr4.py protname(or \"all\") foldThresholdMethod(equi-msd0.9-old)")
        exit(1)
    else:
        return [argv[1]]  if not argv[1] == "all" else os.listdir(), argv[2]  
    
def main():
    sim_folder = "/ptmp/slor/fold" # da cambiare  # todo tempywempy/ptmp/slor/fold  /data/isilon/signorini/fold_runs/tests
    os.chdir(sim_folder) 
    proteinfolders, threshold_method = user_input()
    print(proteinfolders)
    print(threshold_method)
    old_bench_inrealtasidicethreshold_of = {"1afi":0.604438, "1aps" : 0.684557, "1aye":0.852853, "1bnz":0.656197, "1bzp":1.442774, "1csp":0.55736, "1div":0.616245, "1fkb":0.832244, "1hrc":1.010378, "1hz6":0.650115, "1imq":0.948066, "1lmb3":0.866795, "1pgb":0.63142, "1poh":0.735785, "1psf":0.868276, "1shf":0.555695, "1ten":0.813828, "1tit":0.792652, "1ubq":0.813788, "1urn":0.860587, "1wit":1.152467, "2abd":1.045988, "2ci2":0.682243, "2pdd":0.415568, "2vik":1.330742, "256b":0.980126}
    
    for proteinfolder in proteinfolders:
        if proteinfolder.startswith("1") or proteinfolder.startswith("2"):            
            full_path_to_protein_folder = sim_folder+"/"+proteinfolder
            os.chdir(full_path_to_protein_folder)
            print("--------------------------------------------------\n\nPROCESSING", proteinfolder,':\n\n')
            
            folded_runs_file=open(full_path_to_protein_folder+"/"+"folded_runs", "w")
            folded_runs_file.close()
            folded_runs_file=open(full_path_to_protein_folder+"/"+"folded_runs", "a")

            bench_rmsd = benchmark_rmsd(proteinfolder) if threshold_method == "equi" else float(threshold_method[3:]) if threshold_method.startswith("msd") else old_bench_inrealtasidicethreshold_of[proteinfolder[:4]] if threshold_method == "old" else "SBAGLIATO A SCRIVERE threshold method"
            print("benchmark rmsd = " , bench_rmsd, "method = ", threshold_method)
            
            folded_runs_file.write("benchmark rmsd = "+str(bench_rmsd)+"\t threshold method:"+str(threshold_method)+"\n")
            all_folding_proxies = folding_freq(full_path_to_protein_folder, bench_rmsd, folded_runs_file)
            folded_runs_file.close()
             
            f=open("/ptmp/slor/da/folding_stats.dat", "a")
            f.write(proteinfolder+"\t\t"+threshold_method+"\t\t" +str(bench_rmsd)+"\t\t"+all_folding_proxies+"\n")
            f.close()
    return

main()

#AGGIUNTOPERSBAGLIOSELEZIONANDOCOLMOUSE