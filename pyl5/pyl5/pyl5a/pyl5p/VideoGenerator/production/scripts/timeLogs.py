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
Simple script that extracts the rendertime of every file in the log and prints the total time,
the average rendertime for a frame was 50min on a single processor 64bit amd system with 4gig of ram.
'''

import os
LOGDIR = '/shared/render/logs'

def main():
	
	
	tot_sec = 0.0
	tot_done_files = 0
	logs_names = [l for l in os.listdir(LOGDIR) if '.o'  in l]
	tot_files = float( len(logs_names) )

	for i, log in enumerate(logs_names):
		
		# Saved: 01_intro-01_0001.exr Time: 07:13.77
		#  02:10:21.59
		
		for l in open(os.path.join( LOGDIR, log ), 'r'):
			if l.startswith('Saved: '):
				timels = l.split('Time:')[-1].strip().split(':')
				
				sec = 0.0
				if len(timels) >= 1:
					sec += float(timels[-1]) # sec
				if len(timels) >= 2:
					sec += 60*float(timels[-2])  # min
				if len(timels) >= 3:
					sec += 60*60*float(timels[-3])  # hrs
				if len(timels) >= 4:
					raise "foo"
				#print sec
				tot_sec+=sec
				tot_done_files +=1
				# break
		print (i/tot_files) * 100
		
	print tot_sec
	print tot_done_files
	
if __name__ == '__main__':
	main()
