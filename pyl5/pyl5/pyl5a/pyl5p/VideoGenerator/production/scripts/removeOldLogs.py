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
This script removes duplicate log files from the sun grid
'''

import os
LOGDIR = '/shared/render/logs'

def main():
	
	logs_names = os.listdir(LOGDIR)
	
	lognames = {}
	remove_names = []
	keep_names = []
	
	# Group by 
	for l in logs_names:
		exr = l.split('.')[0] # name sans .exr
		lognames.setdefault( exr, [] ).append( l )


	for key, files in lognames.iteritems():
		maxnum = -1
		for l in files:
			try:
				# _13_end-02_0064.e313287   ->   313287
				num = int( l.split('.')[-1][1:] )
			except:
				num = -1
			
			if num > maxnum:
				maxnum = num
		
		if maxnum == -1:
			print 'error, cant get numbers for files...', files
		else:
			str_maxnum = str(maxnum)
			for l in files:
				if str_maxnum not in l:
					remove_names.append(l)
				else:
					keep_names.append(l)
	
	print 'Remove names', len(remove_names)
	print 'Keep names', len(keep_names)
	
	for f in remove_names:
		os.remove( os.path.join( LOGDIR,  f) )

if __name__ == '__main__':
	main()
