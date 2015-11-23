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
This script was used on all peach scenes before rendering, to set the render format and settings
'''


# run with...
# blender -b myblendfile.blend -P render_settings.py -a
from Blender import Scene, Object
import sys

def main():
	
	# Was a camera name given as a python arg???
	# eg...
	# -- SomeCameraName
	camera = None
	argv = sys.argv
	if argv:
		try:
			camera = Object.Get(argv[argv.index('--')+1])
		except:
			print "ERROR, Camera as argument could not be set '%s'" % argv[0]
	
	
	# Settings for all scenes
	for sce in Scene.Get():
		rend = sce.render
		rend.freeImages = True
		rend.saveBuffers = True
		rend.compositeFree = True
		
		rend.oversampling = True
		
		# rend.OSALevel = 8 # We dont want to set this now.
		rend.threads = 1
		
		rend.motionBlur = False
		rend.fieldRendering = False
		
		if camera:
			sce.objects.camera = camera
	
	# Settings for render scene
	sce = Scene.GetCurrent()
	rend = sce.render
	
	rend.extensions = 1
	rend.renderwinSize = 100
	
	#rend.enableSky()
	#rend.enablePremultiply()
	#rend.enableKey()
	
	#rend.enableBWColor()
	rend.enableRGBColor()
	#rend.enableRGBAColor()
	
	rend.compositor = True
	rend.sequencer = False
	rend.sizeX = 1920
	rend.sizeY = 1080
	
	rend.xParts = 6
	rend.yParts = 6
	
	rend.fps = 24
	
	rend.zbuf = False
	rend.halfFloat = True
	rend.preview = False
	
	rend.touch = False
	rend.noOverwrite =False
	
	rend.imageType = Scene.Render.OPENEXR

if __name__ == '__main__':
	main()
