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

# This script is a simpler version of the script which was used to render many images on sun's network.com
# all blend files and frames listed in "blender.in" will be rendered.

if [ -f $HOME/.profile ]; then
  . $HOME/.profile
fi

ifile=blender.in
[ ! -f $ifile ] && exit

while read line_iter
do
  echo "Running" $line_iter
  EXITSTATUS="1"
  while [ ! "$EXITSTATUS" -eq 0 ]
  do
    qsub -N Blender -cwd blenderBatchItem.sh $line_iter
    
    # Deal with failed attempts to add a job.
    EXITSTATUS="$?"
    if [ ! "$EXITSTATUS" -eq 0 ]
    then
      echo "Failed to add job, sleeping 10sec and try again..."
      sleep 10
    fi
    
  done
  
done < $ifile

echo "done"
