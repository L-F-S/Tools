#!/bin/bash
# JOB BASE. 

# proteins: all
# params: default
# readchain=0
# forcefield: default (kb 50, kt 50, random k 0 (=no))
# program: polymerMD


# numero di nodi
#PBS -l select=2:ncpus=7:mem=10gb

# imposta il tempo massimo di esecuzione
#PBS -l walltime=8:00:0 
 
# imposta la coda di esecuzione (usa cpuq (o allq?))
#PBS -q cpuq 

#PBS -e err_prel_ana
#PBS -o out_prel_ana



cd /home/lorenzo.signorini/mplbpd-env/bin
source activate

python3 /home/lorenzo.signorini/tirocinio/tools/prel_analyses.py 0 0

deactivate

