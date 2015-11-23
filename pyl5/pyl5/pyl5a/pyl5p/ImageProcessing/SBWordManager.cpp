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

#include "SBWordManager.h"


SBWordManager::SBWordManager(void)
{
}


SBWordManager::~SBWordManager(void)
{
	for(uint i=0; i<words.size(); i++)
		delete words[i];
	words.clear();
	
}

SBWord* SBWordManager::GetWord(int containerLabel) {

	
	for(uint i=0; i<words.size(); i++) {
		if(words[i]->GetContainerLabel()==containerLabel)
			return words[i];
	}
	return NULL;
}

void SBWordManager::AddWord(SBWord* sbWord) {
	
	words.push_back(sbWord);
}

vector<SBWord*> SBWordManager::GetWords() {
	return words;
}
