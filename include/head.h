#!%SHELL:/bin/ksh% 


set -e          # stop the shell on first error
set -u          # fail when using an undefined variable
set -x          # echo script lines as they are executed
set -o pipefail # fail if last(rightmost) command exits with a non-zero status


# Defines the variables that are needed for any communication with ECF
export ECF_PORT=%ECF_PORT%    # The server port number
export ECF_HOST=%ECF_HOST%    # The host name where the server is running
export ECF_NAME=%ECF_NAME%    # The name of this current task
export ECF_PASS=%ECF_PASS%    # A unique password
export ECF_TRYNO=%ECF_TRYNO%  # Current try number of the task
export ECF_RID=$$             # record the process id. Also used for zombie detection


# Define the path where to find ecflow_client
# make sure client and server use the *same* version.
# Important when there are multiple versions of ecFlow
export PATH=/usr/local/apps/ecflow/%ECF_VERSION%/bin:$PATH


# Tell ecFlow we have started
ecflow_client --init=$$

 
# Define a error handler
ERROR() {
   set +e                      # Clear -e flag, so we don't fail
   wait                        # wait for background process to stop
   ecflow_client --abort=trap  # Notify ecFlow that something went wrong, using 'trap' as the reason
   trap 0                      # Remove the trap
   exit 0                      # End the script
}

# On the Cray HPC link the output to the PBS output file, for watching the output while the job is running

if [[ $HOST = @(cc*) ]]; then
  _real_pbs_outputfile=/var/spool/PBS/spool/${PBS_JOBID}.OU
  _pbs_outputfile=/nfs/moms/$HOST${_real_pbs_outputfile}
  _running_output=%ECF_JOBOUT%.running
  ln -sf $_pbs_outputfile $_running_output 
fi

MARS_FOR_BOND_DATASET=%MARS_FOR_BOND_DATASET:345%

if [[ %MARS_DOUBLE_ARCHIVE:0% != 0 ]]; then 
  export MARS_DOUBLE_ARCHIVE=1
fi

if [[ %ECFS_DOUBLE_ARCHIVE:0% != 0 ]]; then
  export ECFS_DOUBLE_ARCHIVE=1
fi

if [[ %DRY_RUN:0% != 0 ]]; then
  export BOND_DHS_DRY_RUN_RETRIEVE=true
fi

# Trap any calls to exit and errors caught by the -e flag
trap ERROR 0


# Trap any signal that may cause the script to fail
trap '{ echo "Killed by a signal"; ERROR ; }' 1 2 3 4 5 6 7 8 10 12 13 15
