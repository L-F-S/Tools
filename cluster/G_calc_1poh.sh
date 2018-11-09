#PBS -l select=2:ncpus=2:mem=2gb
#PBS -q allq
#PBS -N G_calc_1poh.in
#PBS -o o.1poh
#PBS -e e.1poh

# prova 2: gli os.system di g_calc_wrapper che sembravano non funzionare, sono stati sostituiti da dei 'print', il che vuol dire che il file di  output sarà una listazza di cose che probabilmente basterà eseguire con un altro wrapper possibly (ovvero, basterà aggiungere gli header pbs a G_calc_wrapper_1.out (e rinominarlo (o meglio, slavarne una copia) G_calc_2.in)

module load python-3.5.2
cd /home/lorenzo.signorini/tirocinio/tools/cluster
python3 G_calc_wrapper_CL_1poh.py
module unload
