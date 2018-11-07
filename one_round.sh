#!/bin/bash
# JOB BASE. 
# usa 1 solo core.
#            -ogni job lancia, in sequenza, polyMD per tutte e 26 le molecole.
#                 
#  TEMPO DI ESECUZIONE STIMATO:
#   ogni molecola ci mette circa 10 minuti --> ogni job ci mette circa 260/60 = 4:20 h
#
#  TEMPO DI ESECUZIONE EFFETTIVO:
#  In media, 3.87h a job.

# proteins: all
# params: default
# readchain=0
# forcefield: default (kb 50, kt 50, random k 0 (=no))
# program: polymerMD

# numero di nodi
#PBS -l select=1:ncpus=1:mem=1gb

# imposta il tempo massimo di esecuzione
#PBS -l walltime=5:00:0 
 
# imposta la coda di esecuzione (usa cpuq (o allq?))
#PBS -q cpuq 

#imposta file di output e errore


# ci vogliono circa 10 minuti a simulazione

echo start time: $(date)


module load mpich-3.2  #non so se serva

polymd=/home/lorenzo.signorini/tirocinio/p3rrygo-mpi_polymd-29226ebce6ce/bin/polymerMD.x


cd 

for i in 1afi 1aps 1aye 1bnz_a 1bzp 1csp 1div.n 1fkb 1hrc 1hz6_a 1imq 1lmb3 1pgb 1poh 1psf 1shf_a 1ten 1tit 1ubq 1urn 1wit 2abd 2ci2 2pdd 2vik 256b; do
	echo processing $i. $(date)
	# to change parameters (remember to cambiarli anche al check dopo)
	# gawk -i inplace '{if(NR==1) {print "#read_chain     0"} else if (NR==4) {print "#Nsteps         7000000"} else {print $0} }' ${i}_0.kaw
	cd /home/lorenzo.signorini/tirocinio/input_files_pdb2kaw/$i.pdb
	$polymd $i_0.kaw > out
	echo Done.  $(date)
	echo --------------------------
	done

module unload mpich-3.2

echo end time: $(date)

