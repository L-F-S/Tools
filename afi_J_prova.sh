#!/bin/bash
# JOB DI PROVA: DOVREBBE PRENDERE OGNI MOLECOLA CHE HO (28), E FARE DUE SIMULAZIONI PER OGNI MOLECOLA (UNA SU CORE), USANDO IN TOTALE 48 CORE, PER UNA DECINA DI MINUTI A CORE
# proteins: all
# params: default
# readchain=0
# forcefield: default (kb 50, kt 50, random k 0 (=no))
# program: polymerMD


# numero di nodi
#PBS -l select=3:ncpus=7:mem=1gb

#mem dice la memoria da usare PER NODO

# dovrei avere 3 copie per ognuno dei due??? chissà.

# imposta il tempo massimo di esecuzione
#PBS -l walltime=1:30:0 
 
# imposta la coda di esecuzione (usa cpuq (o allq?))
#PBS -q cpuq

#imposta file di output e errore

#PBS -e err_afi
#PBS -o out_afi

echo start time: $(date)


module load mpich-3.2  #non so se serva

polymd=/home/lorenzo.signorini/tirocinio/p3rrygo-mpi_polymd-29226ebce6ce/bin/polymerMD.x


cd 


echo processing 1afi. $(date)
cd /home/lorenzo.signorini/tirocinio/input_files_pdb2kaw/1afi.pdb
$polymd 1afi_0.kaw > out 
echo Done.  $(date)
echo --------------------------


module unload mpich-3.2

echo end time: $(date)

