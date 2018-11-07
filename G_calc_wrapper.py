#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 15:15:45 2018

@author: lorenzo

V1

python wrapper to iterate over all trajectories of all proteins and launch the 
gc calculator in /tools/gcalc
"""
import os
import numpy as np

input_file_p1 = "#start 0\n#end -1\n#dr  0.25\n#closed1 1\n#closed2 1\n#segment1\n"
input_file_p2 = "#segment2\n"
input_of = {'1aps':['1	38\n','39	96\n']\
            '1aps':['1	38\n','39	96\n']\
            '1aps':['1	38\n','39	96\n']\
            '1aps':['1	38\n','39	96\n']\
            }
def make_input_file(protein):
    seg1 = input_of[protein][0]
    seg2 = input_of[protein][1]
    
    input_for_prot = input_file_p1 + seg1 + input_file_p2 + seg2
    
    filename = "input_"+protein+".dat"
    f=open(filename,'w')
    f.write(input_for_prot)
    f.close()
    return filename

def main():
    sim_folder = "/home/lorenzo.signorini/tirocinio/simulations"  # da cambiare 
    os.chdir(sim_folder) 
    proteins = os.listdir()
    print(proteins)
    for protein in ['1aps']:
         full_path_to_protein_folder = sim_folder+"/"+protein
         os.chdir(full_path_to_protein_folder)
         print("--------------------------------------------------\n\nPROCESSING", protein,':\n\n')
         for run in os.listdir():
             for run in os.listdir():
                 if run.startswith("run"):
                   os.chdir(full_path_to_protein_folder+"/"+run+"/traj")
                   for traj in os.listdir(): # e' un for, ma  e' un file solo, comunque mettiamo l'f check di sicurezza
                       if traj.startswith("traj"):
                           print("Traiettoria n ", run, "protein : ", protein)
                           copia_g = "cp /home/lorenzo.signorini/tirocinio/tools/gcalc/Gc " + full_path_to_protein_folder+"/"+run+"/traj/"
                           os.system(copia_g)
                           input_name = make_input_file(protein)
                           comando = "./Gc " + traj + " " + input_name +" " + protein+"_"+run
                           os.system(comando)                           
                           os.system("rm Gc")
                           os.system("rm "+input_name)
                    
    return

main()