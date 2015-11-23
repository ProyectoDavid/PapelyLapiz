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
This script is quite spesific to the peach pipeline.

It reports files from the renderfarm that need to be reviewed.
'''


import os
import time

def file_date(path):
	#currtime = (year, month, day, hour, min, sec)
	# year, month, day, hour, minute, second, weekday, yearday, daylight = now
	return time.localtime(os.stat(path)[8])[0:6]

def file_date_simple(path):
	return os.stat(path)[8]

def is_dir1_newer(dir1, dir2):
	'''
	does dir1 contain any files newer then dir2
	
	in peach terms, dir1 is current and dir2 is final
	'''
	files1 = [f1 for f1 in os.listdir(dir1) if f1.endswith('.exr')]
	# files2 = os.filelist(dir2) we dont care about dir2 files
	
	maxdate = None
	
	for f1 in files1:
		#print f1
		f1full = os.path.join(dir1, f1)
		f2full = os.path.join(dir2, f1)
		if os.path.exists(f2full):
			if file_date_simple(f1full) > file_date_simple(f2full):
				mydate = file_date(f1full)
				
				if maxdate==None or mydate > maxdate:
					maxdate = mydate
		else:
			pass
	
	if maxdate:
		return maxdate
	return False


def main():
	final_dirs = [ l.strip() for l in os.popen('find /shared/render -name "final"').readlines() if l.strip() ]
	to_check = []
	for final_dir in final_dirs:
		current_dir = '/'.join(final_dir.split('/')[0:-1])
		#print current_dir, final_dir
		maxdate = is_dir1_newer(current_dir, final_dir)
		if maxdate:
			to_check.append((maxdate, final_dir))
			# pass
	to_check.sort()
	to_check.reverse()
	
	for maxdate, final_dir in to_check:
		print maxdate, final_dir
	
	# Now print final dirs that have no final
	final_dirs = [ l.strip() for l in os.popen('find /shared/render -name "final*"').readlines() if l.strip() ]
	odd_paths = set()
	missing_paths = set()
	
	for l in final_dirs:
		if l.endswith('final'):
			continue
		
		l_split = l.split('final')
		
		if len(l_split) >2:
			odd_paths.add( l )
		
		# print l_split[0] + 'final' + '!Test'
		l_test = l_split[0] + 'final'
		# print l_test, os.path.exists( l_test )
		if not os.path.exists( l_test ): # work out the original dir
			missing_paths.add( l_test )
	
	if odd_paths:
		print "*** Odd Paths ***"
		for l in sorted(list(odd_paths)):
			print l
	
	if missing_paths:
		print "*** Missing Final Paths ***"
		for l in sorted(list(missing_paths)):
			print l
	
main()
	
	
	
	

