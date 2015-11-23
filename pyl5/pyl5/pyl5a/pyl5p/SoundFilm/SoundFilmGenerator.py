
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
NUM_FRAMES_ANIMATION = 24
ARTIFACTS_PATH = '/home/jm.moreno743/SoundFilm/'

from time import gmtime, strftime

print ('################################################################################')
print ('Launchin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

# Invocar al API de Blender para crear los actores y acomodar todos los elementos en la escena
# {

import bpy

# Borro todo lo que haya en la escena:
bpy.ops.object.mode_set(mode = 'OBJECT') 
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Remuevo todo lo qe sea audio
for speaker in bpy.data.speakers:
	bpy.data.speakers.remove(speaker)

#bpy.ops.wm.link_append(directory="/Users/jvan/Desktop/production/scenes/06_killing/13_practice.blend/Object/", filename="Squirrel_proxy", link=False)
#bpy.context.area.type = 'NLA_EDITOR'

################################################################################
#
# IMPORTAR Y MANIPULAR UNA ESCENA
#
################################################################################

bpy.ops.wm.open_mainfile(filepath='/home/jm.moreno743/production/scenes/pyl/pyl.blend')

print('#')
print('# INVENTARIO DE OBJETOS')
print('#')
for obj in bpy.data.objects:
	print('Un objeto es ' + obj.name)
'''
# unlink the object from the scene
bpy.context.scene.objects.unlink(bpy.data.objects["Bird"])
#for obj in bpy.data.objects:
#	print('Un objeto es ' + obj.name)
'''
################################################################################
#
# IMPLEMENTACION DE DANIEL
#
################################################################################

# Cargar el archivo XML a memoria, en una estructura mas facilmente entendible
# {

print ('Parsin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

import xml.dom.minidom

doc = xml.dom.minidom.parse(ARTIFACTS_PATH + 'script.xml')

actors = {}

for xmlActor in doc.getElementsByTagName('actor'):
    a = {}

    # Asigno los valores de los atributos de este elemento
    for attr_key in xmlActor.attributes.keys():
        a[attr_key] = xmlActor.getAttribute(attr_key)

    #Asigno el valor de la posicion del elemento
    for xmlPosition in xmlActor.getElementsByTagName('position'):
        #a['position'] = ( float(xmlPosition.getAttribute('x')) * POSITION_SCALE_W , float(xmlPosition.getAttribute('y')) * POSITION_SCALE_W , -float(xmlPosition.getAttribute('z')) * POSITION_SCALE_H, 0 )
        a['position'] = ( float(xmlPosition.getAttribute('x')), float(xmlPosition.getAttribute('y')), float(xmlPosition.getAttribute('z')))

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

# }

# Crear los objetos en las posiciones que nos hayan dicho en el XML

import mathutils
import pprint

bb_max = None
bb_min = None

# Preparamos objetos para agregar sonido
import xml.dom.minidom
score = xml.dom.minidom.parse(ARTIFACTS_PATH + 'score.xml') # Creamos arbol XML score
i = 0

print ('Drawin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

for actor in actors.keys():

    if actors[actor]['asset'] == 'SBCamera':
        continue
    
    if actors[actor]['asset'] == 'Ardilla':
        actors[actor]["unlink"] = False 
        #bpy.ops.wm.link_append(directory=ARTIFACTS_PATH + 'sackboy.blend/Object/', filename="SackboyMO", link=False)
        #bpy.context.scene.objects.active = bpy.data.objects['Sackboy']
        #bpy.context.object.scale = (0.3, 0.3, 0.3)
    
    #if bpy.context.object == None:
        #continue
    
    #ob = bpy.context.object
    #ob.name = actors[actor]['asset']
    #ob.location = actors[actor]['position']
    
    # Voy calculando donde debe quedar la camara (en caso de que no me digan donde de manera explicita) 
    # con base en la posicion de cada elemento de la escena:
    # La camara debe estar por sobre el centro del BoundingBox que contiene a todos los elementos, y mirando
    # hacia abajo
    '''
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
        bb_max[2] = max( bb_max[2] , ob.location[2] )'''

#for actor in actors.keys():
    if len(actors[actor]['trajectory']) == 0:
        continue
        
    obj = bpy.data.objects[actor]
    obj.select = True
    bpy.context.scene.objects.active = obj
    obj.location = (0,0,0)
    bpy.ops.object.constraint_add(type = 'FOLLOW_PATH')
    
    bpy.ops.curve.primitive_nurbs_path_add()
    curve_curve = bpy.data.curves[bpy.context.object.name]
    spline_points = bpy.data.curves[bpy.context.object.name].splines[0].points
    
    obj.constraints[0].target = bpy.context.object
    obj.constraints[0].use_curve_follow = True
    
    curve_curve.path_duration = NUM_FRAMES_ANIMATION
    
    bpy.context.scene.frame_current = 1
    curve_curve.eval_time = 0
    curve_curve.keyframe_insert(data_path = 'eval_time') 
    
    bpy.context.scene.frame_current = NUM_FRAMES_ANIMATION
    curve_curve.eval_time = NUM_FRAMES_ANIMATION
    curve_curve.keyframe_insert(data_path = 'eval_time') 
    
    # Muestreo la trayectoria que debe seguir el objeto en 5 puntos equidistantes, y con ellos construyo un spline
    trajectory_points = actors[actor]['trajectory'];
    
    # Voy a muestrear algunos puntos de la trayectoria apra hcrear la curva, es decir que no los voy a suar todos necesariamente
    # 'traj_step' es cada cuatos puntos voy a tomar una muestra.
    # 'num_points_curve' es cuantos puntos en total tendra la curva
    if len(trajectory_points) < NUM_POINTS_CURVE:
        traj_step = 1
        num_points_curve = len(trajectory_points)
    else:
        traj_step = int(len(trajectory_points) / NUM_POINTS_CURVE)
        num_points_curve = NUM_POINTS_CURVE
    
    if num_points_curve > 5:
        spline_points.add(num_points_curve - 5) # por defecto vienen 5 puntos

    for i in range(num_points_curve):
        spline_points[i].co = ( trajectory_points[i*traj_step][0] , trajectory_points[i*traj_step][1] , trajectory_points[i*traj_step][2] , 1)

    obj.select = False

for actor in actors.keys():
	print('actor ' + actors[actor]['asset'] + 'estara: ' + str(actors[actor]['unlink']))

################################################################################
#
# IMPLEMENTACION SONIDO
#
################################################################################

#
# FOLEY
#
i = 0;
print ('Foleyin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

for actor in actors.keys():
    for tagScore in score.getElementsByTagName('score'): # score
        for tagActor in tagScore.getElementsByTagName('actor'): # actor
            if actors[actor]['asset'] == tagActor.getAttribute('asset'): # hay un actor que en el score se llama igual

                # creo speaker con su sonido
                bpy.context.scene.frame_current = 1 # posicion en timeline donde quiero que se escuche el speaker
                bpy.ops.object.speaker_add(location=actors[actor]['position']) # agregamos speaker en posicion en escena
                bpy.ops.sound.open_mono(filepath=tagActor.getElementsByTagName('sound')[0].getAttribute('value')) # agregamos sonido
                bpy.data.speakers[i].sound = bpy.data.sounds[i] # extraemos de los sonidos de escena

                # uso propiedades para sonorizacion 3D
                bpy.data.speakers[i].volume_min = 0 # valor mínimo de volumen no importa qué tan lejos esté el speaker
                bpy.data.speakers[i].volume_max = 1
                bpy.data.speakers[i].attenuation = 3
                bpy.data.speakers[i].distance_reference = 10

                # agrego copias de strips en los frames dados por el actor en el score
                #for tagFrame in tagActor.getElementsByTagName('frame'):
                    
                    #bpy.context.scene.frame_current = int(tagFrame.getAttribute('number'))
                    #bpy.ops.nla.soundclip_add()

                # agrego un parent para que cuando el parent cambie de posicion el speaker se escuche en esa posicion
                #bpy.context.active_object.parent = ob

                # deselecciono todo en el editor nla
                # esto es porque necesito en los demas speakers hacer copias de uns trip de sonido en el mismo track
                #for soundTrack in bpy.context.active_object.animation_data.nla_tracks:
                    #soundTrack.select = False
                    #for stripOfTrack in soundTrack.strips:
                        #stripOfTrack.select = False

#
# Fondo
#

print ('Ambientin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

x = 0 #TODO: ¿Que pasa si inicializo en una sola linea?
y = 0
z = 0
i = len(bpy.data.speakers)
for tagScore in score.getElementsByTagName('score'): # score
	for tagScene in tagScore.getElementsByTagName('scene'): # scene
		for tagPoint in tagScene.getElementsByTagName('point'): # point
			
			# obtengo puntos
			x = tagPoint.getAttribute('x') 
			y = tagPoint.getAttribute('y')
			z = tagPoint.getAttribute('z')
			
			# creo speaker con su sonido
			bpy.context.scene.frame_current = 1 																# posicion en timeline donde quiero que se escuche el speaker
			bpy.ops.object.speaker_add(location=(int(x), int(y), int(z))) 										# agregamos speaker en posicion en escena
			bpy.ops.sound.open_mono(filepath=tagScene.getElementsByTagName('sound')[0].getAttribute('value')) 	# agregamos sonido
			bpy.data.speakers[i].sound = bpy.data.sounds[i] 													# extraemos de los sonidos de escena
			
			# uso propiedades para sonorizacion 3D
			bpy.data.speakers[i].volume_min = 0 																# valor mínimo de volumen no importa qué tan lejos esté el speaker
			bpy.data.speakers[i].volume_max = 1
			bpy.data.speakers[i].attenuation = 3
			bpy.data.speakers[i].distance_reference = 10
			
			# deselecciono todo en el editor nla
			# esto es porque necesito en los demas speakers hacer copias de uns trip de sonido en el mismo track
			#for soundTrack in bpy.context.active_object.animation_data.nla_tracks:
                            #soundTrack.select = False
                            #for stripOfTrack in soundTrack.strips:
                                #stripOfTrack.select = False
    				
			i = i + 1 # incremento i

################################################################################
#
# IMPLEMENTACION CAMARA
#
################################################################################

print ('Filmin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

'''
bpy.ops.object.camera_add()
camera = bpy.context.object
if 'SBCamera' in actors:
    camera.location = actors['SBCamera']['position']
else:
    camera.location =  ( bb_max + bb_min ) / 2
    camera.location[2] = 15
bpy.context.scene.camera = camera    
'''
bpy.ops.object.camera_add()	
camera = bpy.data.objects["Camera"]
camera.location[0] = 7
camera.location[1] = -6
camera.location[2] = 7
bpy.context.scene.camera = camera

rx = 55.0
ry = 0.0
rz = 35.0
pi = 3.14159265

camera.rotation_mode = 'XYZ'
camera.rotation_euler[0] = rx*(pi/180.0)
camera.rotation_euler[1] = ry*(pi/180.0)
camera.rotation_euler[2] = rz*(pi/180.0)

bpy.ops.sound.bake_animation() # Limpia la cache del sonido

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = NUM_FRAMES_ANIMATION
bpy.context.scene.frame_current = 1

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

# Renderizar la imagen o el video

# uso propiedades de render
bpy.context.scene.camera = camera
bpy.context.scene.render.parts_x = 1
bpy.context.scene.render.parts_y = 1
bpy.context.scene.render.use_sss = False

# reduzo tiempo de generacion de las imagenes
bpy.context.scene.render.use_raytrace = False
bpy.context.scene.render.use_envmaps = False
bpy.context.scene.render.use_textures = False
bpy.context.scene.render.use_shadows = False
bpy.context.scene.render.use_antialiasing = False

# renderizo a video MPEG
bpy.context.scene.render.image_settings.file_format='FFMPEG'
bpy.context.scene.render.filepath = ARTIFACTS_PATH + 'output.mpg'
bpy.context.scene.render.ffmpeg.audio_codec = 'MP3'
bpy.context.scene.render.ffmpeg.video_bitrate = 1024 # Quota de transmision de video
bpy.ops.render.render(animation=True)

print ('THE END AT: ')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')


'''
HOW 2 TEST:
	/Users/barcodepandora/Downloads/blender-2.62release-OSX_10.5_i386/blender.app/Contents/MacOS/blender -P /Users/barcodepandora/Dropbox/tesis/animacion/SoundFilmGenerator.py -b /Users/barcodepandora/Dropbox/tesis/animacion/empty_scene.blend > /Users/barcodepandora/Dropbox/tesis/animacion/SoundFilm.log
TODO:
	animaciones + extensas
'''
