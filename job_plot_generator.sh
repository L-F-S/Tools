#!/bin/bash
# JOB BASE. 

# numero di nodi
#PBS -l select=2:ncpus=5:mem=5gb

# imposta il tempo massimo di esecuzione
#PBS -l walltime=10:00:0 
 
# imposta la coda di esecuzione
#PBS -q cpuq 

#imposta file di output e errore
#PBS -e err_plots -o out_plots

# Iterates through folders and launches the R script to plot.

# DA FARE PRIMA DI LANCIARLO DAVVERO:SOLO DOPO CHE finisce lo script che crea i dati, cambia il nome nelle cartelle in analyses, e leva il .pdb finale.
# cambiare i path in line 24, 30 (due path diversi!)



cd  /home/lorenzo.signorini/tirocinio/analyses  # /home/lorenzo.signorini/tirocinio/analyses

echo $(ls)
for i in $(ls); do
	echo $i
	Rscript /home/lorenzo.signorini/tirocinio/tools/Free_Energy_plot.R /home/lorenzo.signorini/tirocinio/analyses/$i/${i}_nc_rmsd.tsv
done
