#!/bin/bash

 #~ * ***** BEGIN GPL LICENSE BLOCK *****
 #~ *
 #~ * This program is free software; you can redistribute it and/or
 #~ * modify it under the terms of the GNU General Public License
 #~ * as published by the Free Software Foundation; either version 2
 #~ * of the License, or (at your option) any later version.
 #~ *
 #~ * This program is distributed in the hope that it will be useful,
 #~ * but WITHOUT ANY WARRANTY; without even the implied warranty of
 #~ * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #~ * GNU General Public License for more details.
 #~ *
 #~ * You should have received a copy of the GNU General Public License
 #~ * along with this program; if not, write to the Free Software Foundation,
 #~ * Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 #~ *
 #~ *
 #~ * Contributor(s): Campbell Barton
 #~ *
 #~ * ***** END GPL LICENSE BLOCK *****

# This script runs jobs on suns network.com, limiting the maximum number of
# jobs to avoid problems with many blenders accessing files at once.

if [ -f $HOME/.profile ]; then
	. $HOME/.profile
fi

ifile=$1 # Use first argument
[ ! -f $ifile ] && exit

# Dont allow to run without Blender
[ ! -f ~/bin/blender ] && exit

DONE_LOG=$ifile".done"
MAX_QUEUE="6"

rm $DONE_LOG

while read line_iter
do
	# Only add to the queue if the
	QCOUNT=$(qstat -u $USER | grep $USER  | grep -iv interact | grep qw | wc -l)
	echo "Queue At Number "$QCOUNT
	
	while [ "$QCOUNT" -gt "$MAX_QUEUE" ]
	do
		echo "Queue Full, sleeping..."
		sleep 2
		QCOUNT=$(qstat -u $USER | grep $USER | grep -iv interact | grep qw | wc -l)
	done
	
	echo "Running" $line_iter
	EXITSTATUS="1"
	while [ ! "$EXITSTATUS" -eq 0 ]
	do
		# This line should contain the qsub command!
		$line_iter
		
		
		##### echo "PRETEND TO RENDER!!!"
		##### echo $line_iter
		
		sleep 1
		# Deal with failed attempts to add a job.
		EXITSTATUS="$?"
		if [ ! "$EXITSTATUS" -eq 0 ]
		then
			echo "Failed to add job, sleeping 5sec and try again..."
			sleep 5
		fi
	done
	
	# Log as done
	echo $line_iter >> $DONE_LOG

done < $ifile

echo "done"
