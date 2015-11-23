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

# This script generates renderfarm job files for the peach projects blend files

# Wavemage
cd /

PEACHROOT=~/production # use wavemages account
# PEACHROOT=/media/data/peach/production # Normal users

BLENDS=`find $PEACHROOT/scenes -iname "*.blend"`


mkdir $PEACHROOT/jobs
rm $PEACHROOT/jobs/*.job
cd $PEACHROOT/jobs


for blen in $BLENDS
do
	# Generate job file
	echo $blen
	python $PEACHROOT/scripts/blend2job.py $blen
done

# Done generating job files! Now make a job for all frames we need to render based on svn.
# This makes a job $PEACHROOT/queue.job
python $PEACHROOT/scripts/svnCheckRenders.py $PEACHROOT/jobs/queue.job


