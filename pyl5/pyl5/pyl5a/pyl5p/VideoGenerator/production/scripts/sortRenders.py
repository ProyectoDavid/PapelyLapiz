#!/usr/bin/python
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
This script moved EXR images downloaded from the renderfarm into
their subdirectories on the local harddisk
'''


# Sorts images into dirs
print "Running Sort Render"
import os
import time
RENDER='/shared/render/'

DO_VALIDATE_EXR = True
TMPEXR='/tmp/blender_tmp.exr'


if DO_VALIDATE_EXR:
	os.system('rm "%s"' % TMPEXR)
		
def validate_exr(path):
	os.system('exrmakepreview "%s" "%s"' % (path, TMPEXR))
	if not os.path.exists( TMPEXR ):
		return False
	
	os.system( 'rm "%s"' % TMPEXR )
	return True

def file_split(f):
	# 10_chinchilla-03_0001.exr -> 10_chinchilla, 03
	# 
	
	f = f.replace('.exr', '')
	frame = f.split('_')[-1]
	f = f[:-(len(frame)+1)]
	shot = f.split('-')[-1]
	f = f[:-(len(shot)+1)]
	return f, shot, frame

def filename_2_path(f):
	f, shot, frame = file_split(f)
	path = os.path.join(RENDER, f)
	path = os.path.join(path, shot)
	return path

def file_date(path):
	#currtime = (year, month, day, hour, min, sec)
	# year, month, day, hour, minute, second, weekday, yearday, daylight = now
	return time.localtime(os.stat(path)[8])[0:6]

def main():
	
	files_orig = [f for f in os.listdir(RENDER) if f.endswith('.exr')]
	
	if DO_VALIDATE_EXR:
		# Only move exr files if they can be read, else name exr.bad
		files = []
		for f in files_orig:
			path_from = os.path.join(RENDER, f)
			if validate_exr(path_from):
				files.append(f)
			else:
				os.system('mv "%s" "%s.bad"' % (path_from, path_from))
		
	else:
		files = files_orig
	
	
	for f in files:
		path_from = os.path.join(RENDER, f)
		
		path_to = os.path.join(filename_2_path(f), 'exr')
		path_old = os.path.join(path_to, 'old/')
		path_existing_dont_overwrite = os.path.join(path_to, f)
		if os.path.exists( path_existing_dont_overwrite ):
			os.system( 'mkdirhier %s' % path_old )
			os.system( 'mv %s %s' % (path_existing_dont_overwrite, path_old) )
		
		# Log the file as rendered.
		
		exrdate = '"' + f + ' --- yr:%s, month:%s, day:%s, hr:%s, min:%s, sec:%s"' % tuple(file_date(path_from))
		os.system('echo %s >> /shared/render/log.txt' % exrdate)
		
		move_cmd = 'mv %s %s' % (path_from, path_to)
		os.system( 'mkdirhier %s' % path_to )
		
		print 'mv %s %s' % (path_from, path_to)
		os.system( move_cmd )
		
		try:
			os.system( 'chmod 777 ' + path_to + '/*.exr')
		except:
			print 'could not chmod', path_to


main()
