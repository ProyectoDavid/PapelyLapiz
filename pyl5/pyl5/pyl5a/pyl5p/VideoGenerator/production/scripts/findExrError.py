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
This script validates EXR images are not corrupt, prints EXR's that have errors
'''

import os
search = '/shared/render/'
tmpexr = '/tmp/test.exr'

# Get all exr files that arnt in /old/
exr_files = [ l.strip() for l in os.popen('find ' + search + ' -iname "*.exr"').readlines() if '/old/' not in l ]


#usage: exrmakepreview [options] infile outfile
exr_error = []
for i, exr in enumerate(exr_files):
	
	print 'Validating EXR', exr, int(100 * (float(i) / len(exr_files))), '%'
	
	os.system( 'rm "%s"' % tmpexr )
	os.system( 'exrmakepreview "%s" "%s"' % (exr, tmpexr) )
	if not os.path.exists( tmpexr ):
		print "\tERROR, report later!"
		exr_error.append( exr )

print "exr errors"
for exr in exr_error:
	print exr
		
	
	
	
	
	
	
