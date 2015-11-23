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

class SBFilterUtils
{
public:
	SBFilterUtils(void);
	~SBFilterUtils(void);

	static ImageType::Pointer RescaleImage(ImageType::Pointer image, int outputMin, int outputMax);

	static ImageType::Pointer InvertImage(ImageType::Pointer image);

	static int GetGlobalMean(ImageType::Pointer image);

	static ImageType::Pointer ThresholdImage(ImageType::Pointer image, int lowerThreshold, int upperThreshold, int insideValue, int outsideValue);

	static ImageType::Pointer GaussianSmoothImage(ImageType::Pointer image, float variance);

	static ImageType::Pointer ThinImage(ImageType::Pointer image);

	static ImageType::Pointer GetConnectedComponents(ImageType::Pointer image, bool fullyConnected);

	static ImageType::Pointer RegionGrowing(ImageType::Pointer image, ImageType::IndexType seed, bool fullConnectivity, int lowerThreshold, int upperThreshold, int replaceValue);

	static ImageType::Pointer Xor(ImageType::Pointer image1, ImageType::Pointer image2);

	static ImageType::Pointer MeanSmoothImage(ImageType::Pointer image, unsigned int radius);

	static ImageCalculatorFilterType::Pointer GetMaxMinGrayValue(ImageType::Pointer image);
	
	//DWM:
	static int GetOtsuThreshold(ImageType::Pointer);

	static ImageType::Pointer PerformHistogramEqualization(ImageType::Pointer);
	
	static ImageType::Pointer PerformMeanFilter(ImageType::Pointer);
};

