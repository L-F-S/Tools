#!/bin/bash

# numero di nodi
#PBS -l select=2:ncpus=3:mem=10gb

# imposta il tempo massimo di esecuzione
#PBS -l walltime=5:00:0 
 
# imposta la coda di esecuzione (usa cpuq (o allq?))
#PBS -q cpuq 

#############
# Check simulations
#############

# Updates the simulations log. 
# ALWAYS LAUNCH AFTER A FULL CYCLE OF SIMULATIONS
# Once a whole run of simulations is complete,
# this checks that 1) all simulations were completed
# 2) checks the msd to make sure they folded
# 3) checks the numbe rof native contacts formed
# 5) appends all these info to the log/lancio_simulazioni
# 4) moves the Run directory into the 'simulation/prot.pdb directory, (Only if not failed?)

# parmeters must be passed by hand here:
# be careful: DO THIS EVERY RUN, WITH DIFFERENT PARAMETERS
#READCHAIN=0 E VBB



module load python-3.5.2
nsteps=7000000
data=$(date +%Y-%m-%d)
python3 /home/lorenzo.signorini/tirocinio/tools/check_simulations.py $nsteps $data
module unload python-3.5.2
