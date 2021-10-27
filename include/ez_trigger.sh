#!/bin/ksh
#SBATCH --workdir=/scratch/ms/at/zat2
#SBATCH --job-name=ef06h012
#SBATCH --qos=express
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=clemens.wastl@zamg.ac.at

##### Start with ecaccess-job-submit -ni ef12h036 -mp "nothing to be done" -rc 1 ./ez_trigger.sh ######

set -ex

##--- Set date variables for actual model run
lagg=6
lagg2=9
HPROD=$MSJ_BASETIME

(( HRUN = $HPROD + $lagg))
if [[ $HRUN -ge 24 ]]
then
   (( HRUN = $HRUN - 24))
fi

HRJ=$(printf "%02d" $HRUN)

(( HRUN2 = $HPROD + $lagg2))
if [[ $HRUN2 -ge 24 ]]
then
   (( HRUN2 = $HRUN2 - 24))
fi

HRJ2=$(printf "%02d" $HRUN2)

# Set task complete for ecFlow
module load ecflow
export ECF_HOST=ecgate
export ECF_PORT=5276
suiteName='claef'
ecflow_client --resume /${suiteName}/runs/RUN_${HRJ}/dummy/ez_trigger/dummy1 
ecflow_client --resume /${suiteName}/runs/RUN_${HRJ2}/dummy/ez_trigger/dummy1 
exit
