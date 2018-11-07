#!/bin/bash

cd
for i in *.pdb; do
echo $i
	awk '{if (NR==1) {print "#read_chain     0"} else {print $0} }' tirocinio/input_files_pdb2kaw/$i.pdb/$i.kaw > tirocinio/input_files_pdb2kaw/$i.pdb/$i_0.kaw
	done
