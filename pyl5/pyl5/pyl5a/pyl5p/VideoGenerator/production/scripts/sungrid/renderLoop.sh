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

# Runs on the sungrid, render the movie in a loop
#
# * Waits until queue is finished
# * Downloads EXR frames
# * Updates SVN
# * Render all the files tagged to render

QUEUE="$HOME/production/jobs/queue.job"
cd ~
while [ 1 ] ; do
	echo "render movie..."
	
	# Only add to the queue if the
	QCOUNT=$(qstat -u $USER | grep $USER | grep -iv interact | wc -l)
	echo "Queue At Number "$QCOUNT
	
	while [ "$QCOUNT" -gt "0" ]
	do
		echo "Queue Full, cant render anything until finished... "$QCOUNT
		sleep 60
		QCOUNT=$(qstat -u $USER | grep $USER | grep -iv interact | wc -l)
	done
	
	# reuse QCOUNT to see if frames downloaded.
	QCOUNT=$(ls *.exr | wc -l)
	while [ "$QCOUNT" -gt "0" ]
	do
		echo "Downloading EXR frames still, waiting to finish before rendering more... "$QCOUNT
		sleep 60
		QCOUNT=$(ls *.exr | wc -l)
	done
		
	echo "Updating movie!"
	bash ./up_movie.sh
	
	
	QUEUECOUNT=$(cat $QUEUE | wc -l)
	
	sleep 1
	if [ ! "$QUEUECOUNT" -eq "0" ] ; then
		echo "Rendering queue!"
		echo $QUEUECOUNT
		./commandBatch.sh $QUEUE
	fi
	sleep 60
done

### # Simple
### /opt/sfw/bin/rsync --progress -ave 'ssh -p 80' *.exr  wavemage@blender3d.dyndns.org:/shared/render/
