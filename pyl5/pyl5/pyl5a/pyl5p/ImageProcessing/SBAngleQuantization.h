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
#include "SBShape.h"

class SBAngleQuantization
{
	SBShape *sbShape;
	
	//Number of bins to use for the angle quantization
	int k;

	//The step for the selected points from the original points of sbShape
	int step;

	std::vector<float> bins;
	std::vector<int> feature;

	//Classifies the angle in its correspondent bin (angle range)
	void ClassifyAngleInBin(float angle);

public:
	SBAngleQuantization(void);
	~SBAngleQuantization(void);

	void SetSBShape(SBShape *pSBShape);

	void SetK(int pK);

	void SetStep(int pStep);

	//Calculates the normalized feature of the sbShape
    //void CalculateFeature();

	void CalculateAdvancedFeature();
};

