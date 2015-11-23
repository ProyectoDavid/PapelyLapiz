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
This script find images in the project directory that arnt used in any blend files. only TGA and PNG images at the moment.
'''

import os



tempf = '/tmp/blenLibChecker.temp'
blends = '/tmp/blenLibCheckerFiles.temp'
search = '/media/data/peach/production'


def main():
	
	# Get images first
	os.system('find %s -name "*.png" > %s' % (search, blends))
	os.system('find %s -name "*.tga" >> %s' % (search, blends))
	file_images = open(blends, 'r').readlines()
	file_images = [ f.split('/')[-1].strip() for f in file_images ]
	
	
	
	os.system('find %s -name "*.blend" > %s' % (search, blends))

	file_blends = open(blends, 'r').readlines()
	
	
	errors = {}
	error_count = 0
	error_path = []
	tot = len(file_blends)
	for i, line in enumerate(file_blends):
		line = line.strip()
		print 'Loading', line, str(int( (float(i)/tot) * 100.0 )) + '% done,  error count:', error_count
		
		line = line.strip()
		#os.system('export ')
		
		
		# RUN Blender to find Library errors AND run a script that looks broken paths!
		## os.system('LD_LIBRARY_PATH=/shared/software/exr/lib /render/blender_$(whoami)/blender/blender -b %s 1> %s 2>&1' % (line, tempf))
		
		
		pyscript = search + '/scripts/printLocalImages.py'
		# Also run a py script
		os.system('LD_LIBRARY_PATH=/shared/software/exr/lib /render/blender_$(whoami)/blender/blender -b %s   -P %s   1> %s 2>&1' % (line, pyscript, tempf))
		
		
		
		#os.system('/render/blender_$(whoami)/blender/blender -b %s')
		file_lib = open(tempf, 'r')
		
		context_lib = None
		for out_line in file_lib.readlines():
			if out_line.startswith('IMG: ') : # Py Script makes this one
				errors.setdefault(out_line.strip().split()[-1], [0])[0] += 1
				error_count+=1
	
	
	# Repor errors
	items = errors.items()
	items.sort(key = lambda a: -a[1][0])

	for im, count in items:
		
		try:
			file_images.remove(im)
		except:
			pass
		
		#if im not in file_images:
		#	print "HoooBar", im
	
		print im, count
		
	for im in file_images:
		print im, 'ZERO'
	
	os.system('rm ' + tempf)
	os.system('rm ' + blends)
	

main()
