#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 11:50:53 2018

@author: lorenzo
v2.
    extraction of G coordinatesd added.
v1.
Extracts RMSD and Native Contact values, across all runs, for every protein in the dataset
Saves the occurences in the file protname.pdb_nc_rmsd.tsv.
Use that file to creat the graphs

USAGE:
    
python prel_analyses.py 0 

# to specify a protein, do:

python prel_analyses.py prot_folder_name

# to specifiy mpore than one protein:

python prel_analyses.py prot1-prot2-prot3


# This presuppone che tutte le cartelle si chiamino proteina_optifold, e dentro abbiano 
# cartelle che si chiamano run_numeri, e che TUTTE queste cartelle siano run funzionanti
"""

#
from sys import argv
import os

####################################
# COORDINATES EXTRACTION
def extract_coordinates_of_folded_runs_onlye(protein, full_path_to_prot, do_nc=True, do_rmsd=True):
    f_runs_file = open(full_path_to_prot+'/folded_runs', 'r')
    folded_runs=[f.rstrip('\n') for f in f_runs_file.readlines()]
    f_runs_file.close()
    rmsd=[]
    all_nc=[]
    for run in sorted(os.listdir()):
        if run.startswith("run") and run in folded_runs:
            os.chdir(full_path_to_prot+"/"+run)
            for subfolder in os.listdir():
                if subfolder.startswith("msd") and do_rmsd == True:
                    os.chdir(full_path_to_prot+"/"+run)
                    f=open(subfolder)
                    msd_values=f.readlines()
                    f.close()
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
    
    
    """ supponendo ora che i valori di rmsd e nc siano stati appesi in ordine:"""
    if len(rmsd) == len(normalized_nc):
        """crea un file da dare in pasto ad un altro script per fare il grafico della free energy"""
        os.chdir(full_path_to_prot)
        fname=protein+"FOLDED_nc_rmsd.tsv"
        f = open(fname, "w")
        for i in range(len(rmsd)):
            line = str(round(rmsd[i], 2)) + "\t" + str(round(normalized_nc[i],2)) + "\n"    
            f.write(line)
        f.close()
    else:
        raise ValueError("ATTENZIONE!! La lista di RMSD e NC della proteina", protein, "hanno lunghezza diversa!!\nLen(rmsd):" , len(rmsd),"\nLen(nc):", len(normalized_nc))
 
    return



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
    sim_folder = "/ptmp/slor/fold"
    os.chdir(sim_folder)   
    proteins = wrapper()
    for protein in proteins:
        if protein.startswith("1") or protein.startswith("2"):
             full_path_to_protein_folder = sim_folder+"/"+protein
             os.chdir(full_path_to_protein_folder)
             print("--------------------------------------------------\n\nPROCESSING", protein,':\n\n')
             print('extracting rmsd and nc values')
             extract_coordinates_of_folded_runs_onlye(protein, full_path_to_protein_folder)
             print("DONE")
    return

main()
