
#
#Papel y Lapiz - Software para la creacion de pequeños cortos.
#Copyright (C) 2015  Universidad de Los Andes - Proyecto DAVID.   
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along
#with this program; if not, write to the Free Software Foundation,
#Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#

################################################################################
#
# IMPLEMENTACION
#
################################################################################

print ('Parsing: ')

# Invocar al API de Blender para crear los actores y acomodar todos los elementos en la escena
# {

import bpy

# Borrar todo lo que haya en la escena:
bpy.ops.object.mode_set(mode = 'OBJECT') 
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

#bpy.ops.wm.link_append(directory="/Users/jvan/Desktop/production/scenes/06_killing/13_practice.blend/Object/", filename="Squirrel_proxy", link=False)
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 120

# IMPLEMENTACION SONIDO

import xml.dom.minidom

score = xml.dom.minidom.parse('score.xml') # Creamos arbol XML score

# Crea el sonido dada una etiqueta scene
x = 0 #TODO: ¿Que pasa si inicializo en una sola linea?
y = 0
z = 0
speakers = []
asound = ''
for tagScore in score.getElementsByTagName('score'): # score
	for tagScene in tagScore.getElementsByTagName('scene'): # scene
		for tagPoint in tagScene.getElementsByTagName('point'): # point
			x = tagPoint.getAttribute('x') # point
			#y = tagPoint.getAttribute('y')
			z = tagPoint.getAttribute('z')
			bpy.context.scene.frame_current = 1 															# posicion en timeline donde quiero que se escuche el speaker
			bpy.ops.object.speaker_add(location=(int(x), int(y), int(z))) 									# agregamos speaker en posicion en escena
			speakers.append(bpy.context.object.data) 														# agregamos speaker a contenedor de speakers
			bpy.ops.sound.open(filepath=tagScene.getElementsByTagName('sound')[0].getAttribute('value')) 	# agregamos sonido
			speakers[0].sound = bpy.data.sounds[0] 															# extraemos de los sonidos de escena


bpy.context.scene.frame_current = 1

# Crear la camara

import mathutils

# Para el calculo del BoundingBox de la escena mas abajo
bb_min = None
bb_max = None

ob = bpy.context.object
bb_min = mathutils.Vector(ob.location)
bb_max = mathutils.Vector(ob.location)

bpy.ops.object.camera_add()
camera = bpy.context.object
camera.location =  ( bb_max + bb_min ) / 2
camera.location[2] = 15

bpy.context.scene.camera = camera

bpy.context.scene.render.image_settings.file_format='FFMPEG'
bpy.context.scene.render.filepath = "output.mpg"
bpy.context.scene.render.ffmpeg.audio_codec = 'MP3'
bpy.ops.render.render(animation=True)


'''
ERROR: Cannot render, no camera
Fra:0 Mem:7.38M (0.10M, peak 7.48M) Sce:  Ve:0 Fa:0 La:0
Closing ffmpeg...
Flushing delayed frames...
zero video stream 0x7ff5765a2a00
read blend: /var/www/pyl2/VideoGenerator/empty_scene.blend
'''
