'''
 * ***** BEGIN GPL LICENSE BLOCK *****
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software Foundation,
 * Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 *
 *
 * Contributor(s): Campbell Barton
 *
 * ***** END GPL LICENSE BLOCK *****
'''

'''
This script prints files that have absolute paths or missing files
'''

import Blender
'''
paths = Blender.GetPaths(1)
for f in paths:
	if f.lower().endswith('.blend'):
		continue
	
	if not Blender.sys.exists(f):
		print "ERROR PATH:", f
'''
import bpy

expandpath = Blender.sys.expandpath
exists = Blender.sys.exists
for i in bpy.data.images:
	if not i.lib:
		name = i.name
		if 'Viewer Node' in name or 'Render Result' in name or 'Untitled' in name:
			continue
		
		filename = i.filename
		if not filename.startswith('//'):
			print "ABSOLUTE PATH:", name, filename
		
		if not exists(expandpath(filename)):
			print "ERROR PATH:", name, filename, 'ABS:', expandpath(filename)
	
	