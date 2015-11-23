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

# This script runs blender on solaris with a bundeled python and openGL

export NAN_BLENDERHOME=$PWD
export NAN_BLENDEROUT=${NAN_BLENDERHOME}/render
export LD_LIBRARY_PATH=/usr/local/lib:/usr/X11/lib:${NAN_BLENDERHOME}/lib
export PYTHONHOME=${NAN_BLENDERHOME}/pythonhome

echo $LD_LIBRARY_PATH
echo $NAN_BLENDERHOME

$NAN_BLENDERHOME/bin/blender