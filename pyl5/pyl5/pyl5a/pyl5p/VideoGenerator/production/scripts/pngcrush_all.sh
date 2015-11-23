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

# This script crushes all PNG's in the current directory with a fairly high compression

TMPPNG="/tmp/temp_pngcrush.png"
for f in `find . -iname "*.png" | sort`
do
	echo $f
	pngcrush -brute -l 9 -z 1 "$f" "$TMPPNG"
	mv "$TMPPNG" "$f"
	# exit 0
done
