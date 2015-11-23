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
This script goes through loading blend files and reporting any library errors they have in a useful way
Run every once in a while to chack the validity of the movies blend files
'''

import os

tempf = '/tmp/blenLibChecker.temp'
blends = '/tmp/blenLibCheckerFiles.temp'

outfile = '/shared/peach/missing_lib.txt'

# search = '/media/data/peach/production'
search = '/home/wavemage/production_nobackup'

# blender_bin = '/render/blender_$(whoami)/blender/blender'
blender_bin = '/home/wavemage/blender'

VERBOSE = True

def main():
	os.system('find %s -name "*.blend" > %s' % (search, blends))
	
	file_blends = open(blends, 'r').readlines()
	
	errors = {}
	error_count = 0
	error_path = []
	tot = len(file_blends)
	for i, line in enumerate(file_blends):
		line = line.strip()
		
		if VERBOSE:
			print 'Loading', line, str(int( (float(i)/tot) * 100.0 )) + '% done,  error count:', error_count
		
		line = line.strip()
		#os.system('export ')
		
		
		# RUN Blender to find Library errors AND run a script that looks broken paths!
		## os.system('LD_LIBRARY_PATH=/shared/software/exr/lib /render/blender_$(whoami)/blender/blender -b %s 1> %s 2>&1' % (line, tempf))
		
		
		pyscript = search + '/scripts/findPathError.py'
		# Also run a py script
		os.system('LD_LIBRARY_PATH=/shared/software/exr/lib %s -b %s   -P %s   1> %s 2>&1' % (blender_bin, line, pyscript, tempf))
		
		#os.system('/render/blender_$(whoami)/blender/blender -b %s')
		file_lib = open(tempf, 'r')
		
		context_lib = None
		for out_line in file_lib.readlines():
			if out_line.startswith('ERROR PATH: ') or out_line.startswith('ABSOLUTE PATH: '): # Py Script makes this one
				context_lib = out_line.strip()
				errors.setdefault(line, ({}, []))[1].append(out_line.strip())
				error_count += 1
			elif out_line.startswith('read library: '):
				context_lib = out_line.strip()
			elif out_line.startswith('LIB ERROR: '):
				errors.setdefault(line, ({}, []))[0].setdefault(context_lib, []).append(out_line.strip())
				error_count += 1
	
	
	# Repor errors
	out = open(outfile, 'w')
	
	for blenfile, blenfile_dict_and_pics in errors.iteritems():
		out.write('BLENFILE: ' + blenfile + '\n')
		for libfile, errorls in blenfile_dict_and_pics[0].iteritems():
			out.write('\tLIBFILE: ' + libfile + '\n' )
			for err in errorls:
				out.write( '\t\t: ' + err + '\n')
		for file in blenfile_dict_and_pics[1]:
			out.write('\t' + file + '\n')
	
	os.system('rm ' + tempf)
	os.system('rm ' + blends)
	

main()
