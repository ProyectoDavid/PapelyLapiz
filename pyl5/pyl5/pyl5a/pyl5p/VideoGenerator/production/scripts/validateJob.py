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
this script checks for jobs that have been rendered, as well as frames that were missed when rendering
'''

import sys, os
argv = sys.argv
if len(argv) < 3:
	print "To use this script give the following arguments"
	print "python validateJobs.py ./jobfile.job ./renderpath"


def main():
	job = argv[-2]
	imgdir = argv[-1]
	
	print 'JOB:', job, 'IMAGESEARCH PATH:', imgdir, 
	
	try:
		jobfile = open(job)
	except:
		print "cant read job error!"
		return
	
	image_final_images = [ll for l in jobfile.readlines() for ll in (l.split()[-1].lower(),)]
	
	# These 2 lists are in sync
	image_names = []
	image_paths = []
	
	for (path, dames, fnames) in os.walk(imgdir):
		for fn in fnames:
			if fn.endswith('.exr'):
				image_names.append(fn.lower()) # used for comparing files, so lower
				image_paths.append( os.path.join(path, fn) )
	
	missing = len(image_final_images)
	
	for exr in image_final_images:
		if exr.lower() in image_names:
			missing -= 1
	
	
	if missing == len(image_final_images):
		print " -- NONE!"
	elif missing == 0:
		print " -- ALL"
	else:
		print " -- SOME", len(image_final_images)-missing, 'of', len(image_final_images)
	

main()
