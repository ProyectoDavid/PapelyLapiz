#!/bin/bash

# Wavemage
cd /

# PEACHROOT=~/production # use wavemages account
PEACHROOT=/media/data/peach/production # Normal users

REND=/shared/render

JOBS=`find $PEACHROOT/jobs -iname "*.job"`

for j in $JOBS
do
	# Generate job file
	echo $blen
	python $PEACHROOT/scripts/validateJob.py $j $REND
done
