#!/bin/bash

cd
for i in 1afi 1aps 1aye 1bnz_a 1bzp 1csp 1div.n 1fkb 1hrc 1hz6_a 1imq 1lmb3 1pgb 1poh 1psf 1shf_a 1ten 1tit 1ubq 1urn 1wit 2abd 2ci2 2pdd 2vik 256b; do
	awk '{if (NR==1) {print "#read_chain     0"} else {print $0} }' tirocinio/input_files_pdb2kaw/$i.pdb/$i.kaw > tirocinio/input_files_pdb2kaw/$i.pdb/$i_0.kaw
	done
