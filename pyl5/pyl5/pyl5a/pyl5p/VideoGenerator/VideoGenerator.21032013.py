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

import xml.dom.minidom
import pprint


POSITION_SCALE_W = 16
POSITION_SCALE_H = 8
DEFAULT_CAMERA_ALTITUDE = 12 
FRAME_STEP = 2
NUM_POINTS_CURVE = 5
NUM_FRAMES_ANIMATION = 1

import os

MODELS_PATH = '/var/www/pyl2/VideoGenerator'
RENDER_LOW_QUALITY = "True"
RENDER_VIDEO = os.getenv('RENDER_VIDEO') == "True"
SCRIPT_XML_FILENAME = os.getenv('SCRIPT_XML_FILENAME')
SCORE_XML_FILENAME = os.getenv('SCORE_XML_FILENAME')

from time import gmtime,strftime

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
    #a["unlink"] = True 

# Invocar al API de Blender para crear los actores y acomodar todos los elementos en la escena

import bpy
import mathutils

# Borrar todo lo que haya en la escena:
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

for tmp_curve in bpy.data.curves:
    bpy.data.curves.remove(tmp_curve)

for tmp_mesh in bpy.data.meshes:
    bpy.data.meshes.remove(tmp_mesh)

# Para el calculo del BoundingBox de la escena mas abajo
bb_min = None
bb_max = None

# bpy.ops.sequencer.sound_strip_add(filepath='/Users/barcodepandora/Sites/VideoGenerator/sound/jazz.mp3', frame_start=1, channel=1)
print ('##### INICIO #####')
print (strftime('%Y-%m-%d %H:%M:%S', gmtime()))
# Crear los objetos en las posiciones que nos hayan dicho en el XML
for actor in actors.keys():
    if actors[actor]['asset'] == 'SBCamera':
        continue
    
    if actor.startswith("elven") or actor.startswith("casa"):
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius=0.3, depth=1, cap_end=True)
    elif actor.startswith("medieval"):
        #bpy.ops.mesh.primitive_cube_add()
        bpy.ops.mesh.primitive_monkey_add()
        bpy.context.object.scale = (0.3, 0.3, 0.3)
    elif actor.startswith("dessert") or actor.startswith("carro"):
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/desertTruck.blend/Object/", filename="DragonMO", link=False)
        bpy.context.scene.objects.active = bpy.data.objects['Dragon']
        bpy.context.object.scale = (0.3,0.3,0.3)
    elif actor.startswith("robot") or actor.startswith("hombre") :
        bpy.ops.import_scene.autodesk_3ds(filepath=MODELS_PATH + "/robot.3ds")
        bpy.context.scene.objects.active = bpy.data.objects['Dexter']
        bpy.context.object.scale = (0.01,0.01,0.01)
   # elif actor.startswith("ninja") or actor.startswith("mujer"):
       # bpy.ops.wm.link_append(directory=MODELS_PATH + "/sackboy.blend/Object/", filename="SackboyMO", link=False)
       # bpy.context.scene.objects.active = bpy.data.objects['Sackboy']
       # bpy.context.object.scale = (0.3, 0.3, 0.3)
    elif actor.startswith("Rabbit"):
	#actors[actor]["unlink"] = False
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/rabbit.blend/Object/", filename="rabbit", link=False)
        bpy.context.scene.objects.active = bpy.data.objects['rabbit']
        bpy.context.object.scale = (1.0,1.0,1.0)
    elif actor.startswith("Squirrel"):
	#actors[actor]["unlink"] = False
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/squirrel.blend/Object/", filename="squirrel", link=False)
        bpy.context.scene.objects.active = bpy.data.objects['squirrel']
        bpy.context.object.scale = (1.5,1.5,1.5)
    elif actor.startswith("Chinchilla"):
        #actors[actor]["unlink"] = False
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/chinchilla.blend/Object/", filename="chinchilla", link=False)     
        bpy.context.scene.objects.active = bpy.data.objects['chinchilla']
        bpy.context.object.scale = (1.5,1.5,1.5)
    elif actor.startswith("Butterfly"):
        #actors[actor]["unlink"] = False
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/butterfly.blend/Object/", filename="butterfly_body", link=False)
        bpy.context.scene.objects.active = bpy.data.objects['butterfly_body']
        bpy.context.object.scale = (8,8,8)
    elif actor.startswith("Bird"):
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/bird.blend/Object/", filename="Bird", link=False)
        bpy.context.scene.objects.active = bpy.data.objects['Bird']
        bpy.context.object.scale = (0.12,0.12,0.12)
    elif actor.startswith("Apple"):
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/apple.blend/Object/", filename="apple1", link=False)
        bpy.context.scene.objects.active = bpy.data.objects['apple1']
        bpy.context.object.scale = (3,3,3)
    elif actor.startswith("FlyingSquirrel"):
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/flyingsquirrel.blend/Object/", filename="FlyingSquirrel", link=False)
        bpy.context.scene.objects.active = bpy.data.objects['FlyingSquirrel']
        bpy.context.object.scale = (1.5,1.5,1.5)
    else:
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/pear.blend/Object/", filename="pearXL", link=False)
        bpy.context.scene.objects.active = bpy.data.objects['pearXL']
        bpy.context.object.scale = (2.0,2.0,2.0)
        #bpy.ops.mesh.primitive_cylinder_add(radius=0.3)
        
    ob = bpy.context.object
    ob.name = actors[actor]['asset']
    ob.location = actors[actor]['position']
    #ob.location[2] = ob.location[2]+5.0
    print('Object '+ob.name+' '+str(actors[actor])+'.')
    print(ob.location) 

    # Voy calculando donde debe quedar la camara (en caso de que no me digan donde de manera explicita) con base en la posicion de cada elemento de la escena:
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

print('bb_min')
print(bb_min)
print('bb_max')
print(bb_max)
    
# Crear el piso
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="matte_hills", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_hills']
bpy.context.object.scale = (0.055,0.055,0.07)
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(0.0,0.0,-0.4622))
print('Matte_hills')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="matte_haze", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_haze']
bpy.context.object.scale = (0.051,0.051,0.051)
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(0.0,0.0,59.4459))
print('Matte_haze')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="matte_sky", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_sky']
bpy.context.object.scale = (0.05,0.05,0.05)
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(0.0,0.0,-0.6622))
print('Matte_sky')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="matte_clouds", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_clouds']
bpy.context.object.scale = (0.055,0.055,0.07)
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(0.0,0.0,57.8609))
bpy.ops.transform.rotate(value=(-0.5235,), constraint_axis=(False,False,True))
print('Matte_clouds')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="smellingfield_ground", link=False)
bpy.context.scene.objects.active = bpy.data.objects['smellingfield_ground']
bpy.context.object.scale = (1.0,1.0,1.0)
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(11.5,0.0,-0.5))
print('Smelling_Field_Ground')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="kite_trees_big1", link=False)
bpy.context.scene.objects.active = bpy.data.objects['kite_trees_big1']
bpy.context.object.scale = (0.1,0.1,0.15)
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(128.0,-15.0,2.24))
print('Kite_Trees_Big')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.001", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.002", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.003", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.004", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.005", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.006", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.007", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.008", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.009", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.010", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.011", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.012", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="lightbeam", link=False)
'''bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/sets/intro.blend/Object/", filename="ground", link=False)
bpy.context.scene.objects.active = bpy.data.objects['ground']
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(7.0,0.0,-2.005))
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/sets/intro.blend/Object/", filename="grass_ground", link=False)
bpy.context.scene.objects.active = bpy.data.objects['grass_ground']
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(7.0,0.0,-2.105))
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/sets/intro.blend/Object/", filename="matte_forest_treeA", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_forest_treeA']
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(-20.0,-76.0,10.4883))
print('Matte_Forest_treeA')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/sets/intro.blend/Object/", filename="matte_forest_treeB", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_forest_treeB']
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(-16.0,-51.0,5.3335))
print('Matte_Forest_treeB')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/sets/intro.blend/Object/", filename="matte_forest_treeC", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_forest_treeC']
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(0.0,-54.0,7.9643))
print('Matte_Forest_treeC')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/sets/intro.blend/Object/", filename="matte_forest_treeD", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_forest_treeD']
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(39.8691,-196.2142,22.3492))
print('Matte_Forest_treeD')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/sets/intro.blend/Object/", filename="matte_forest_treeD", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_forest_treeD']
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(36.8691,-196.2142,22.3492))
print('Matte_Forest_treeD')
print(bpy.context.object.location)'''

# Agregar la camara

bpy.ops.object.camera_add()
camera = bpy.context.object
bpy.ops.object.lamp_add()
lamp = bpy.context.object
camera.location[0] = ( bb_max[0] + bb_min[0] ) / 2
camera.location[1] = ( (bb_max[1] + bb_min[1]) - 26 ) / 2
camera.location[2] = DEFAULT_CAMERA_ALTITUDE / 3
print('Camera')
print(camera.location)

bpy.context.scene.camera = camera

#Agregar lampara a la escena
lamp.location = mathutils.Vector(ob.location)
lamp.location[0] = ( bb_max[0] + bb_min[0] ) / 2
lamp.location[1] = ( (bb_max[1] + bb_min[1]) - 5 ) / 2
lamp.location[2] = ob.location[2] + 5
print('Lamp location')
print(lamp.location)

# Agregar Rotaciones de Camara
rx = 84.0
ry = 0.0
rz = 0.0

pi = 3.14159265

camera.rotation_mode = 'XYZ'
camera.rotation_euler[0] = rx*(pi/180.0)
camera.rotation_euler[1] = ry*(pi/180.0)
camera.rotation_euler[2] = rz*(pi/180.0)

# Agregar Fondo de la Escena - Cielo
world = bpy.context.scene.world
# World settings
world.use_sky_blend = True
world.ambient_color = (0.030, 0.030, 0.030)
world.horizon_color = (0.0883, 0.272, 0.704)
world.zenith_color = (0.04, 0.0, 0.04)
# Stars
sset = world.star_settings
sset.use_stars = True
sset.average_separation = 7.8
sset.color_random = 1.0
sset.distance_min = 0.7
sset.size = 10
# Environment lighting
wset = world.light_settings
wset.use_environment_light = True
wset.environment_color = 'PLAIN'
wset.environment_energy = 1.0
wset.use_ambient_occlusion = True
wset.ao_blend_type = 'MULTIPLY'
wset.ao_factor = 0.8
wset.gather_method = 'APPROXIMATE'

# Realizar animaciones

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = NUM_FRAMES_ANIMATION

score = xml.dom.minidom.parse(SCORE_XML_FILENAME)

# Crear el sonido de ambiente
#for xmlScore in score.getElementsByTagName('score'):
#	for xmlAmbient in xmlScore.getElementsByTagName('scene'):
#		bpy.ops.sequencer.sound_strip_add(filepath=xmlAmbient.getAttribute('value'), frame_start=1, channel=1)

for actor in actors.keys():
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

    print(ground_plane.active_material.name.split('.')[0])
    print(actor.split('_')[0])

    for i in range(num_points_curve):
        spline_points[i].co = ( trajectory_points[i*traj_step][0] , trajectory_points[i*traj_step][1] , trajectory_points[i*traj_step][2] , 1)
        if spline_points[i].co[0] < ground_plane.dimensions[0]:
        	floor = ground_plane.active_material.name.split('.')[0]
        	frame_limit = (NUM_FRAMES_ANIMATION / num_points_curve) * (i + 1)
        	for xmlScore in score.getElementsByTagName('score'):
        		for xmlActor in xmlScore.getElementsByTagName('actor'):
        			if xmlActor.getAttribute('asset') == actor.split('_')[0]:
        				for xmlFrame in xmlActor.getElementsByTagName('frame'):
        					if frame_limit > int(xmlFrame.getAttribute('number')):
        						for xmlSound in xmlFrame.getElementsByTagName('sound'):
        							if xmlSound.getAttribute('key') == floor:
        								bpy.ops.sequencer.sound_strip_add(filepath=xmlSound.getAttribute('value'), frame_start=int(xmlFrame.getAttribute('number')), channel=2)
    obj.select = False
    

bpy.context.scene.frame_current = 1

# }


# Renderizar la imagen o el video
# {
bpy.context.scene.camera = camera
bpy.context.scene.render.parts_x = 1
bpy.context.scene.render.parts_y = 1
bpy.context.scene.render.use_sss = False
    
if RENDER_LOW_QUALITY:
    bpy.context.scene.render.use_raytrace = False
    bpy.context.scene.render.use_envmaps = False
    bpy.context.scene.render.use_textures = True
    bpy.context.scene.render.use_shadows = False
    bpy.context.scene.render.use_antialiasing = False
else:
    bpy.context.scene.render.use_raytrace = True
    bpy.context.scene.render.use_envmaps = True
    bpy.context.scene.render.use_textures = True
    bpy.context.scene.render.use_shadows = True
    bpy.context.scene.render.use_antialiasing = True


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
print ('##### FIN #####')
print (strftime('%Y-%m-%d %H:%M:%S', gmtime()))
bpy.ops.wm.save_mainfile(filepath="output.blend", check_existing=False)
