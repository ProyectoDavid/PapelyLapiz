
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

#!/usr/bin/python

print('################################################################################')
print('#')
print('# VIDEO GENERATOR')
print('#')
print('################################################################################')

# Import
import xml.dom.minidom
import pprint
import os
from time import gmtime,strftime
import bpy
import mathutils

# Constantes
POSITION_SCALE_W = 16
POSITION_SCALE_H = 8
DEFAULT_CAMERA_ALTITUDE = 12 
FRAME_STEP = 2
NUM_POINTS_CURVE = 5
NUM_FRAMES_ANIMATION = 72
MODELS_PATH = '/var/www/pyl3/VideoGenerator'
#RENDER_LOW_QUALITY = os.getenv('RENDER_LOW_QUALITY') == "True"
RENDER_LOW_QUALITY = "True"
RENDER_VIDEO = os.getenv('RENDER_VIDEO') == "True"
SCRIPT_XML_FILENAME = os.getenv('SCRIPT_XML_FILENAME')
SCORE_XML_FILENAME = os.getenv('SCORE_XML_FILENAME')

print ('Beginnin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

# Cargar el archivo XML a memoria, en una estructura mas facilmente entendible
print ('Parsing: ' + SCRIPT_XML_FILENAME)

doc = xml.dom.minidom.parse(SCRIPT_XML_FILENAME)

actors = {}

for xmlActor in doc.getElementsByTagName('actor'):
    a = {}

    # Asigno los valores de los atributos de este elemento
    for attr_key in xmlActor.attributes.keys():
        a[attr_key] = xmlActor.getAttribute(attr_key)

    #Asigno el valor de la posicion del elemento
    for xmlPosition in xmlActor.getElementsByTagName('position'):
        a['position'] = ( float(xmlPosition.getAttribute('x')) * POSITION_SCALE_W , -float(xmlPosition.getAttribute('z')) * POSITION_SCALE_H, 0 )

    # Asigno la trayectoria que tiene este elemento
    a['trajectory'] = []
    for xmlPoint in xmlActor.getElementsByTagName('point'):
        a['trajectory'].append( ( float(xmlPoint.getAttribute('x')) * POSITION_SCALE_W , -float(xmlPoint.getAttribute('z')) * POSITION_SCALE_H , 0 ) )

    # Por ultimo agrego este elemento a la lista de actores de la composicion, pero me cuido de no sobreescribir otro actor que tenga el mismo nombre
    currIndex = 0
    assetName = a['asset']
    while assetName in actors: # Seria mas bonito con un do..while , pero Python no lo tiene
        assetName = "%s_%d" % ( a['asset'] , currIndex )
        currIndex += 1
    a['asset'] = assetName
    actors[assetName] = a

    # NUEVO
    a["unlink"] = True 
    a["model"] = None

# Invocar al API de Blender para crear los actores y acomodar todos los elementos en la escena
print ('Deletin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

# Borrar todo lo que haya en la escena:
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

for tmp_curve in bpy.data.curves:
    bpy.data.curves.remove(tmp_curve)

for tmp_mesh in bpy.data.meshes:
    bpy.data.meshes.remove(tmp_mesh)

# Remuevo audio
for speaker in bpy.data.speakers:
	bpy.data.speakers.remove(speaker)

# Para el calculo del BoundingBox de la escena mas abajo
bb_min = None
bb_max = None

################################################################################
#
# IMPORTAR Y MANIPULAR UNA ESCENA
#
################################################################################
print ('Importin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

bpy.ops.wm.open_mainfile(filepath='/home/jm.moreno743/production/scenes/pyl/pyl.blend') # Si hago esta operacion pierdo el contexto

print('#')
print('# INVENTARIO DE OBJETOS')
print('#')
#otro = bpy.data.objects["Bird"].copy()
#for obj in bpy.data.objects:
#        print('Un objeto es ' + obj.name)

# unlink the object from the scene
#bpy.context.scene.objects.unlink(bpy.data.objects["Bird"])
#for obj in bpy.data.objects:
#    print('Un objeto ahora es ' + obj.name)

print ('Drawin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

# bpy.ops.sequencer.sound_strip_add(filepath='/Users/barcodepandora/Sites/VideoGenerator/sound/jazz.mp3', frame_start=1, channel=1)
# Crear los objetos en las posiciones que nos hayan dicho en el XML

for actor in actors.keys():
    if actors[actor]['asset'] == 'SBCamera':
        continue
    if actor.startswith("Pajaro"):
        actors[actor]["unlink"] = False
        bpy.data.objects["Bird"].location = actors[actor]['position']
    elif actor.startswith("Ardilla"):
        actors[actor]["unlink"] = False
        bpy.data.objects["Ardilla"].location = actors[actor]['position']

never = False
for obj in bpy.data.objects:
    never = False
    if obj.name == 'Bird':
        for actor in actors.keys():
            if actor.startswith("Pajaro") and actors[actor]['unlink'] == False:
                never = True
        if never == False:
            bpy.context.scene.objects.unlink(bpy.data.objects["Bird"])
    elif obj.name == 'squirrel':
        for actor in actors.keys():
            if actor.startswith("Ardilla") and actors[actor]['unlink'] == False:
                never = True
        if never == False:
            bpy.context.scene.objects.unlink(bpy.data.objects["squirrel"])

# Agregar la camara
print ('Camerin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

'''
bpy.ops.object.camera_add()
camera = bpy.context.object
bpy.ops.object.lamp_add()
lamp = bpy.context.object
camera.location[0] = ( bb_max[0] + bb_min[0] ) / 2
camera.location[1] = ( (bb_max[1] + bb_min[1]) - 25 ) / 2
camera.location[2] = DEFAULT_CAMERA_ALTITUDE / 3
bpy.context.scene.camera = camera
#print('La camara esta ubicada en ' + camera.location)

# Agregar lampara a la escena
print ('Lightin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

lamp.location = mathutils.Vector(ground_plane.location)
lamp.location[0] = lamp.location[0]
lamp.location[1] = bb_min[1]-1
lamp.location[2] = lamp.location[2]+5
#print('La luz esta ubicada en ' + lamp.location)
'''
bpy.ops.object.camera_add()	
camera = bpy.data.objects["Camera"]
if 'SBCamera' in actors:
    camera.location = actors['SBCamera']['position']
else:
    camera.location[0] = 7
    camera.location[1] = -6
camera.location[2] = 5
print('la camara quedo en ' + str(camera.location[0]) + ', ' + str(camera.location[1]) + ', ' + str(camera.location[2]))

bpy.context.scene.camera = camera

# Agregar Rotaciones de Camara
print ('Rotatin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

rx = 55.0
ry = 0.0
rz = 0.0
pi = 3.14159265

camera.rotation_mode = 'XYZ'
camera.rotation_euler[0] = rx*(pi/180.0)
camera.rotation_euler[1] = ry*(pi/180.0)
camera.rotation_euler[2] = rz*(pi/180.0)

# Realizar animaciones
# {
print ('Animatin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

# }

################################################################################
#
# IMPLEMENTACION SONIDO
#
################################################################################

# Defino esquema de propagacion
bpy.context.scene.audio_distance_model = 'EXPONENT_CLAMPED'

# FOLEY

i = 0;
print ('Foleyin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

score = xml.dom.minidom.parse(SCORE_XML_FILENAME) # Creamos arbol XML score
for actor in actors.keys():
    for tagScore in score.getElementsByTagName('score'): # score
        for tagActor in tagScore.getElementsByTagName('actor'): # actor
            if actors[actor]['asset'] == tagActor.getAttribute('asset') and actors[actor]['unlink'] == False: # hay un actor que en el score se llama igual

                # creo speaker con su sonido
                bpy.context.scene.frame_current = 1 # posicion en timeline donde quiero que se escuche el speaker
                print ('Agregando el sonido ' + tagActor.getElementsByTagName('sound')[0].getAttribute('value'))
                bpy.ops.object.speaker_add(location=actors[actor]['position']) # agregamos speaker en posicion en escena
                bpy.ops.sound.open_mono(filepath=tagActor.getElementsByTagName('sound')[0].getAttribute('value')) # agregamos sonido
                bpy.data.speakers[i].sound = bpy.data.sounds[i] # extraemos de los sonidos de escena

                # uso propiedades para sonorizacion 3D
                bpy.data.speakers[i].volume_min = 0 # valor mínimo de volumen no importa qué tan lejos esté el speaker
                bpy.data.speakers[i].volume_max = 1
                bpy.data.speakers[i].attenuation = 3
                bpy.data.speakers[i].distance_reference = 5

                # agrego un parent para que cuando el parent cambie de posicion el speaker se escuche en esa posicion
                #bpy.data.speakers[i].parent = actors[actor]['model'] # El parent funciona

                # deselecciono todo en el editor nla
                # esto es porque necesito en los demas speakers hacer copias de uns trip de sonido en el mismo track
                #for soundTrack in bpy.context.active_object.animation_data.nla_tracks:
                    #soundTrack.select = False
                    #for stripOfTrack in soundTrack.strips:
                        #stripOfTrack.select = False
                i = i + 1

# Fondo

print ('Ambientin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

x = 0 #TODO: ¿Que pasa si inicializo en una sola linea?
y = 0
z = 0
#i = len(bpy.data.speakers)
for tagScore in score.getElementsByTagName('score'): # score
	for tagScene in tagScore.getElementsByTagName('scene'): # scene
		for tagPoint in tagScene.getElementsByTagName('point'): # point
			
			# obtengo puntos
			x = tagPoint.getAttribute('x') 
			y = tagPoint.getAttribute('y')
			z = tagPoint.getAttribute('z')
			
			# creo speaker con su sonido
			bpy.context.scene.frame_current = 1 																# posicion en timeline donde quiero que se escuche el speaker
			print ('Agregando el sonido ' + tagScene.getElementsByTagName('sound')[0].getAttribute('value'))
			bpy.ops.object.speaker_add(location=(int(x), int(y), int(z))) 										# agregamos speaker en posicion en escena
			bpy.ops.sound.open_mono(filepath=tagScene.getElementsByTagName('sound')[0].getAttribute('value')) 	# agregamos sonido
			bpy.data.speakers[i].sound = bpy.data.sounds[i] 													# extraemos de los sonidos de escena
			
			# uso propiedades para sonorizacion 3D
			bpy.data.speakers[i].volume_min = 0 																# valor mínimo de volumen no importa qué tan lejos esté el speaker
			bpy.data.speakers[i].volume_max = 1
			bpy.data.speakers[i].attenuation = 3
			bpy.data.speakers[i].distance_reference = 5
			
			# deselecciono todo en el editor nla
			# esto es porque necesito en los demas speakers hacer copias de uns trip de sonido en el mismo track
			#for soundTrack in bpy.context.active_object.animation_data.nla_tracks:
                            #soundTrack.select = False
                            #for stripOfTrack in soundTrack.strips:
                                #stripOfTrack.select = False
    				
			i = i + 1 # incremento i

# Renderizar la imagen o el video
print ('Filmin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

# {
bpy.ops.sound.bake_animation() # Limpia la cache del sonido
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = NUM_FRAMES_ANIMATION
bpy.context.scene.frame_current = 1

bpy.context.scene.camera = camera
bpy.context.scene.render.parts_x = 1
bpy.context.scene.render.parts_y = 1
bpy.context.scene.render.use_sss = False

################################################################################
#
# RENDERIZADO A VIDEO
#
################################################################################

print ('TEST RENDERIN PROPERTIES:')
print ('bpy.context.scene.render.use_raytrace = False')
print ('bpy.context.scene.render.use_envmaps = False')
print ('bpy.context.scene.render.use_textures = False')
print ('bpy.context.scene.render.use_shadows = False')
print ('bpy.context.scene.render.use_antialiasing = False\n')
print ('Renderin at: ')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

if RENDER_LOW_QUALITY:
    bpy.context.scene.render.use_raytrace = False
    bpy.context.scene.render.use_envmaps = False
    bpy.context.scene.render.use_textures = False
    bpy.context.scene.render.use_shadows = False
    bpy.context.scene.render.use_antialiasing = False
else:
    bpy.context.scene.render.use_raytrace = True
    bpy.context.scene.render.use_envmaps = True
    bpy.context.scene.render.use_textures = True
    bpy.context.scene.render.use_shadows = True
    bpy.context.scene.render.use_antialiasing = True
    print('oiga bpy.context.scene.render.use_raytrace = ' + str(bpy.context.scene.render.use_raytrace));

if RENDER_VIDEO:
    #Archivo muy grande: bpy.context.scene.render.image_settings.file_format='AVI_JPEG'
    #Archivo 1.3M .dvd: 
    bpy.context.scene.render.image_settings.file_format='FFMPEG'
    #NO funciona: bpy.context.scene.render.image_settings.file_format='AVICODEC'
    #no lo probe: bpy.context.scene.render.image_settings.file_format='XVID'
    #bpy.context.scene.render.image_settings.file_format='THEORA'
    #1.1M avi : bpy.context.scene.render.image_settings.file_format='H264'
    bpy.context.scene.render.filepath = "output.mpg"
    bpy.context.scene.render.ffmpeg.audio_codec = 'MP3'
    bpy.ops.render.render(animation=True)
    #os.rename("output-0001-0300.ogg", "output.ogg")    
else:
    bpy.context.scene.render.image_settings.file_format='PNG'
    bpy.context.scene.render.filepath = "output.png"
    bpy.ops.render.render(write_still=True)

# }
print ('THE END AT: ')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

'''
HOW 2 TEST:
	/usr/bin/Downloads/blender -P /home/david/Pyl/SoundFilmGenerator.py -b /home/david/Pyl//empty_scene.blend > //home/david/Pyl/SoundFilm.log
TODO:
	+ objetos
	objetos + extensos
	animaciones + extensas
'''

