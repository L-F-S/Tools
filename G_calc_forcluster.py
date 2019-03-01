#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 28/02/2019 from G_calc_wrapper.py
la versione per girare su clsuter a Mainz

@author: lorenzo

V2

python wrapper to iterate over all trajectories of all proteins and launch the 
gc calculator in /tools/gcalc
"""
import os
import sys
import numpy as np
import pandas as pd

input_file_p1 = "#start 0\n#end -1\n#dr  0.25\n#segment1\n"
input_file_p2 = "#segment2\n"


def fai_cose(traj, run, protein, path, input_name):
#       """devo: prendere il file traj, copiarlo temporaneamente 
#   in /ptmp/slor/temp, creare ivi il file input_data (che quindi creo una tantum per proteina),
#   metterci il Gc (che posso quindi metterci diretto da local), e infine cancellare il .traj
#   """  
   
   print("Traiettoria n ", run, "protein : ", protein)
  #     copia_g = "cp /home/lorenzo.signorini/tirocinio/tools/gcalc/Gc " + full_path_to_protein_folder+"/"+run+"/traj/"
#                           os.system(copia_g)
   copia_traj = "cp " + path +"/"+traj+"  /ptmp/slor/temp"
   print(copia_traj)
   os.system(copia_traj)
   os.chdir("/ptmp/slor/temp")
   comando = "./Gc " + traj + " " + input_name +" " + protein+"_"+run
   print(comando)
   os.system(comando)                           
   os.system("rm "+ traj)
   # sposta le traiettorie dentro le rispettive run
   #sposta_traj='mv '+'G_'+ protein+"_"+run+'.dat'+' "/ptmp/slor/fold/'+protein+'/'+run+'/'
  # os.system(sposta_traj)
   return


def input_data():
    os.chdir("/ptmp/slor/da")
    data = pd.read_csv("baiesi_data", header= 1, sep ='\t')
    return data

def make_input_file(protein, prot_metadata):
    os.chdir("/ptmp/slor/temp")
    i1 = int(prot_metadata.i1)
    i2 = int(prot_metadata.i2)
    j1 = int(prot_metadata.j1)
    j2 = int(prot_metadata.j2)
    
    input_for_prot = input_file_p1 + str(i1) + "	" + str(i2) +"\n" + input_file_p2 + str(j1) + "	" + str(j2) + "\n"
    
    filename = "input_"+protein+".dat"
    f=open(filename,'w')
    f.write(input_for_prot)
    f.close()
    return filename


def user_input():
    if len(sys.argv) <= 1:
        print("USAGE: python3 G_calc_forcluster.py protname(or [all])")
        exit(1)
    else:
        return [sys.argv[1]]  if not sys.argv[1] == "all" else os.listdir()
    
def main():
    
    protein_metadata = input_data()
    
    sim_folder = "/ptmp/slor/fold"  # da cambiare 
    os.chdir(sim_folder) 
    proteins = user_input()
    print(proteins)
    for protein in proteins:
         if protein.startswith("1") or protein.startswith("2"):
             print("--------------------------------------------------\n\nPROCESSING", protein,':\n\n')
             input_name = make_input_file(protein, protein_metadata[protein_metadata.name==protein[:4]])
             full_path_to_protein_folder = sim_folder+"/"+protein
             os.chdir(full_path_to_protein_folder)
             for run in os.listdir():
                 if run.startswith("run"):
                   full_p_pr_t = full_path_to_protein_folder+"/"+run+"/traj"
                   os.chdir(full_p_pr_t)
                   for traj in os.listdir(): # e' un for, ma  e' un file solo, comunque mettiamo l'f check di sicurezza
                       if traj.startswith("traj"):
                           fai_cose(traj, run, protein, full_p_pr_t, input_name)               
    return

main()