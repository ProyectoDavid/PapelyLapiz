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

# This script prints the last rendered EXR images

LOGFILE = '/shared/render/log.txt'
shot_dict = {}

def shotAndFrame(filename):
	filename = filename[:-4] # remove .exr
	
	filename_split = filename.split('_')
	
	frame = int(filename_split.pop())
	
	return '_'.join( filename_split ), frame

def dateToTuple(date):
	'''
	yr:2008, month:3, day:2, hr:23, min:38, sec:22
		to
	(2008, 3, 2, 23, 38, 22)
	'''
	return tuple([int(d.split(':')[-1]) for d in date.replace(',', '').split() ])
	

def main():

	for l in open(LOGFILE, 'r'):
		filename, date = l.strip().split(' --- ')
		shot, frame = shotAndFrame(filename)
		shot_dict.setdefault( shot, {} )[frame] = dateToTuple(date)
	
	# Now we need to find the newest frames for each shot
	shot_dict_keys = shot_dict.keys()
	shot_dict_keys.sort()
	
	shot_times = []
	
	for shot_key in shot_dict_keys:
		max_date = max( shot_dict[shot_key].values() )
		shot_times.append( (max_date, shot_key) )
	
	shot_times.sort()
	
	for max_date, shot_key in shot_times:
		print max_date, shot_key

main()


