#!/bin/bash
# proteins: 1afi, 1aps, 1bnz_a, 1bzp, 1csp, 1div.n, 1fkb 
#PARAMETERS:
#read_chain     0
#Nbeads         72
#timestep       0.0005
#Nsteps         7000000
#FENE_bond      1.5
#FENE_kappa     30.0
#dump_traj      1000
#RV             4.0
#epsilon        1.0
#tau_frict      1.0
#temp           0.1
#niters         100
#------------------------
# forcefield: default (kb 50, kt 50, random k 0 (=no))
# program: polymerMD

polymd= /home/lorenzo.signorini/tirocinio/p3rrygo-mpi_polymd-29226ebce6ce/bin/polymerMD.x

lamboot 

cd ../input_files_pdb2kaw

## declare an array variable
# declare -a arr=("1afi.pdb" "1aps.pdb" "1bnz_a.pdb" "1bzp.pdb" "1csp.pdb" "1div.n.pdb" "1fkb.pdb") non funge come sh 
echo $ls
for i in 1afi 1aps 1bnz_a 1bzp 1csp 1div.n 1fkb; do
	cd ${i}.pdb

	# CHANGE PARAMETERS HERE
	gawk -i inplace '{if(NR==1) {print "#read_chain     0"} else if (NR==4) {print "#Nsteps         7000000"} else {print $0} }' ${i}_0.kaw
	echo simulating ${i}_0
	$polymd ${i}_0.kaw > out &	
	cd ../
	done
echo ho finito di lanciare le simulazioni, stanno girando
