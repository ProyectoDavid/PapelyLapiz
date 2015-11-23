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
A simple script that makes a 'blendname.job' file in the current directory, by reading the blend file header.
'''

# -------------------------- copied from bpymodule/blend2renderinfo.py!
import struct
def read_blend_rend_chunk(path):
	file = open(path, 'rb')
	
	if file.read(len('BLENDER')) != 'BLENDER':
		return []
	
	# 
	if file.read(1) == '-':
		is64bit = True
	else: # '_'
		is64bit = False

	if file.read(1) == 'V':
		isBigEndian = True # ppc
	else: # 'V'
		isBigEndian = False # x86
	
	
	# Now read the bhead chunk!!!
	file.read(3) # skip the version
	
	scenes = []
	
	while file.read(4) == 'REND':
	
		if is64bit:		sizeof_bhead = sizeof_bhead_left = 24 # 64bit
		else:			sizeof_bhead = sizeof_bhead_left = 20 # 32bit
	
		sizeof_bhead_left -= 4
		
		if isBigEndian:	rend_length = struct.unpack('>i', file.read(4))[0]
		else:			rend_length = struct.unpack('<i', file.read(4))[0]
		
		sizeof_bhead_left -= 4
		
		# We dont care about the rest of the bhead struct
		file.read(sizeof_bhead_left)
		
		# Now we want the scene name, start and end frame. this is 32bites long
		
		if isBigEndian:	start_frame, end_frame = struct.unpack('>2i', file.read(8))
		else:			start_frame, end_frame = struct.unpack('<2i', file.read(8))
		
		scene_name = file.read(24)
		scene_name = scene_name[ : scene_name.index('\0') ]
		
		scenes.append( (start_frame, end_frame, scene_name) )
	return scenes
# ------------------------ end copy





# use this to generate jobs for suns renderfarm
# python blend2job.py my.blend

def write_job(job_name, frel, sce, name, i, output_file, camera_name):
	
	# output_file not used yet
	
	s = 'qsub -N _%s -cwd blenderBatchItem.sh %s ' % (job_name, frel)
	if sce:
		s += '-S %s ' % sce
	
	s += '-P ./production/scripts/render_settings.py -o %s_ -f %i ' % (name, i)
	
	
	if camera_name != None:
		s += ' -- '
		s += camera_name
	
	s += '\n'
	return s

import sys
import os
def main_func():

	ROOT_PATH = 'production' # relative to the first instance of this path
	EXT = 'exr'

	blend_args = [arg for arg in sys.argv if arg.lower().endswith('.blend')]
	# f = blend_args[-1]
	
	
	
	for f in blend_args:
		
		file_lines = []
		
		# Linux + peach spesific
		frel = f.split(ROOT_PATH)[-1]
		frel = './' + ROOT_PATH + frel

		# second last path + filename
		# /01_intro/04.blend  -->  01_intro-04
		name = f.split('/')[-2] + '-' + f.split('/')[-1].split('.')[0]
		
		
		jobfn = name + '.job' # Job filename "01_intro-04.job"
		jobfn_part = name + '_part.job' # Job filename "01_intro-04_part.job"    - use for partial update
		
		
		# Ok, this text file defines start and end frames
		f_options = f.replace('.blend', '.txt')
		if os.path.exists( f_options ):
			options = [ opt.strip() for opt in open( f_options ).readlines() ]
			# options.split()
			
			frame_ranges = []
			camera_changes = []
			
			for opt in options:
				opt = opt.strip()
				if not opt:
					continue
				opt_words = opt.split()
				if len(opt_words) != 2: continue
				s = int( opt_words[0] )
				cam_name = None
				try:
					e = int( opt_words[1] )
					frame_ranges.append( (s,e) )
				except:
					cam_name = opt_words[1].strip()
					camera_changes.append( (s, cam_name) )
			
			frame_ranges.sort()
			camera_changes.sort()
			
			if not frame_ranges:
				tmp_data = read_blend_rend_chunk(f)
				if len(tmp_data) != 1:
					print "ERROR: Undefined render frame ranges"
				# This kindof sucks since there could be a number of frame ranges!
				frame_ranges.append( tmp_data[0][0:2] )
			
			for s, e in frame_ranges:
				sce = None # dont set
				
				# We need this for making the job name
				digit_len = max(4, len(str(e)))
				
				for i in xrange(s,e+1):
					
					camera_name = None
					if camera_changes:
						for frame, nm in camera_changes:
							if frame <= i:
								camera_name = nm
							else:
								break
					
					# Make the job name
					frame_string = str(i)
					job_name = name + '_' + frame_string.zfill(digit_len)
					
					output_file = job_name + '.' + EXT

					file_lines.append( ( output_file, write_job(job_name, frel, sce, name, i, output_file, camera_name)) )
			
			
		else:
			for s, e, sce in read_blend_rend_chunk(f):
				
				print "\tscene:", sce
				
				if sce != 'comp':
					print 'WARNING! a scene other then "comp" is rendering'
				
				# We need this for making the job name
				digit_len = max(4, len(str(e)))
				
				for i in xrange(s,e+1):
					
					# Make the job name
					frame_string = str(i)
					job_name = name + '_' + frame_string.zfill(digit_len)
					output_file = job_name + '.' + EXT
					
					# Use a py script for scene setup
					file_lines.append( ( output_file, write_job(job_name, frel, sce, name, i, output_file, None)) )
		
		file = open(jobfn, 'w')
		for nm, line in file_lines:
			file.write(line)
		file.close()
		
		# Should we write a partial render job??
		
		# Make sure this dosnt screw up! we are predicting the render path that files are copied to, this cant chantge.
		
		
		#frel_dir = os.path.split(f)[0]
		
		frel_dir = f.replace('.blend', '/exr') # turn the blend file into a path name.
		frel_dir = '/shared/render/' + frel_dir.split(ROOT_PATH + '/scenes/')[-1]
		
		# Ok, the dir is now somthing like
		# /shared/render/12_peach/17
		os.system("mkdirhier %s" % frel_dir)
		
		existing_files = os.listdir(frel_dir)
		try:		existing_files = os.listdir(frel_dir)
		except:		existing_files = []
		
		# print existing_files
		
		if existing_files:
			done_count = 0
			file_lines_part = []
			for nm, line in file_lines:
				if nm in existing_files:
					done_count += 1
				else:
					file_lines_part.append( (nm, line) )
			
			if file_lines_part and done_count != 0:
				
				file = open(jobfn_part, 'w')
				for nm, line in file_lines_part:
					file.write(line)
				file.close()
			
		'''
		for nm, line in file_lines:
			if nm not in 
			file.write(line)
		'''
		
		print jobfn, 'written in $PWD'

if __name__ == '__main__':
	main_func()
