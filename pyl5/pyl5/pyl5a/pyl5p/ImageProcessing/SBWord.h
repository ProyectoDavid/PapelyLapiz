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

#pragma once
#include "SBDefinitions.h"

using namespace std;
class SBWord
{
	ImageType::Pointer image;
	int containerLabel;
	vector<int> letterLabels;
	string text;
	BoundingBoxType::Pointer boundingBox;

public:
	SBWord(void);
	~SBWord(void);

	ImageType::Pointer GetImage();
	void SetImage(ImageType::Pointer pImage);
	
	int GetContainerLabel();
	void SetContainerLabel(int pContainerLabel);

	vector<int> GetLetterLabels();
	void SetLetterLabels(vector<int> pLetterLabels);

	string GetText();
	void SetText(string pText);

	BoundingBoxType::Pointer GetBoundingBox();
	void SetBoundingBox(BoundingBoxType::Pointer pBoundingBox);

};

