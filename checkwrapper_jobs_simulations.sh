# Wrapper for the check_jobs.py and check_simulations.py

###############
# check jobs
#############

python3 check_jobs.py

#############
# Check simulations
#############

# Updates the simulations log. 
# ALWAYS LAUNCH AFTER A FULL CYCLE OF SIMULATIONS
# Once a whole run of simulations is complete,
# this checks that 1) all simulations were completed
# 2) checks the msd to make sure they folded
# 3) checks the numbe rof native contacts formed
# 5) appends all these info to the log/lancio_simulazioni
# 4) moves the Run directory into the 'simulation/prot.pdb directory, (Only if not failed?)

# parmeters must be passed by hand here:
# be careful: DO THIS EVERY RUN, WITH DIFFERENT PARAMETERS
#READCHAIN=0 E VBB
nsteps=7000000

#	date	protein    run    rmsd   natcon

cd /home/lorenzo.signorini/tirocinio/input_files_pdb2kaw
for i in $(ls); do
	echo checking $i
	cd /home/lorenzo.signorini/tirocinio/input_files_pdb2kaw/$i/run*
	msd=msd*   # $(lsd msd*)
	data=$(date +%Y-%m-%d)
	rundir=${PWD##*/}
    python3 /home/lorenzo.signorini/tirocinio/tools/check_simulations.py $msd $data $i $rundir $nsteps
	mv /home/lorenzo.signorini/tirocinio/input_files_pdb2kaw/$i/run* /home/lorenzo.signorini/tirocinio/simulations/$i
done
echo ------------------------------------------------------------------------------------------------------------------------ >> /home/lorenzo.signorini/tirocinio/log/lancio_simulazioni
echo >> /home/lorenzo.signorini/tirocinio/log/lancio_simulazioni

