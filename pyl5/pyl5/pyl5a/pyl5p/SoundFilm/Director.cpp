/*
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
*/

/*
 *  Director.cpp
 *  SoundFilm
 *
 *  Created by Juan Manuel Moreno on 12/05/12.
 *  Copyright 2012 __MyCompanyName__. All rights reserved.
 *
 */

#include "Director.h"
#include "stdio.h"
#include "stdlib.h"
#include <string>
using std::string;
#include <sstream>
#include "tinyxml.h"

#define TIME 4

/*Director::Director()
{
	vocabulary = NULL;
	script = NULL;

}*/

Director::Director(	const char* aVocabulary, 
					const char* aScript, 
					const char* aScore, 
					const char* aSoundsActors, 
					const char* aSoundsAnimations)
{

	vocabulary = aVocabulary;
	script = aScript;
	score = aScore;
	soundsActors = aSoundsActors;
	soundsAnimations = aSoundsAnimations;
	temporal = ( ( (string)score ).substr(0, strlen(score) - 9) ).c_str();
	printf("temporal = %s\n", temporal);
}

Director::~Director()
{
}

// Verifica que dos elementos coincidan en asset
bool coinciden(TiXmlNode* actorScript, TiXmlNode* object) 
{
	if( ( (string)actorScript->ToElement()->Attribute("asset") ).compare( 
		(string)object->ToElement()->Attribute("asset") ) == 0 ) {
		
		return true;
	}
	return false;
}

// Verifica si un sonido es periodico
bool isPeriodic(TiXmlElement *eventE)
{
	if( eventE->Attribute("framestart") != NULL) {
		
		return true;
	}
	return false;
}

// Crea un archivo de sonido
void createSoundXElement(TiXmlElement* soundScore, int time, int delay, string soundValue, string temporal)
{
	TiXmlElement* frameScore; 
	for (int i = 0; i <= (time / delay); i++) {

		printf("copiando %s en %stmp_%d.wav\n", soundValue.c_str(), temporal.c_str(), (i + 1));
		char text[325];
		sprintf(text, "cp %s %stmp_%d.wav", soundValue.c_str(), temporal.c_str(), (i + 1)); // Creo una copia para combinar las copias despues
		system(text);
	}
	char text[425];

	/*
	Tareas:
	Usar .wav
	Hacer copias del sonido con sox
	Producir el sonido completo con las copias con sox
	Traducir a un archivo de sonido leible por blender con ffmpeg
	*/
	sprintf(text, "../sox-14.3.0/src/sox %stmp*.wav %stmpgarage.wav", temporal.c_str(), temporal.c_str());
	system(text);
	soundValue = temporal + soundValue.substr(3, strlen(soundValue.c_str()) - 1); //ojo con ese substring, se supone que es para obtener solo el nombre del archivo...
	sprintf(text, "../ffmpeg -y -i %stmpgarage.wav -ab 128k -ar 44100 %s.mp3", temporal.c_str(), soundValue.c_str()); // -y fuerza el sobreescribir
	printf("../ffmpeg -y -i %stmpgarage.wav -ab 128k -ar 44100 %s.mp3   ", temporal.c_str(), soundValue.c_str());
	system(text);
	soundScore->SetAttribute("value", (soundValue + ".mp3").c_str());
	sprintf(text, "rm -rf %stmp*", temporal.c_str());
	system(text);
}

// Escribe un elemento en score
void writeSceneScore(	TiXmlElement* elementScore, 
						TiXmlNode* soundLibrary, 
						TiXmlNode* object, 
						int time, 
						TiXmlNode* actorScript, 
						TiXmlElement* sceneScore,
						const char* ambientSound,
						TiXmlAttribute* temporal)
{

	string sceneAsset = (string)object->ToElement()->Attribute("asset") ;

	// Material
	//sceneScore->SetAttribute("material", scene->ToElement()->Attribute("material"));
	
	// Tipo de sonido. 
	int delay;
	if ( ( (string)object->ToElement()->Attribute("typeofsound") ).compare("voice") ) { // Voz aplica delay.
	
		delay = atoi( ( (string)object->ToElement()->Attribute("delay") ).c_str() );
	} else if ( ( (string)object->ToElement()->Attribute("typeofsound") ).compare("ambient") ) { // Ambiente no tiene delay.
	
		delay = 1;
	}
	sceneScore->SetAttribute("asset", sceneAsset.c_str()); // Nombre del objeto escena.
	elementScore->LinkEndChild( sceneScore );
	string soundValue;
	TiXmlElement* soundScore;
	TiXmlNode* point;
	TiXmlElement* pointScore;
	for( TiXmlNode* soundOfLibrary = soundLibrary->IterateChildren("sound", 0); 
		soundOfLibrary; soundOfLibrary = soundLibrary->IterateChildren("sound", soundOfLibrary))
	{
		
		// Atributos de nombre de ambiente de los dos nodos son iguales
		if( ( (string)soundOfLibrary->ToElement()->Attribute("name") ).compare( (string)ambientSound ) == 0 ) {
			soundScore = new TiXmlElement( "sound" ); // Creamos elemento sonido.
			soundValue = (string)soundOfLibrary->ToElement()->Attribute("value");		
			point = actorScript->FirstChild("position"); // Agregamos elemento punto nuevo.
			pointScore = new TiXmlElement( "point" );
printf("you can do it\n"); 
			pointScore->SetAttribute("x", point->ToElement()->Attribute("x"));
			pointScore->SetAttribute("y", point->ToElement()->Attribute("z"));
			pointScore->SetAttribute("z", "0");
printf("you can do it\n");
			sceneScore->LinkEndChild( soundScore );
printf("you can do it\n");
			sceneScore->LinkEndChild( pointScore );
			printf("temporal string = %s\n", temporal->Value());
			createSoundXElement(soundScore, time, delay, soundValue, temporal->Value());

		}	
	}
}

// Extiende el script
void extendScript(TiXmlNode* actorsScript)
{
	TiXmlDocument docScript( "/var/www/pyl3/ImageProcessing/SoundFilm/scriptnature.xml" );
	bool loadOk = docScript.LoadFile();
	if (loadOk) {
		
		printf("el script alternativo es valido\n");
	}
	TiXmlNode* actors = docScript.FirstChild("actors"); // Objetos.
	TiXmlElement* actorClone;
	TiXmlNode* point;
	TiXmlElement* pointActor;
	for( TiXmlNode* actor = actors->IterateChildren("actor", 0); 
		actor; actor = actors->IterateChildren("actor", actor))
	{
		actorClone = new TiXmlElement( "actor" );
		actorClone->SetAttribute("asset", actor->ToElement()->Attribute("asset"));
		actorClone->SetAttribute("animation", actor->ToElement()->Attribute("animation"));
		actorClone->SetAttribute("facing", actor->ToElement()->Attribute("facing"));
		actorClone->SetAttribute("scaleOffset", actor->ToElement()->Attribute("scaleOffset"));
		point = actor->FirstChild("position"); // Agregamos elemento punto nuevo.
		pointActor = new TiXmlElement( "position" ); 
		pointActor->SetAttribute("x", point->ToElement()->Attribute("x"));
		pointActor->SetAttribute("y", point->ToElement()->Attribute("y"));
		pointActor->SetAttribute("z", point->ToElement()->Attribute("z"));
		actorClone->LinkEndChild( pointActor );
		actorsScript->LinkEndChild( actorClone );
	}
}

string defaultAmount(TiXmlNode* actors)
{
	printf("Contando la cantidad de actores...\n");
	string text = "";
	for( TiXmlNode* actor = actors->IterateChildren("actor", 0); 
		actor; actor = actors->IterateChildren("actor", actor))
	{
		text=text+"Default*";
	}
	printf( "Valor definido:%s\n",text.c_str() );
	return text;	
}

void Director::compose(void)
{

	// Objetos lectura
	TiXmlNode* actions; // Acciones.
	TiXmlNode* action;
	string sceneAsset;
	int delay;
	string ambientSound;
	string emotionName;
	string emotionSound;
	const char* selectedSound;
	
	TiXmlNode* events; // Eventos.
	TiXmlNode* event;
	TiXmlElement *eventE;
	TiXmlNode* eventLibrary;
	TiXmlNode* eventOfLibrary;
	
	TiXmlElement* soundE; // Sonidos.
	TiXmlNode* soundLibrary;
	TiXmlNode* soundOfLibrary;
	
	TiXmlNode* material; // Otros.
	TiXmlNode* frame;
	TiXmlElement* frameE;
	
	// Objetos escritura
	TiXmlDocument documentScore;
	TiXmlElement * elementScore;
	TiXmlElement * actorScore;
	TiXmlElement * soundScore;
	TiXmlElement * foleyScore;

	// Salvamos temporal
	string stemporal = (string)temporal;
	
	// Extraemos simbolos del script que necesitamos.
	TiXmlDocument docScript( script );
	
	bool loadOk = docScript.LoadFile();
	if (loadOk) {
		
		printf("el script es valido\n");
	}
	
	// Objetos lectura script
	TiXmlNode* compositions = docScript.FirstChild("compositions"); // Objetos.
	TiXmlNode* composition;
	TiXmlNode* actorsScript;
	TiXmlNode* actorScript;
			
	// Escribimos encabezado score.
	TiXmlDeclaration * decl = new TiXmlDeclaration( "1.0", "", "" );
	documentScore.LinkEndChild( decl );
	elementScore = new TiXmlElement( "score" );
	documentScore.LinkEndChild( elementScore );
	
	// Archivo XML.
	TiXmlDocument doc( vocabulary );
	loadOk = doc.LoadFile();
	if (loadOk) {
		
		printf("el vocabulario es valido\n");
	}
	
	// Objetos lectura vocabulario.
	TiXmlNode* objects = doc.FirstChild("objects"); // Objetos.
	TiXmlNode* object;
	TiXmlNode* scene;

	// Extendemos script para bosque y mar
	composition = compositions->FirstChild("composition" );
	//extendScript(composition->FirstChild("actors" ));
	//docScript.SaveFile( script );
	
	
	//arreglo para los default.....
	//string defaultText=defaultAmount( composition->FirstChild("actors" ) );
	//const char* soundsActors = defaultText.c_str();
	//const char* soundsAnimations = defaultText.c_str();
	for (int n = 0; n < 10 ; n++)
	{
		listSoundsActors[n] = "Default";
		listSoundsAnimations[n] = "Default";
	}
	
			
	// Recorremos objetos
	printf("listo para los objetos\n");
	for( object = objects->IterateChildren("object", 0); 
		object; object = objects->IterateChildren("object", object))
	{

		printf("el objeto que da es %s\n", ( (string)object->ToElement()->Attribute("asset") ).c_str());
	   // Verificamos que el objeto tenga un sonido asociado a una emocion
	   if (object->ToElement()->Attribute("emotion") != NULL) {

		   emotionName = (string)object->ToElement()->Attribute("emotion") ;
		   eventLibrary = objects->FirstChild("emotionlibrary");
		   for( eventOfLibrary = eventLibrary->IterateChildren("event", 0); 
			   eventOfLibrary; eventOfLibrary = eventLibrary->IterateChildren("event", eventOfLibrary))
		   {
			   
			   // Atributos 'name' de los dos nodos son iguales
			   if( ( (string)object->ToElement()->Attribute("emotion") ).compare((string)eventOfLibrary->ToElement()->Attribute("name") ) == 0 ) {
				   
				   // Buscamos sonido de la emocion en la libreria.
				   soundE = eventOfLibrary->FirstChild("sound")->ToElement();
				   soundLibrary = objects->FirstChild("soundlibrary");
				   for( soundOfLibrary = soundLibrary->IterateChildren("sound", 0); 
					   soundOfLibrary; soundOfLibrary = soundLibrary->IterateChildren("sound", soundOfLibrary))
				   {
					   
					   // Atributos 'name' de los dos nodos son iguales
					   if( ( (string)soundE->Attribute("name") ).compare( 
																		 (string)soundOfLibrary->ToElement()->Attribute("name") ) == 0 ) {
						   
							// Escribimos sonido.
							emotionSound = (string)soundOfLibrary->ToElement()->Attribute("value"); 
						}
					}
				}
			}
	   	}

printf("el objeto que da es %s\n", ( (string)object->ToElement()->Attribute("asset") ).c_str());	   
		// Obtenemos composiciones
		composition = compositions->FirstChild("composition" );
		
		// Obtenemos actores
		actorsScript = composition->FirstChild("actors" ); 

		// Obtenemos sonidos de actores y animaciones
		// Si lo hago por fuera del for no hace nada
		char str[100];
		strncpy(str, soundsActors, sizeof(str));
		char* temp = strtok (str, "*");
		int i = 0;
		const char* soundWithBlank;
		char soundWithBlank2[100];
		while (temp != NULL)
		{
			soundWithBlank = temp;
			strncpy(soundWithBlank2, soundWithBlank, sizeof(soundWithBlank) -1);
			listSoundsActors[i] = soundWithBlank2;
			temp = strtok (NULL, "*");
			i++;
		}
		strncpy(str, soundsAnimations, sizeof(str));
		temp = strtok (str, "*");
		i = 0;
		const char* soundWithBlank3;
		char soundWithBlank4[100];
		while (temp != NULL)
		{
			soundWithBlank3 = temp;
			strncpy(soundWithBlank4, soundWithBlank3, sizeof(soundWithBlank3) -1);
			listSoundsAnimations[i] = soundWithBlank4;		
			temp = strtok (NULL, "*");
			i++;
		}

		// Recorremos actores de script.
		printf("listo para los actores\n");
		int counteractors = 0;
		int counter = 0;
		for( actorScript = actorsScript->IterateChildren("actor", 0); 
			actorScript; actorScript = actorsScript->IterateChildren("actor", actorScript))
		{
			// Verificamos que en script hay un actor que tenga una trayectoria
			// y coincida con el objeto en asset.
			printf("el actor que da es %s\n", ( (string)actorScript->ToElement()->Attribute("asset") ).c_str());
			if ( coinciden(actorScript, object) ) {
							   
			   printf("el objeto que da es %s\n", ( (string)object->ToElement()->Attribute("asset") ).c_str());
			   // Verificamos que el objeto tenga un sonido
			   // Un objeto puede tener un tipo de sonido ambiente o fondo, o voz
			   if (object->ToElement()->Attribute("typeofsound") != NULL &&
					(	((string)object->ToElement()->Attribute("typeofsound")).compare("ambient") == 0 ||
						((string)object->ToElement()->Attribute("typeofsound")).compare("voice") == 0)) {

					printf("es fondo o voz\n");
					if ( ( (string)object->ToElement()->Attribute("typeofsound") ).compare("ambient") == 0 ) {
					
						selectedSound = object->ToElement()->Attribute("sound") ;
					}
				   // Verificamos sonido escogido.
				   // Default continuamos.
					else if ( ( (string)listSoundsActors[counteractors] ).compare("Default") == 0 ) {
					
						printf("es el por defecto\n");
						selectedSound = object->ToElement()->Attribute("sound") ;
;
					} else {
					
						printf("es el que me da la lista de sonidos\n");
						selectedSound = listSoundsActors[counteractors];
					}
					counteractors++;
					//selectedSound = object->ToElement()->Attribute("sound") ;
					printf("el sonido por defecto del actor es %s\n", selectedSound);
					

				   // Escribimos etiqueta de escena con sonido.
					if ( ( (string)object->ToElement()->Attribute("typeofsound") ).compare("ambient") == 0 ) {
					
						actorScore = new TiXmlElement( "scene" ); // Nuevo elemento de una escena en score de fondo
					} else if ( ( (string)object->ToElement()->Attribute("typeofsound") ).compare("voice") == 0 ) {
					
						actorScore = new TiXmlElement( "actor" ); // Nuevo elemento de una escena en score de actor
					}				   

printf("hola\n");
				   // Completamos etiqueta
				   writeSceneScore( 
				   		elementScore, objects->FirstChild("soundlibrary"), 
				   		object, TIME, actorScript, actorScore, selectedSound, new TiXmlAttribute("value", stemporal.c_str())); 
printf("tu\n"); 			   
			} 

			   // Recorremos acciones
			   for( actions = object->IterateChildren("actions", 0); 
				   actions; actions = object->IterateChildren("actions", actions))
			   {
				   
				   // Recorremos accion
				   for( action = actions->IterateChildren("action", 0); 
					   action; action = actions->IterateChildren("action", action))
				   {
					   
					   // Si esta accion tiene un evento creamos elemento actor en score
					   // y ademas si la accion del actor coincide con la de la acción del objeto.
					   
					   // Ejercicio para el conejo
					   // Si el actor es un conejo
					   // Agregar acción por defecto levantarse
					   
					   printf("el actor es ::%s::\n", actorScript->ToElement()->Attribute("asset"));
					   printf("la animacion del actor es ::%s::\n", actorScript->ToElement()->Attribute("animation"));
					   printf("la de la acciones ::%s::\n", action->ToElement()->Attribute("animation"));
					   
					   if (	(	!action->NoChildren() &&
					   			( (string)actorScript->ToElement()->Attribute("animation") ).compare(
					   				(string)action->ToElement()->Attribute("animation") ) == 0 ) ||
					   			( ( (string)actorScript->ToElement()->Attribute("asset") ).compare("Conejo") == 0 ) ) 
					   {
						   
						   //actorScore = new TiXmlElement( "actor" );
						   //actorScore->SetAttribute("asset", object->ToElement()->Attribute("asset"));
						   //elementScore->LinkEndChild( actorScore );								
						   								   
						   // Recorremos eventos
						   for( events = action->IterateChildren("events", 0); 
							   events; events = action->IterateChildren("events", events))
						   {
							   
							   // Recorremos evento
							   for( event = events->IterateChildren("event", 0); 
								   event; event = events->IterateChildren("event", event))
							   {
								   
								  	// Hacemos etiqueta de foley null.
						   			foleyScore = NULL;

								   // Buscamos evento en libreria
								   eventE = event->ToElement();
								   eventLibrary = objects->FirstChild("eventlibrary");
								   for( eventOfLibrary = eventLibrary->IterateChildren("event", 0); 
									   eventOfLibrary; eventOfLibrary = eventLibrary->IterateChildren("event", eventOfLibrary))
								   {
									   
									   // Atributos 'name' de los dos nodos son iguales
									   if( ( (string)eventE->Attribute("name") ).compare( (string)eventOfLibrary->ToElement()->Attribute("name") ) == 0 ) {
										   
										   // Buscamos sonido del evento en la libreria.																			   
										   soundE = eventOfLibrary->FirstChild("sound")->ToElement();
										   printf("hay el evento y su sonido es %s::oiga\n", soundE->Attribute("name"));
										   printf("pero puede ser %s::oiga\n", listSoundsAnimations[counter]);
										   
										   // Verificamos sonido escogido.
										   // Default continuamos.
											if ( ( (string)listSoundsAnimations[counter] ).compare("Default") == 0 ) {
											
												printf("es el por defecto");
												selectedSound = soundE->Attribute("name");
											} else {
											
												printf("es el que me da la lista de sonidos\n");
												selectedSound = listSoundsAnimations[counter];
											}
											counter++;
											printf("el sonido por defecto de la accion es %s\n", selectedSound);
											
											
										   soundLibrary = objects->FirstChild("soundlibrary");
										   for( soundOfLibrary = soundLibrary->IterateChildren("sound", 0); 
											   soundOfLibrary; soundOfLibrary = soundLibrary->IterateChildren("sound", soundOfLibrary))
										   {
											   
											   // Atributos 'name' de los dos nodos son iguales
											   if( ( (string)selectedSound ).compare( (string)soundOfLibrary->ToElement()->Attribute("name") ) == 0 ) {
												   
												   // Creamos etiqueta foley
												   if (foleyScore == NULL) {
												   
												   		foleyScore = new TiXmlElement( "foley" );
												   		actorScore->LinkEndChild( foleyScore ); // Escribimos el sonido en el frame.
												   }
												   
												   
												   // Verificamos que es periodico
												   if (isPeriodic(eventE)) {
	
													   // Escribimos el sonido.
													   printf("es periodico ... \n");
													   material = soundOfLibrary->FirstChild("material");
													   soundScore = new TiXmlElement( "foley" );
																						   //soundScore->SetAttribute("key", material->ToElement()->Attribute("key"));
													   string soundValue = (string)material->ToElement()->Attribute("value");
													   int delay = atoi( ( (string)eventE->Attribute("delay") ).c_str() );
													   printf("creando un foley periodico... \n");
													   createSoundXElement(soundScore, TIME, delay, soundValue, stemporal);
													   //soundScore->SetAttribute("value", material->ToElement()->Attribute("value"));
													   soundScore->SetAttribute("frame", "1");
													   foleyScore->LinkEndChild( soundScore ); // Escribimos el sonido en el frame.
												   } else {
	
													   printf("no es periodico ... \n");
													   // Escribimos frames.
													   for( frame = event->IterateChildren("frame", 0); 
														   frame; frame = event->IterateChildren("frame", frame))
													   {
														   
														   printf("estoy en un frame ... \n");
														   frameE = new TiXmlElement( "frame" );
														   frameE->SetAttribute("number", frame->ToElement()->Attribute("number"));
														   
														   // Escribimos el sonido.
														   material = soundOfLibrary->FirstChild("material");
														   soundScore = new TiXmlElement( "foley" );
														   //soundScore->SetAttribute("key", material->ToElement()->Attribute("key"));
														   string soundValue = (string)material->ToElement()->Attribute("value");
														   int delay = atoi( ( (string)eventE->Attribute("delay") ).c_str() );
														   printf("creando un foley no periodico... \n");
														   createSoundXElement(soundScore, delay - 1, delay, soundValue, stemporal);
														   //soundScore->SetAttribute("value", material->ToElement()->Attribute("value"));
														   soundScore->SetAttribute("frame", frame->ToElement()->Attribute("number"));
														   foleyScore->LinkEndChild( soundScore ); // Escribimos el sonido en el frame.
														   //actorScore->LinkEndChild( frameE );
													   }
													}
												}
											}
										}
									}
								}
							}
						}
					}
			    }
		    }
		}
	}

	// Escribimos score para emocion.
	//printf("agregando emocion\n");
	TiXmlElement* emotionScore = new TiXmlElement( "emotion" );
	//elementScore->LinkEndChild( emotionScore );
	emotionScore->SetAttribute("value", emotionSound.c_str());
	
	// Salvamos.
	documentScore.SaveFile( score );	
	printf("sayonara, SBI!\n");

	// Llamamos a Blender
	//char text[182];
	//sprintf(text, "/opt/blender/blender -P SoundFilmGenerator.py -b /var/www/pyl2/VideoGenerator/empty_scene.blend >> SoundFilm.log");
	//system(text);
}

/*
Forma de ejecutar:

sudo ./MySoundFilm2 /var/www/pyl2/ImageProcessing/Execution/vocabularybbb.xml /var/www/pyl2/ImageProcessing/Execution/scriptbbb.xml /var/www/pyl2/ImageProcessing/Execution/score.xml
*/
