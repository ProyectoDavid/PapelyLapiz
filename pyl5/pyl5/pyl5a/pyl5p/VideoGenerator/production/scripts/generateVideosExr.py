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

# This script makes hi and low quality video files from EXR images, using blender's hidden sequencer api.

import os, time

def system_date():
	return time.localtime()[0:6]

def file_date(path):
	#currtime = (year, month, day, hour, min, sec)
	# year, month, day, hour, minute, second, weekday, yearday, daylight = now
	return time.localtime(os.stat(path)[8])[0:6]
		
# This script goes through all jpegs in the render dir and makes movies from them
def file_age(path):
	'''
	Total hack!
	'''
	tester = '/tmp/howoldami.tmp'
	os.system('touch "%s"' % tester)
	
	time_now = os.stat(tester)[8]
	time_path = os.stat(path)[8]
	
	return time_now-time_path




search = '/shared/render/'
svnrender_dir = '/shared/render/testrenders/'

ONLY_UPDATE = 1
RENDER = 1
# Use the age of exrs to make sure we dont do any renders for exrs that are being uploaded.
DOSVN=1


def main(DO_FINAL):
	
	first_frame = 1
	
	file_exrFolders = os.popen('find -L %s' % search).readlines() # -L is to read symlinks
	file_exrFolders.sort()
	
	if DOSVN:
		os.system('svn update "%s"' % svnrender_dir)
	
	dirs = {}
	
	errors = {}
	error_count = 0
	tot = len(file_exrFolders)
	
	# Get all folders containing jpegs
	for i, line in enumerate(file_exrFolders):
		line = line.strip()
		line_ok = False
		
		if DO_FINAL:
			if line.lower().endswith('.exr') and '/exr/final/' in line and '/old/' not in line and '/back/' not in line:
				line_ok = True
		else:
			if line.lower().endswith('.exr') and '/exr/' in line and '/old/' not in line and '/back/' not in line and '/final' not in line:
				line_ok = True
		
		if line_ok:
			#print 'Loading', line, str(int( (float(i)/tot) * 100.0 )) + '% done,  error count:', error_count
			if DO_FINAL:
				moviedir, filename = line.split('/exr/final/')
				moviedir += '/exr/final/'
			else:
				moviedir, filename = line.split('/exr/')
				moviedir += '/exr/'
			
			# Ok we have a path containing jpegs 
			# /shared/render/05_throwing/10/jpg/foo.jpg
			
			# Add a list for this folder if its not there.
			#if '09_' in moviedir and '_02' in moviedir:
			#	dirs.setdefault(moviedir, []).append(filename)
			
			
			dirs.setdefault(moviedir, []).append(filename)
	
	# For testing
	'''
	# remove all but 1
	print dirs.keys()
	
	KKeys = dirs.keys()
	for k in KKeys[1:]:
		del dirs[k]
	
	print dirs
	# return
	'''
	
	
	# Now render the frames
	import Blender
	Blender.Scene.Render.EnableDispView() 
	
	sce = Blender.Scene.GetCurrent()
	seq = sce.sequence
	
	# Settings for all scenes

	rend = sce.render
	rend.oversampling = True
	
	rend.OSALevel = 16 # We dont want to set this now.
	rend.threads = 2
	
	rend.motionBlur = False
	rend.fieldRendering = False
	
	rend.extensions = 1
	rend.renderwinSize = 100
	
	#rend.enableSky()
	#rend.enablePremultiply()
	#rend.enableKey()
	
	#rend.enableBWColor()
	rend.enableRGBColor()
	#rend.enableRGBAColor()
	
	rend.compositor = False
	rend.sequencer = True

	
	rend.xParts = 6
	rend.yParts = 6
	
	rend.fps = 24
	
	rend.touch = False
	rend.noOverwrite =False
	
	rend.imageType = Blender.Scene.Render.AVIJPEG
	
	RENDER_COUNT = 0
	for moviedir, files in sorted(dirs.items()):
		if len(files) > 1:
			#### fname = jpgdir.split('/')[-4] + '_' + jpgdir.split('/')[-3]
			
			
			
			if DO_FINAL:
				fname =   moviedir.split('/')[-5].split('_')[0] + '_' + moviedir.split('/')[-4]
				
				fname_hash = '%s../../../%s_final.hash' % (moviedir, fname)
				fname_avi = '%s../../../%s_final.avi' % (moviedir, fname)
				fname_avi_hi = '%s../../../%s_final_hi.avi' % (moviedir, fname)
			else:
				fname =   moviedir.split('/')[-4].split('_')[0] + '_' + moviedir.split('/')[-3]
				
				fname_hash = '%s../../%s.hash' % (moviedir, fname)
				fname_avi = '%s../../%s.avi' % (moviedir, fname)
				fname_avi_hi = '%s../../%s_hi.avi' % (moviedir, fname)
			
			# Check if we need to render the avi, is the avi older then any of the exr's?
			if ONLY_UPDATE:
				# Generate a hash from all the exrs
				filehash = long(0) # Any longer and it will be a long! - just a hope the number wont get too huge.
				for f in files:
					filehash += os.stat(os.path.join(moviedir, f))[8]
				
				if os.path.exists(fname_hash):
					filehash_last = long(open(fname_hash, 'r').read().strip())
				else:
					filehash_last = -1
				
			else:
				filehash = -1
				filehash_last = -1
			
			print moviedir, filehash, filehash_last

			
			if not ONLY_UPDATE or filehash != filehash_last:
				print "Different hash!"
				
				# TODO - dont make avi while rendering!
				
				if 1:
					files.sort()
					strip = seq.new( (moviedir, files), first_frame, 1 )
					strip.name = fname
					#seq.start = first_frame
				
					# print fname 
					
					if RENDER:
						rend.sFrame= first_frame
						rend.eFrame= first_frame + (len(files) - 1)
						
						# render high
						rend.renderPath = fname_avi_hi
						rend.quality(95)			
						rend.sizeX = 1920
						rend.sizeY = 1080
						rend.renderAnim()
						print 'render', fname_avi_hi
						RENDER_COUNT+=1
						
						# render low
						rend.renderPath = fname_avi
						rend.quality(60)
						rend.sizeX = 960
						rend.sizeY = 540
						rend.renderAnim()
						print 'render', fname_avi
						RENDER_COUNT+=1
						
						# log the 
						avidate = '"' + fname_avi.split('/')[-1] + ' --- yr:%s, month:%s, day:%s, hr:%s, min:%s, sec:%s"' % tuple(file_date(fname_avi))
						os.system('echo %s >> /shared/render/log_video.txt' % avidate)
						
						# Commit to svn!
						if DOSVN and DO_FINAL:
							#os.system( 'cp "%s" "%s"' % (fname_avi, svnrender_dir))
							
							# fname_avi_rename = fname_avi
							fname_avi_rename = fname_avi.replace('_final', '')
							
							os.system( 'cp "%s" "%s/%s"' % (fname_avi, svnrender_dir, fname_avi_rename.split('/')[-1].split('\\')[-1] ) ) # only for finals
							# print "TEST222:", svnrender_dir_rename
							
							os.system( 'svn add %s/%s' % ( svnrender_dir, fname_avi_rename.split('/')[-1].split('\\')[-1] ) )
							os.system( 'svn commit %s/%s --message "automatic_commit"' % ( svnrender_dir, fname_avi_rename.split('/')[-1].split('\\')[-1] ) )
						
						# Write the hash
						open(fname_hash, 'w').write(str(filehash))
						
					
			
			first_frame += len(files)
	print RENDER_COUNT

if __name__ == '__main__':
	main( 1 ) # render finals
	main( 0 ) # render normally
		
		
		
		
