#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 11:50:53 2018

@author: lorenzo

Extracts RMSD and Native Contact values, across all runs, for every protein in the dataset
Saves the occurences in the file protname.pdb_nc_rmsd.tsv.
Use that file to creat the graphs

USAGE:
    
python prel_analyses.py 0 

# to specify a protein, do:

python prel_analyses.py prot_folder_name

# to specifiy mpore than one protein:

python prel_analyses.py prot1-prot2-prot3


# This presuppone che tutte le cartelle si chiamino proteina.pdb, e dentro abbiano 
# cartelle che si chiamano run_numeri, e che TUTTE queste cartelle siano run funzionanti
# presuppone quindi di aver mandato check-simulations.py
"""

#
from sys import argv
import os

####################################
# COORDINATES EXTRACTION

def extract_nc_rmsd(protein, full_path_to_prot, do_nc=True, do_rmsd=True):
    """Extract values of NC and RMSD together, for every timestep 
    and every simulation, and save them as a list of tuples. Every tuple
    is an occurrence of a given NC and a given RMSD. """
    rmsd=[]
    all_nc=[]
    nc_and_rmsd=[]
    for run in os.listdir():
        if run.startswith("run"):
            os.chdir(full_path_to_prot+"/"+run)
            for subfolder in os.listdir():
                if subfolder.startswith("msd") and do_rmsd == True:
                    os.chdir(full_path_to_prot+"/"+run)
                    f=open(subfolder)
                    msd_values=f.readlines()
                    f.close()
                    print(run)
                    curr_rmsd = [float(msd.split(" ")[1].rstrip()) for msd in msd_values]                   
                    rmsd+=curr_rmsd
                    
                if subfolder.startswith("native") and do_nc == True:
                     os.chdir("native_contacts")
                     firstline = True
                     for nc in os.listdir():
                        f=open(nc)
                        nc_values=f.readlines()
                        f.close()
                        curr_nc = [int(nc.split(" ")[1].rstrip()) for nc in nc_values]
                        if firstline == True:                  
                            total_nc = int(nc_values[0].split(" ")[2].rstrip())
                        all_nc+=curr_nc
                        
                        firstline = False
                
    normalized_nc = [nc/total_nc for nc in all_nc]
    
    print()
    
    """ supponendo ora che i valori di rmsd e nc siano stati appesi in ordine:"""
    if len(rmsd) == len(normalized_nc):
        """crea un file da dare in pasto ad R per fare il grafico della free energy"""
        full_path_to_graphs = full_path_to_prot.rstrip(protein).rstrip("/").rstrip("simulations") + "analyses/"
        os.chdir(full_path_to_graphs+protein+"/")
        fname=protein+"_nc_rmsd.tsv"
        f = open(fname, "a")
        f.write("RMSD\tNC\n")
        for i in range(len(rmsd)):
            line = str(round(rmsd[i], 2)) + "\t" + str(round(normalized_nc[i],2)) + "\n"    
            f.write(line)
        f.close()
    else:
        raise ValueError("ATTENZIONE!! La lista di RMSD e NC della proteina", protein, "hanno lunghezza diversa!!\nLen(rmsd):" , len(rmsd),"\nLen(nc):", len(normalized_nc))
              
    return nc_and_rmsd

################################    
#   main and Input manager
###############################

def wrapper():
    "returns a list of strings with protein names + an int enctrypting the analyses to be done (see 'preprocess' function)"
    
    print("\n--------------------------------------------------\n\nWellcome to your coarse grained molecular dynamics \nsimulations preprocessing unit\n\n--------------------------------------------------\n\n")
    # check which proteins
    if argv[1] == str(0):
        proteins = os.listdir()
        print("Processing all proteins\n")
    else:
        proteins = []
        if "-" in argv[1]:
            proteins = argv[1].split("-")
        else:
            proteins.append(argv[1])

    return proteins

def main():
    sim_folder = "/home/lorenzo.signorini/tirocinio/simulations" 
    os.chdir(sim_folder)   
    proteins = wrapper()
    for protein in proteins:
         full_path_to_protein_folder = sim_folder+"/"+protein
         os.chdir(full_path_to_protein_folder)
         print("--------------------------------------------------\n\nPROCESSING", protein,':\n\n')
         print('extracting rmsd and nc values')
         extract_nc_rmsd(protein, full_path_to_protein_folder)
         print("DONE")
    return

main()
