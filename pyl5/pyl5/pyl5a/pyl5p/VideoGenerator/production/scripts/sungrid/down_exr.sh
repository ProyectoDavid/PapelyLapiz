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

# Download EXR's in a loop and copy them to the correct locations

TMPFILE="$HOME/exr.tmp"
cd ~
while [ 1 ] ; do
	echo "down exr..."
	ls -1 *.exr > $TMPFILE
	#ls -1 ~/_* > $TMPFILE
	
	EXRCOUNT=$(cat $TMPFILE | wc -l)
	sleep 8
	if [ ! "$EXRCOUNT" -eq 0 ] ; then
		
		chmod 777 *.exr
		
		/opt/sfw/bin/rsync --progress --files-from=$TMPFILE -ave 'ssh -p 80' ./ wavemage@blender3d.dyndns.org:/shared/render/
		
		# Be careful, dont remove files if rsync didnt finish.
		if [ "$?" -eq 0 ] ; then
			for f in `cat $TMPFILE` ; do
				rm $f
			done
		fi
		
		# Sort render images into correct dirs
		ssh wavemage@blender3d.dyndns.org -p 80 'python /home/wavemage/production/scripts/sortRenders.py'
		
		# Download logs, these will need manual removal
		/opt/sfw/bin/rsync --progress -ave 'ssh -p 80' _*.*  wavemage@blender3d.dyndns.org:/shared/render/logs/
		
	fi
	sleep 60
done

### # Simple
### /opt/sfw/bin/rsync --progress -ave 'ssh -p 80' *.exr  wavemage@blender3d.dyndns.org:/shared/render/
