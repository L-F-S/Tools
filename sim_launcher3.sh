#!/bin/bash
# proteins: 1ten 1tit 1ubq 1urn 2abd 2ci2 2pdd
# params: default
# readchain=0
# forcefield: default (kb 50, kt 50, random k 0 (=no))
# program: polymerMD

polymd=../../p3rrygo-mpi_polymd-29226ebce6ce/bin/polymerMD.x

lamboot 

cd ../input_files_pdb2kaw

## declare an array variable
# declare -a arr=("1afi.pdb" "1aps.pdb" "1bnz_a.pdb" "1bzp.pdb" "1csp.pdb" "1div.n.pdb" "1fkb.pdb") non funge come sh 

for i in 1ten 1tit 1ubq 1urn 2abd 2ci2 2pdd; do
	cd $i.pdb
	# CHANGE PARAMETERS HERE	
	gawk -i inplace '{if(NR==1) {print "#read_chain     0"} else if (NR==4) {print "#Nsteps         7000000"} else {print $0} }' ${i}_0.kaw
	echo simulating ${i}_0
	$polymd ${i}_0.kaw > out &	
	cd ../
	done
echo ho finito di lanciare le simulazioni, stanno girando
