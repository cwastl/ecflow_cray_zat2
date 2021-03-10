#-----------------------------------------
#PBS -N %NAME%
#PBS -A %ACCOUNT%
#PBS -q %CLASS%
#PBS -v STHOST=%STHOST%
#PBS -m a
#PBS -M clemens.wastl@zamg.ac.at
#PBS -l EC_total_tasks=%NP%
#PBS -l EC_hyperthreads=1
#PBS -l EC_threads_per_task=1
#PBS -o %ECF_JOBOUT%
#PBS -j oe
#PBS -l EC_memory_per_task=8GB
#-----------------------------------------
