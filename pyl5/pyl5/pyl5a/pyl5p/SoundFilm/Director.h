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
 *  Director.h
 *  SoundFilm
 *
 *  Created by Juan Manuel Moreno on 12/05/12.
 *  Copyright 2012 __MyCompanyName__. All rights reserved.
 *
 */
#include "tinyxml.h"
#include <string>
using std::string;

class Director
{
public:
	//Director();
	Director(	const char* aVocabulary, 
				const char* aScript, 
				const char* aScore, 
				const char* aSoundsActors, 
				const char* aSoundsAnimations);
	~Director();
	void compose(void);
	
	const char* temporal;
	
private:
	const char* vocabulary;
	const char* script;
	const char* score;
	const char* soundsActors;
	const char* listSoundsActors[100]; 
	const char* soundsAnimations;
	const char* listSoundsAnimations[100];
	
};

