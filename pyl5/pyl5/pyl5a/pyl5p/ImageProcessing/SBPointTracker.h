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
#include "SBShape.h"



class SBPointTracker
{
	SBShape *sbShape;

	ImageType::IndexType GetInitialB(ImageType::Pointer image);
	CBPair GetNextPathPoint(ImageType::Pointer image, ImageType::IndexType c, ImageType::IndexType b);

	ImageType::IndexType GetIntersectionOrEndPointNeighbor(ImageType::IndexType fromIndex, ImageType::IndexType evaluatedIndex);
	ImageType::IndexType GetIntersectionNeighbor(ImageType::IndexType fromIndex, ImageType::IndexType evaluatedIndex);

	void TrackEndToIntersectionOrEndToEndPaths();

	void IterateClockwiseNeighbors(ImageType::IndexType index);
	void TrackIntersectionToIntersectionPath();

public:
	SBPointTracker(void);
	~SBPointTracker(void);

	void TrackPoints();

	void TrackAdvancedPoints();

	void TrackPaths();

	void SetSBShape(SBShape *pSBShape);
};




