#!/bin/bash
pdbcode=$1
echo 'pdb file '${pdbcode}'.pdb'
grep "ATOM" ${pdbcode}.pdb | grep " CA "  > ca.pdb
if [ -n "$2" ]; 
then
    chain=$2
    echo ${chain}' chain selected'
    grep " ${chain} " ca.pdb > ca2.pdb
    mv ca2.pdb ca.pdb
fi

awk 'BEGIN{FS=""}{if(($17==" ")||($17=="A"))print}' ca.pdb > ca2.pdb
mv ca2.pdb ca.pdb

#kaw structure
awk {'printf ("%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\n", $7/3.8,$8/3.8,$9/3.8,0.0,0.0,0.0)'} ca.pdb > conf.kaw
awk '{printf ("%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%d\t", $7/3.8,$8/3.8,$9/3.8,0.0,0.0,0.0,$6);print NR}' ca.pdb > ${pdbcode}.ind
n_beads=$(($(wc -l conf.kaw | awk '{print $1}')))
echo ${n_beads}' beads found'

printf '#read_chain     1\n' > head.kaw
printf '#Nbeads         %d\n'  "${n_beads}" >> head.kaw
printf '#timestep       0.0005\n' >> head.kaw
printf '#Nsteps         7000000\n' >> head.kaw
printf '#FENE_bond      1.5\n' >> head.kaw
printf '#FENE_kappa     30.0\n' >> head.kaw
printf '#dump_traj      1000\n' >> head.kaw
printf '#RV             4.0\n' >> head.kaw
printf '#epsilon        1.0\n' >> head.kaw
printf '#tau_frict      1.0\n' >> head.kaw
printf '#temp           0.1\n' >> head.kaw
printf '#niters         100\n' >> head.kaw
printf '#Coordinates  \n' >> head.kaw

cat head.kaw conf.kaw > ${pdbcode}.kaw

#xyz structure
printf '%d\n' "${n_beads}" > ${pdbcode}.xyz
printf 'constructed from %s\n' "${pdbfile}" >> ${pdbcode}.xyz
awk {'printf ("R%d\t%.3f\t%.3f\t%.3f\n", $6,$7/3.8,$8/3.8,$9/3.8)'} ca.pdb >> ${pdbcode}.xyz


rm ca.pdb conf.kaw head.kaw


