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
#include "SBArrow.h"
#include "SBShape.h"

class SBActor
{
	string imageName;
	BoundingBoxType::Pointer boundingBox;
	string asset;
	std::map<string, string> animationSet;
	string animation;
	SBArrow trajectory;
	int label;
	string facing;
	double scaleOffset;
	
public:
	SBActor(SBShape&);

	BoundingBoxType::Pointer GetBoundingBox();
	void SetBoundingBox(BoundingBoxType::Pointer pBoundingBox);
	
	string GetAsset();
	
	string GetImageName();

	map<string, string> GetAnimationSet();

	string GetAnimation();
	void SetAnimation(string pAnimation);
	
	SBArrow GetTrajectory();
	void SetTrajectory(SBArrow);

	int GetLabel();

	string GetFacing();

	double GetScaleOffSet();
};

