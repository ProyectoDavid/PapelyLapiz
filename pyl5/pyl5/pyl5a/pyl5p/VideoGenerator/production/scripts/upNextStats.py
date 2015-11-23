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
Report whats up next on the renderfarm.
This script compares 2 render jobs, one thats currently running
on the renderfarm, and another that is generated recently.
'''

UPNEXT = '/shared/render/upnext.job'
CURRENT = '/home/wavemage/production/jobs/queue.job'
UPNEXT_STAT = '/shared/render/upnext.log'

def main():
	next_lines = [l.strip() for l in open(UPNEXT, 'r').readlines()]
	current_lines = [l.strip() for l in open(CURRENT, 'r').readlines()]

	for l in current_lines:
		try:
			next_lines.remove( l )
		except:
			pass
	
	file = open(UPNEXT, 'w')
	for l in next_lines:
		file.write('%s\n' % l)
	file.close()
	del file
	
	file_frames = {}
	for l in next_lines:
		l_split = l.split() 
		
		file = l_split[-3]
		# frame = l_split[-1]
		
		try:
			file_frames[file] += 1
		except:
			file_frames[file] = 1
	
	file = open(UPNEXT_STAT, 'w')
	tot = 0
	for f, num in file_frames.iteritems():
		if f.endswith('_'):
			f = f[:-1]
		file.write('%s\t%d\n' % (f, num))
		tot += num
		
	file.write('\n*** total ***\n')
	file.write('%d\n' % tot)

if __name__ == '__name__':
	main()