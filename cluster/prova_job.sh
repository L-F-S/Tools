#!/bin/bash
# JOB DI PROVA: DOVREBBE PRENDERE OGNI MOLECOLA CHE HO (28), E FARE DUE SIMULAZIONI PER OGNI MOLECOLA (UNA SU CORE), USANDO IN TOTALE 48 CORE, PER UNA DECINA DI MINUTI A CORE
# proteins: all
# params: default
# readchain=0
# forcefield: default (kb 50, kt 50, random k 0 (=no))
# program: polymerMD


# numero di nodi
#PBS -l select=2:ncpus=7:mem=30gb

# imposta il tempo massimo di esecuzione
#PBS -l walltime=2:30:0 
 
# imposta la coda di esecuzione (usa cpuq (o allq?))
#PBS -q cpuq 


module load mpich-3.2  #non so se serva



polymd=/home/lorenzo.signorini/tirocinio/p3rrygo-mpi_polymd-29226ebce6ce/bin/polymerMD.x


cd 

## declare an array variable
# declare -a arr=("1afi.pdb" "1aps.pdb" "1bnz_a.pdb" "1bzp.pdb" "1csp.pdb" "1div.n.pdb" "1fkb.pdb") non funge come sh 

for i in 1afi 1aps 1aye 1bnz_a 1bzp 1csp 1div.n 1fkb 1hrc 1hz6_a 1imq 1lmb3 1pgb 1poh 1psf 1shf_a 1ten 1tit 1ubq 1urn 1wit 2abd 2ci2 2pdd 2vik 256b; do
	cd /home/lorenzo.signorini/tirocinio/input_files_pdb2kaw/$i.pdb
	$polymd $i_0.kaw > out &
	done

module unload mpich-3.2

