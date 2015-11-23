import os, time

search = '/shared/render/'

def get_file_number(f):
	'''
	Tricky func to get the frame number	from say
		someName3232342.exr
	'''
	f_tmp = f.split('.')[0]
	
	# work out how many numbers are at the end if any
	j = 1
	while j <= len(f_tmp) and f_tmp[-j].isdigit(): j+=1
	
	if j>1:
		# We have a number!
		return int(f_tmp[-(j-1):])
	else:
		return None

def main():
	
	first_frame = 1
	
	dirs = {}
	
	errors = {}
	
	if 0:
		"""
		file_exrFolders = os.popen('find %s' % search).readlines()
		file_exrFolders.sort()
		tot = len(file_exrFolders)
		
		# Get all folders containing jpegs
		for i, line in enumerate(file_exrFolders):
			line = line.strip()
			if line.lower().endswith('.exr') and '/exr/' in line and '/old/' not in line:
				
				moviedir, filename = line.split('/exr/')
				moviedir += '/exr/'
				
				# Ok we have a path containing jpegs 
				# /shared/render/05_throwing/10/jpg/foo.jpg
				
				# Add a list for this folder if its not there.
				#if '09_' in moviedir and '_02' in moviedir:
				#	dirs.setdefault(moviedir, []).append(filename)
				
				dirs.setdefault(moviedir, []).append(filename)
		"""
	
	else:
		# Alternate method of getting all exr frames together
		# Use the job files, this means the exrs dont need to be rendered! ;)
		
		# ----------------------
		# From sortRenders.py
		# from sortRenders import filename_2_path
		RENDER='/shared/render/'
		def file_split(f):
			# 10_chinchilla-03_0001.exr -> 10_chinchilla, 03
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
		# ----------------------
		
		
		jobdir = '/home/wavemage/production/jobs/' # must have trailing slash!
		for job in os.listdir(jobdir):
			# Get the path for this job!
			for line in open(os.path.join(jobdir, job), 'r'):
				
				# Get the filename from the job name
				filename = line.split()[2][1:] + '.exr'
				moviedir = filename_2_path(filename)
				dirs.setdefault(os.path.join(moviedir, 'exr/'), []).append(filename)
	
	
	# Now render the frames
	import Blender
	
	sce = Blender.Scene.GetCurrent()
	seq = sce.sequence
	
	for moviedir, files_all in sorted(dirs.items()):
		if len(files_all) > 1:
			fname =   moviedir.split('/')[-4].split('_')[0] + '_' + moviedir.split('/')[-3]
			
			# --------------
			files_all.sort()
			
			files_split = [ [] ] # split the files which have discontinues numbering (so we get the cuts that were rendered into 1 image dir)
			
			last_index = '' # nothing will == this!
			
			for f in files_all:
				# Assume the file was rendered in blender and it has a number at the end. eg -> foo000001.exr
				frame_index = get_file_number(f)
				
				if (type(frame_index)==int and type(last_index)==int) and (last_index+1 == frame_index): # we are numbered frames, check they are consistant
					files_split[-1].append( f )
				elif frame_index == last_index: # ok we are not numbered frames, just append if they are both not numbered/
					files_split[-1].append( f )
				else:
					files_split.append( [] )
					files_split[-1].append( f )
				
				last_index = frame_index
			
			files_split = [files for files in files_split if files] # remove empty lists
			
			if len(files_split) > 1:
				print files_split
			
			
			for i, files in enumerate(files_split):
				print files
				strip = seq.new( (moviedir, files), first_frame, i+1 )
				strip.name = '%s-%d' % ( fname, i)
				
				first_frame += len(files)

if __name__ == '__main__':
	main()