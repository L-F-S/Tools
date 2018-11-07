#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 15:03:16 2018

@author: lorenzo

TO BE USED ONLY ONCE

This cycles through all proteins and checks that all 'good' runs are 7000000 steps.

If they are greater (they shouldn't be lower, because I just check_simulation.py'ed),
it moves them to the more_than_7000000_nsteps folder
"""
import os
def move(protein, run):
    msd_mover = open('/home/lorenzo.signorini/tirocinio/simulations/temp_run_mover', 'a')
    line = "mv "+"/home/lorenzo.signorini/tirocinio/simulations/"+protein+"/"+run+" "+"/home/lorenzo.signorini/tirocinio/simulations/"+protein+"/more_than_7000000_nsteps\n"
    msd_mover.write(line)

def find_greater_timesteps(msd_file):
    f=open(msd_file)
    lines = len(f.readlines())
    if lines > 7000:
        print("found", lines, "lines")
        f.close()
        return True
    f.close()
    return False

def main():
    # iterate over all 26 proteins:
    #cd to simulations
    sim_folder = "/home/lorenzo.signorini/tirocinio/simulations/" #todo : change this to input_files_pdb2kaw if needed
    os.chdir(sim_folder)
    print(os.listdir())
    for protein_folder in os.listdir():
        full_path_to_protein_folder = sim_folder+"/"+protein_folder
        os.chdir(full_path_to_protein_folder)
        
        #iterate over all runs:
        messaggio="ci sono"+ str(len(os.listdir()))+ "runs"
        print(protein_folder)
        print(messaggio)
        
        for run_folder in os.listdir():
            if run_folder.startswith('run'):
                full_path_to_run = sim_folder+"/"+protein_folder+"/"+run_folder
                os.chdir(full_path_to_run)
                greater_timestep = False
                for msdfile in os.listdir():
                    if msdfile.startswith('msd'):
                        greater_timestep = find_greater_timesteps(msdfile)
                if greater_timestep == True:
                    print("^ found in protein", protein_folder, "run", run_folder)
                    move(protein_folder, run_folder)
    
    return

main()