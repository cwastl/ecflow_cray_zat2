#!/bin/ksh

#date=20190422

#curdate=$(date '+%%Y%%m%%d');
date=$(date '+%Y%m%d')
date=20190725
run=06
leadtime=60
lagg=6

blocks=6
ii=0
(( triggert=${leadtime}/2 + ${lagg} ))
echo $triggert
#while (( $ii <= $lead )); do
#   (( block = ( ${ii} - 1 ) / $blocks + 1 ))
#   (( ii = $ii + 1 ))
#   echo $block
#done
