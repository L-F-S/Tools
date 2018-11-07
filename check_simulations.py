#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    CAMBIARE PATH!!!

Created on Sat Jun  9 11:37:12 2018

@author: lorenzo

# Once a whole run of simulations is complete,
# this checks that 1) all simulations were completed
# 2) checks the msd to make sure they folded
# 3) checks the numbe rof native contacts formed
# 5) appends all these info to the log/lancio_simulazioni
# 7) moves all failed simulations to a 'failed' subfolder
# 6) creates a check_simulations log
# WARNING. this DOES not mv folders from the input_files_pdb2kaw to the simulations, xke mi scazzzava tutto.
# so do it manually.

#	# parmeters that must be passed as input:
# be careful: DO THIS EVERY RUN, WITH DIFFERENT PARAMETERS

nsteps = 7000000 , date = $(date +%Y-%m-%d)  the format is important.

usage: either through sh check_simulations.sh wrapper, or: (for example):

python check_simulations.py 7000000 $(date +%Y-%m-%d)



"""

from sys import argv
import os
import shutil

#os.chdir("/home/lorenzo.signorini/tirocinio/input_files_pdb2kaw")
#for dir in os.listdir():
#    os.ch
#    print (subdir)
      


# inspect MSD file

def inspect_msd(msd_file, nsteps): 
    f = open(msd_file)
    first= True
    lastline = []
    firstline = []
    lines = f.readlines()
    if len(lines) < int(nsteps)/1000:
        messaggio = "run" + run_folder + "of protein" + protein_folder + "not completed. : len :"  + str(len(lines))
        print(messaggio)
        flog.write(messaggio + '\n')
        shutil.move(full_path_to_run, full_path_to_protein_folder+"/failed/")
        return 1, 1
    for line in lines:
        if first == True:
            firstline=line.split()
            first = False
        else:
            if len(line.split()) == 2: 
                lastline=line.split()
    f.close()  
    return firstline, lastline
 
# 1) check simulation completed all the steps

def check_steps(firstline, lastline, nsteps):
    if int(lastline[0]) == int(nsteps):
        runcompleted = True
    else:
        runcompleted = False
    return runcompleted

# 2) check msd decreased

def check_msd_decreased(firstline, lastline):    
    if float(firstline[1]) > float(lastline[1]):
        msd_decreased = True
    else:
        msd_decreased = False
    
    last_msd_value = lastline[1]
    
    fold_success = ""
    if float(last_msd_value) < 1:
        fold_success = "OK"
    else:
        fold_success = "FAIL"
    return last_msd_value, fold_success, msd_decreased

# 3) inspect native contacts

def inspect_native_contacts():
    os.chdir('native_contacts')
    nativefile=open(os.listdir()[0])
    max_nc = 0
    for line in nativefile.readlines():
    
        # if the simulation failed, it might not have printed all the line
        if len(line.split()) == 3:
            iteration, nat_cont, native_native_conts = [i for i in line.split(" ")]
            if int(nat_cont) > int(max_nc):
                max_nc = nat_cont
            last_nc = nat_cont
        
    nativefile.close()
    return last_nc, max_nc, native_native_conts
# 4) append all these info to the lancio simulazioni file:

def write_line(msd_decreased, chain_name, data, run_name, runcompleted, nsteps, last_msd_value, fold_success, last_nc, max_nc, native_native_conts):
    f = open('/home/lorenzo.signorini/tirocinio/log/lancio_simulazioni_1ubq1urn', 'a')
    
    # chain_name date run_name parameters  results  simulation decreased MSD  msd native contacts
    #other parameters: append in the back
    
    if runcompleted:
        simulation = "OK"
    else: 
        simulation = "FAIL"
        
    if msd_decreased:
        sim_status = 'OK'
    else:
        sim_status = 'FAIL'
    
    riga = data + "\t" + chain_name + "\t" + run_name + "\t"  + nsteps + \
    "\t"  + "\\\\\\\\\\\\\\\\\\\\" + "\t" +simulation  + "\t" + sim_status  + "\t" +\
      last_msd_value + "\t"+ fold_success + "\t" + str(last_nc)+"-"+str(max_nc)+"/"+str(native_native_conts)+'\n'
    
    f.write(riga)
    f.close()
    return

###########
# main
##########

#cd to simulations
sim_folder = "/home/lorenzo.signorini/tirocinio/simulations" #todo : change this to input_files_pdb2kaw if needed
os.chdir(sim_folder)

# iterate over all 26 proteins:
print(os.listdir())
for protein_folder in ['1ubq', '1urn']:
    flog = open('/home/lorenzo.signorini/tirocinio/log/chek_simulations_log', 'a')
    full_path_to_protein_folder = sim_folder+"/"+protein_folder
    os.chdir(full_path_to_protein_folder)
    
    #iterate over all runs:
    messaggio="ci sono"+ str(len(os.listdir()))+ "runs"
    print(protein_folder)
    print(messaggio)
    
    flog.write(protein_folder + '\n')
    flog.write(messaggio + '\n')

    for run_folder in os.listdir():
        if run_folder.startswith('run'):
            full_path_to_run = sim_folder+"/"+protein_folder+"/"+run_folder
            os.chdir(full_path_to_run)
            msdfile=""
    
            for x in os.listdir():
                if x.startswith('msd'):
                    msdfile = x

            if not len(os.listdir())==7:
               if not run_folder == "readchain1":
                   if not run_folder == "histograms":
                       messaggio = "run" + run_folder + "of protein" + protein_folder + "not completed." + " dirs:" + str(os.listdir())
                       print(messaggio)
                       flog.write(messaggio + '\n')
                       shutil.move(full_path_to_run,full_path_to_protein_folder+"/failed/" )
            else:
                
                nsteps = argv[1] 
    
                firstline, lastline = inspect_msd(msdfile, nsteps)
                if firstline == 1:
                    # run not completed abort
                    continue
                else:
                    runcompleted = check_steps(firstline,lastline,nsteps)
                    last_msd_value, fold_success, msd_decreased = check_msd_decreased(firstline, lastline)
                    last_nc, max_nc, native_native_conts = inspect_native_contacts()
                    
                    chain_name = protein_folder 
                    data = argv[2] 
                    run_name = run_folder #todo
                    
                    write_line(msd_decreased, chain_name, data, run_name, runcompleted, nsteps, last_msd_value, fold_success, last_nc, max_nc, native_native_conts)
    
    flog.close()
            
#            # go back to protein_folder (useless, fortunatel ybecause it s indented wrong)
#            full_path_to_protein_folder = sim_folder+"/"+protein_folder
#            os.chdir(full_path_to_protein_folder)
            
    # go back to simulations folder
    os.chdir(sim_folder)
