#!BPY
"""
Name: 'UV Pin Edges'
Blender: 243
Group: 'UV'
Tooltip: 'Put some useful info here'
"""

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

# This is a script that was spesificly written for alligning and pinning strips of faces on a tree trunk

from Blender import Scene, Mesh, Window, sys, Mathutils
import BPyMessages
import bpy
import BPyMesh
from Blender.Mathutils import Vector, AngleBetweenVecs, RotationMatrix

def my_mesh_util(me):
	# Examples
	S = Mesh.EdgeFlags.SEAM
	edges_seam = set([ed.key for ed in me.edges if ed.flag & S])
	
	# make an edges_seam
	ed_face_count = {}
	for f in me.faces:
		if not f.hide: # ignore seams next to hidden faces
			for edkey in f.edge_keys:
				try:		ed_face_count[edkey] += 1
				except:		ed_face_count[edkey] =  1
	
	# remove all single edge faces (or on the bounds of a hidden face) from edges_seam to make edges_seam_island - this means 
	edges_seam = edges_seam.difference( set( [edkey for edkey, eduser in ed_face_count.iteritems() if eduser == 1] ) )
	
	uv_key_vec_dict = {}
	uv_connect_dict = {}
	uv_seamconnect_dict = {}
	
	face_uv_islands = BPyMesh.facesUvIslands(me)
	print len(face_uv_islands), 'islands'

	for face_uv_island in face_uv_islands:
		face_uv_island[:] = [f for f in face_uv_island if f.sel]
	
	face_uv_islands = [face_uv_island for face_uv_island in face_uv_islands if face_uv_island]

	print "totislands =-= ", len(face_uv_islands)

	for face_uv_island in face_uv_islands:
		
		# For every island!
		for f in face_uv_island:
			
			vs = f.v
			uv = f.uv
			uv_keys = [tuple(v) for v in uv]
			fkeys = f.edge_keys
			
			if len(vs) == 3:
				f.uvSel = (0,0,0)
				pairs = (0,1), (1,2), (2,0)
			else:
				f.uvSel = (0,0,0,0)
				pairs = (0,1), (1,2), (2,3), (3,0)
			
			for i, i_other in pairs:
				
				# first add to global uvconnect dict.
				# Add all other UVs - for connectivity
				uvk1 = uv_keys[i]
				st = uv_connect_dict.setdefault(uvk1, set())
				st.update( [ uv_keys[j] for j in xrange(len(f)) if j != i] )
				
				# This dict maps uv keys to a list of face uvs
				ls = uv_key_vec_dict.setdefault(uvk1, [])
				ls.append(uv[i])
				
				if fkeys[i] in edges_seam: # This is a seam
					uvk2 = uv_keys[i_other]
					
					ls = uv_seamconnect_dict.setdefault(uvk1, [])
					if uvk2 not in ls: ls.append(uvk2)
					
					ls = uv_seamconnect_dict.setdefault(uvk2, [])
					if uvk1 not in ls: ls.append(uvk1)
		
		# Find UV strips!!!
		
		def next_uv(uv_ls, uv_prev):
			if len(uv_ls) == 2:
				if uv_ls[0] == uv_prev:
					return uv_ls[1]
				elif uv_ls[1] == uv_prev:
					return uv_ls[0]
				
		uv_strips = []
		
		for uv_key, uv_brothers in uv_seamconnect_dict.iteritems():
			#print len(uv_brothers), uv_brothers
			if len(uv_brothers) == 1:
				# print "ONE BRO"
				uvlist = [uv_key, uv_brothers[0]]
				uv_brothers[:] = [] # INVALIDATE
				uv_strips.append(uvlist)
				while True:
					uv_next_bro = uv_seamconnect_dict[ uvlist[-1] ]
					if len(uv_next_bro) != 2:
						uv_next_bro[:] = [] # INVALIDATE
						break
					
					uv_key = next_uv(uv_next_bro, uvlist[-2])
					
					#if uv_key==None:
					#	return
					
					uv_next_bro[:] = []
					
					uvlist.append(uv_key)
				print len(uvlist)
				
				
		
		# Build a mapping so we can know the UVs
		# we could really 
		
		face_uvs = [(uv, tuple(uv)) for f in face_uv_island for uv in f.uv]
		#face_uvs = [uv for f in face_uv_island for uv in f.uv]
		
		print len(uv_strips), 'strips for this island'
		
		vec1 = Vector( 0,0 )
		vec2 = Vector( 0,0 )
		"""
		vecs = []
		for uvlist in uv_strips:
			vec_average = Vector( 0,0 )
			for i in xrange(1,len(uvlist)):
				vec1[:] = uvlist[i-1]
				vec2[:] = uvlist[i]
				
				vec_average += vec1-vec2
			vecs.append( vec_average.normalize() )
		
		# add all the lines into an average for this island
		print len(uv_strips), 'uv_strips'
		
		if vecs:
			vec_average_island = vecs[0]
			if len(vecs)!=1:
				# Add the others 
				for  i in xrange(1, len(vecs)):
					vec_average = vecs[i]
					
					# Get a direction for this island
					if AngleBetweenVecs(vec_average_island, vec_average) > 180:
						vec_average = -vec_average
						vec_average_island += vec_average
			
			ang = AngleBetweenVecs(vec_average_island, Vector(0.0, 1.0))
			
			if Mathutils.CrossVecs(vec_average_island.copy().resize3D(), Vector(0.0, 1.0, 0)).z > 0:
				ang = -ang
			rotmat = RotationMatrix(ang, 2)
			
			
			for f in face_uv_island:
				for uv in f.uv:
					uv[:] = uv*rotmat
		"""
		if 1:
			
			# when more then 2 strips, use leftmost and rightmost.
			if len(uv_strips) > 2:
				striplocs = []
				for i, uvlist in enumerate(uv_strips):
					average_x = 0.0
					average_y = 0.0
					
					for uv_key in uvlist:
						average_x += uv_key[0]
						average_y += uv_key[1]
					
					striplocs.append( (average_x/len(uvlist), average_y/len(uvlist), i) )
				
				# we only really care about the x, since this is teh first value, min/max work ok
				uv_strips[:] = [uv_strips[min(striplocs)[2]], uv_strips[max(striplocs)[2]]]
				
			
			
			
			for uvlist in uv_strips:
				# Rotate Strips
				
				uvlist_uvvecs = [] # face 
				
				# Collect uvs for this strip.
				for uv_key in uvlist:
					uvlist_uvvecs.append(uv_key_vec_dict[uv_key])
				
				x = 0.0
				for uvls in uvlist_uvvecs:
					x += uvls[0].x # all uvs in this uvls are the same, dont apply them twice when averaging
				
				x = x/len(uvlist_uvvecs)
				for uvls in uvlist_uvvecs:
					for uv in uvls:
						uv.x = x
				
				# Set the pinning
				for f in face_uv_island:
					for i, uv in enumerate(f.uv):
						
						# BAD!!!
						for uvls in uvlist_uvvecs:
							if uv in uvls:
								# PIN? UVSel for now, this sucks too, just select them
								uvsel = list(f.uvSel)
								uvsel[i] = 1
								f.uvSel = tuple(uvsel)
								break
			
			#uv_strips_uvcog
	
	
def main():
	
	# Gets the current scene, there can be many scenes in 1 blend file.
	sce = bpy.data.scenes.active
	
	# Get the active object, there can only ever be 1
	# and the active object is always the editmode object.
	ob_act = sce.objects.active
	
	if not ob_act or ob_act.type != 'Mesh':
		BPyMessages.Error_NoMeshActive()
		return 
	
	
	# Saves the editmode state and go's out of 
	# editmode if its enabled, we cant make
	# changes to the mesh data while in editmode.
	is_editmode = Window.EditMode()
	if is_editmode: Window.EditMode(0)
	
	Window.WaitCursor(1)
	me = ob_act.getData(mesh=1) # old NMesh api is default
	t = sys.time()
	
	# Run the mesh editing function
	my_mesh_util(me)
	
	# Restore editmode if it was enabled
	if is_editmode: Window.EditMode(1)
	
	# Timing the script is a good way to be aware on any speed hits when scripting
	print 'My Script finished in %.2f seconds' % (sys.time()-t)
	Window.WaitCursor(0)
	
	
# This lets you can import the script without running it
if __name__ == '__main__':
	main()