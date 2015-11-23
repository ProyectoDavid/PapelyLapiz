
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
# IMPLEMENTACION INICIO
#
################################################################################

POSITION_SCALE_W = 16
POSITION_SCALE_H = 8
DEFAULT_CAMERA_ALTITUDE = 15
FRAME_STEP = 30
NUM_POINTS_CURVE = 5
NUM_FRAMES_ANIMATION = 72

print ('Launchin: ')

# Invocar al API de Blender para crear los actores y acomodar todos los elementos en la escena
# {

import bpy

# Borrar todo lo que haya en la escena:
#bpy.ops.object.mode_set(mode = 'OBJECT') 
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

#bpy.ops.wm.link_append(directory="/Users/jvan/Desktop/production/scenes/06_killing/13_practice.blend/Object/", filename="Squirrel_proxy", link=False)
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 38

################################################################################
#
# IMPLEMENTACION DE DANIEL
#
################################################################################

# Cargar el archivo XML a memoria, en una estructura mas facilmente entendible
# {

print ('Parsing: script.xml')

import xml.dom.minidom

doc = xml.dom.minidom.parse('/home/jm.moreno743/SoundFilm/script.xml')

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

# }

# Crear los objetos en las posiciones que nos hayan dicho en el XML

import mathutils
import pprint

bb_max = None
bb_min = None

for actor in actors.keys():
    if actors[actor]['asset'] == 'SBCamera':
        continue
    
    if actors[actor]['asset'] == 'Ardilla':
        print('encontre una ardilla')
        bpy.ops.wm.link_append(directory="/home/jm.moreno743/SoundFilm/sackboy.blend/Object/", filename="SackboyMO", link=False)
        bpy.context.scene.objects.active = bpy.data.objects['Sackboy']
        bpy.context.object.scale = (0.3, 0.3, 0.3)
        
    ob = bpy.context.object
    ob.name = actors[actor]['asset']
    #ob.location = actors[actor]['position']
    
    # Voy calculando donde debe quedar la camara (en caso de que no me digan donde de manera explicita) 
    # con base en la posicion de cada elemento de la escena:
    # La camara debe estar por sobre el centro del BoundingBox que contiene a todos los elementos, y mirando
    # hacia abajo
    if bb_min is None:
        bb_min = mathutils.Vector(ob.location)
    else:
        bb_min[0] = min( bb_min[0] , ob.location[0] )
        bb_min[1] = min( bb_min[1] , ob.location[1] )
        bb_min[2] = min( bb_min[2] , ob.location[2] )
        
    if bb_max is None:
        bb_max = mathutils.Vector(ob.location)
    else: 
        bb_max[0] = max( bb_max[0] , ob.location[0] )
        bb_max[1] = max( bb_max[1] , ob.location[1] )
        bb_max[2] = max( bb_max[2] , ob.location[2] )


################################################################################
#
# IMPLEMENTACION SONIDO
#
################################################################################

import xml.dom.minidom

score = xml.dom.minidom.parse('/home/jm.moreno743/SoundFilm/score.xml') # Creamos arbol XML score

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
			y = tagPoint.getAttribute('y')
			z = tagPoint.getAttribute('z')
			bpy.context.scene.frame_current = 1 															# posicion en timeline donde quiero que se escuche el speaker
			bpy.ops.object.speaker_add(location=(int(x), int(y), int(z))) 									# agregamos speaker en posicion en escena
			speakers.append(bpy.context.object.data) 														# agregamos speaker a contenedor de speakers
			bpy.ops.sound.open(filepath=tagScene.getElementsByTagName('sound')[0].getAttribute('value')) 	# agregamos sonido
			speakers[0].sound = bpy.data.sounds[0] 															# extraemos de los sonidos de escena
			speakers[0].volume_min = 0 																		# valor mínimo de volumen no importa qué tan lejos esté el speaker
			speakers[0].volume_max = 1
			speakers[0].attenuation = 3
			speakers[0].distance_reference = 10

################################################################################
#
# IMPLEMENTACION CAMARA
#
################################################################################

bpy.ops.object.camera_add()
camera = bpy.context.object
if 'SBCamera' in actors:
    print('hay una camara')
    camera.location = actors['SBCamera']['position']
else:
    camera.location =  ( bb_max + bb_min ) / 2
    camera.location[2] = 15
camera.location.x = 0
camera.location.y = 0
camera.location.z = 5

bpy.context.scene.camera = camera

bpy.ops.sound.bake_animation() # Limpia la cache del sonido

bpy.context.scene.frame_current = 1

################################################################################
#
# RENDERIZADO A VIDEO
#
################################################################################

bpy.context.scene.render.image_settings.file_format='FFMPEG'
bpy.context.scene.render.filepath = "/home/jm.moreno743/SoundFilm/output.mpg"
bpy.context.scene.render.ffmpeg.audio_codec = 'MP3'
bpy.ops.render.render(animation=True)


'''
OK agregué una cámara, se necesita para que pueda crear el video
'''
