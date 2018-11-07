#!/bin/bash
# proteins: 1hrc, 1hz6_A, 1imq, 1lmb3, 1pgb, 1poh, 1psf 
# params: default
#readchain=0
# forcefield: default (kb 50, kt 50, random k 0 (=no))
# program: polymerMD

polymd=../../p3rrygo-mpi_polymd-29226ebce6ce/bin/polymerMD.x

lamboot

cd ../input_files_pdb2kaw
for i in 1hrc 1hz6_a 1imq 1lmb3 1pgb 1poh 1psf; do
	cd $i.pdb
	# CHANGE PARAMETERS HERE	
	gawk -i inplace '{if(NR==1) {print "#read_chain     0"} else if (NR==4) {print "#Nsteps         7000000"} else {print $0} }' ${i}_0.kaw
	echo simulating ${i}_0
	$polymd ${i}_0.kaw > out &	
	cd ../
	done
echo ho finito, non so se solo di lanciare i comandi o anche di simulare
