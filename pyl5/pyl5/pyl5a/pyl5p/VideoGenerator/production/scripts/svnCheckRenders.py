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
Check the peach SVN commit log for a DORENDER command, from andy, if there is one,
the commited files are rendered on the renderfarm. as long as the do-render command
is more recent then the dates of any existing EXR files.
'''

import os
import time
import sys



try:
	RENDER_JOB = [arg for arg in sys.argv if arg.lower().endswith('.job')][0]
except:
	RENDER_JOB = None

RENDER_PATH = '/shared/render/'
SVN_PATH = 'svn://biserver/peach/production/scenes'
#SVN_RENDER_DUDE = 'ideasman42'
SVN_RENDER_DUDE = 'andy' # Only andy can render stuff!
SVN_RENDER_CMD = 'DORENDER'
SVN_PEACHROOT='/home/wavemage/'

"""
RENDER_LOG ='/shared/render/render.log'
render_log_dict = {}
for line in open(RENDER_LOG, 'r').readlines():
	line = line.lower().split()
	if len(line)==2:
		if line[0] in render_log_dict:
			if render_log_dict[line[0]] < int(line[1]): # if this is older?
				render_log_dict[line[0]] = int(line[1])
		else:
			render_log_dict[line[0]] = int(line[1])
"""

def file_date(path):
	#currtime = (year, month, day, hour, min, sec)
	# year, month, day, hour, minute, second, weekday, yearday, daylight = now
	return time.localtime(os.stat(path)[8])[0:6]

def main():
	# RENDER_LOG simple format, blend name then revision number
	# 01_01.blend 19234
	
	if RENDER_JOB==None:
		print "Must give a .job as an argument"
		return
	
	render_cmd_dates = {} # key is the name, (no blend), value is the most recent time it was requested to render. 


	lines = [line.strip() for line in os.popen('svn log --verbose --xml %s' % SVN_PATH ).readlines()]
	i = len(lines)
	while i:
		i -= 1;
		while not lines[i-1].endswith('>'):
			lines[i-1] += ' ' + lines.pop(i)

	render_user = False
	render_files = []
	render_revision = -1
	for line in lines:
		#continue
		# print line
		if line.startswith('<logentry revision='):
			# <logentry revision="1895">
			render_revision = int( line.split('"')[1] )
		if line.startswith('<author>'):
			# <author>env</author>
			if SVN_RENDER_DUDE in line:	render_user = True
			else:						render_user = False
			render_files = []
		
		# render_revision is easier then date
		
		elif render_user and line.startswith('<date>'):
			date, time = line.replace( '<date>', '' ).replace( '</date>', '' ).split('T')
			year, month, day = [int(i) for i in date.split('-')]
			hour, min, sec = [float(i.replace('Z', '')) for i in time.split(':')]
			
			# NOTE HOUR-1 is for python compat which starts at 0?
			currtime = (year, month, day, hour+1, min, sec)
			# print year, month, day, hour, min, sec

		elif render_user and line.startswith('<path '):
			#  <path action="M">/production/scenes/12_peach/06.blend</path> 
			# to
			#  /production/scenes/12_peach/06.blend
			filename = line[1:-1].split('>')[1].split('<')[0]
			
			if filename.endswith('.blend'):
				render_files.append( filename )
		
		elif render_user and line.startswith('<msg>'):
			message = line.replace( '<msg>', '' ).replace( '</msg>', '' ).upper()
			# if SVN_RENDER_CMD in message:
			
			if SVN_RENDER_CMD in message:
				# print  message
				# print 
				if not render_files:
					print "No blend files commited!"
				else:
					for file in render_files:
						'''
						file = file.split('\\')[-1].split('/')[-1].lower()
						
						if file in render_log_dict:
							if render_log_dict[file] < render_revision:
						'''
						
						
						#file = file.split('\\')[-1].split('/')[-1].replace('.blend', '')
						
						
						# /home/wavemage/production/scenes/05_throwing/01.blend
						# to
						# 05_throwing, 01
						
						file_scene, file_shot = file.replace('.blend', '').split('/')[-2:] # UNIX Only, sorry MS :/
						
						file_sce_sht = (file_scene, file_shot)
						
						if file_sce_sht in render_cmd_dates:
							if currtime > render_cmd_dates[file_sce_sht]:
								render_cmd_dates[file_sce_sht] = currtime
						else:
							render_cmd_dates[file_sce_sht] = currtime
								
						
				
			
	# Ok, Now work out which frames arnt rendered.
	
	# Util function to know what frame were rendering
	def exr_framenum(exr):
		# print exr
		
		
		# /blah/blah/08_a-team-07_0013.exr    ->     13
		exr = exr.split('\\')[-1].split('/')[-1]
		exr = exr.replace('.exr', '')
		exr = exr.split('_')[-1]
		return int(exr)
	
	def job_framenum(jobtxt):
		# Get the framenumber from the job
		# qsub -N _04_rodents-01_0062 -cwd blenderBatchItem.sh ./production/scenes/04_rodents/01.blend -S comp -P ./production/scripts/render_settings.py -o 04_rodents-01_ -f 62
		
		jobtxt = jobtxt.split(' -f ')[1]
		jobtxt = jobtxt.split()[0]
		return int(jobtxt)
	
	out_job = open(RENDER_JOB, 'w')
	
	exr_files_main = os.popen('find "%s" -name "*.exr"' % RENDER_PATH).readlines()
	exr_files_main = [l.strip() for l in exr_files_main if '/old/' not in l if '/back/' not in l if '/final' not in l] 
	
	
	#print exr_files_main
	def exr_file_contains_name(basename, path):
		path = path.split('/')[-1] # remove path
		# remove _0001.exr
		path = '_'.join(path.split('_')[:-1])
		
		return basename == path
	
	for file_sce_sht, commit_time in render_cmd_dates.iteritems():
		# 05_throwing, 01  ->  05_throwing_01 
		file_sce_sht_text = '-'.join(file_sce_sht) 
		
		# get exrs that have the blend file name in them.
		print "file_sce_sht_text", file_sce_sht_text
		exr_files = [l for l in exr_files_main if exr_file_contains_name(file_sce_sht_text, l)]
		
		# Are any files where? if not add this to the queue.job file
		file_job_name = SVN_PEACHROOT + '/production/jobs/' + file_sce_sht_text + '.job'
		try:	file_job = open(file_job_name, 'r')
		except:	file_job = None
		if file_job == None:
			print 'could not open job file "%s"' % file_job_name
		else:		
			if not exr_files:
				### print "NO ExISTING FILES", file_sce_sht_text
				# Write all files!
				out_job.writelines(l.strip() + '\n' for l in file_job.readlines() if l.strip())
			else:
				### print "SOME ExISTING FILES", file_sce_sht_text
				# Ok we have some files, check that
				# First build a dictionary of ExR files we have,
				exr_frame_dict = dict([(exr_framenum(exr), exr) for exr in exr_files])
				job_frames_items = [(job_framenum(l), l.strip()) for l in file_job.readlines() if l.strip()]
				
				for job_frame, job_line in job_frames_items:
					if job_frame not in exr_frame_dict:
						out_job.write( job_line + '\n' )
					else:
						exr = exr_frame_dict[job_frame]
						exr_currtime = file_date(exr)
						#print exr_currtime
						#print commit_time
						if commit_time > exr_currtime:
							print "ReRender", job_line.split()[2]
							print '\t',exr
							print '\t',job_line
							print '\tFILE TIME', exr_currtime
							print '\tCOMMIT TIME', commit_time
							
							out_job.write( job_line + '\n' )
		

	#for file, date in render_cmd_dates.iteritems():
	#	# check the dates
	#	
	#	#mtime = os.stat(tfile).st_mtime
	# print lines

if __name__ == '__main__':
	main()