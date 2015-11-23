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
This script makes 2 directories of EXR images have the same names by
applying the first directories names to the secont dir.
'''

import sys
import os

def main_func():
	if len(sys.argv) < 3:
		print "give 2 dirs as args: SOURCE TARGET"
	
	dir_src = sys.argv[-2]
	dir_tar = sys.argv[-1]
	
	f_src = [f for f in os.listdir(dir_src) if f.endswith('.exr')]
	f_tar = [f for f in os.listdir(dir_tar) if f.endswith('.exr')]
	
	if len(f_src) != len(f_tar):
		print "difference in file count in each dir!", len(f_src), len(f_tar)
	
	f_src.sort()
	f_tar.sort()
	
	for i in xrange(len(f_src)):
		src = os.path.join(dir_src, f_src[i])
		tar = os.path.join(dir_src, f_tar[i])
		os.system('mv "%s" "%s"' % (src, tar) )

if __name__ == '__main__':
	main_func()
