#!/bin/bash

# This cycle submits 100 jobs, each of which takes one core and sequencially simulates all 26 proteins. Each protein takes about 10 mins, each run takes on average 3.87 hours.


for i in  {1..250}; do
	less one_round.sh > round_${i}.sh
	qsub -q cpuq round_${i}.sh -e err_round_$i -o out_round_$i
done

