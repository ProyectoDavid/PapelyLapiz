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

# This script runs blender in background mode with "renderLogView.blend"
# to generate an image of the renderfarm's progress

export LD_LIBRARY_PATH=/shared/software/exr/lib/
CURRENT="/shared/render/logs_img/current.png"

# Hack, dont make an animation!
DATE=$(date +%Y%m%d%H%M%S)-

while [ 1 ]  ; do
	# Uncomment if you want to record every update.
	# DATE=$(date +%Y%m%d%H%M%S)-
	~/blender -b ~/production_nobackup/scripts/renderLogView.blend -P Text.001 -o /shared/render/logs_img/$DATE -f 1
	rm $CURRENT
	ln -s /shared/render/logs_img/$DATE"0001.png" $CURRENT
	sleep 20
done