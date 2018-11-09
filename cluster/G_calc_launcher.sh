# for loop to launch 26 jobs to calc G for 25 proteins (tutte meno 1poh)

for i in 1afi 1aps 1aye 1bnz_a 1bzp 1csp 1div.n 1fkb 1hrc 1hz6_a 1imq 1lmb3 1pgb 1psf 1shf_a 1ten 1tit 1ubq 1urn 1wit 2abd 2ci2 2pdd 2vik 256b;do
job=${i}_g_job

echo \# file creato con g_calc_launcher.sh >> $job
echo \#PBS -l select=2:ncpus=2:mem=2gb >> $job
echo \#PBS -q cpuq >> $job
echo \#PBS -N G_calc_${i}.in >> $job
echo \#PBS -o o.${i} >> $job
echo \#PBS -e e.${i} >> $job
echo module load python-3.5.2 >> $job
echo cd /home/lorenzo.signorini/tirocinio/tools/cluster >> $job
echo python3 G_calc_wrapper_CL_${i}.py >> $job
echo module unload >>$job

qsub $job

done


