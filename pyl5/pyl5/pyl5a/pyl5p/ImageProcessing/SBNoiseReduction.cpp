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

#include "SBNoiseReduction.h"
#include "SBFilterUtils.h"
#include "SBFileUtils.h"


void SBNoiseReduction::ReduceNoise() {
	
	//string log="";
	int average = 0;
	ImageType::Pointer image = sbShape->GetImage();
	image=SBFilterUtils::RescaleImage(image, 0, MAX_GRAY_VALUE);

	SBFileUtils::WriteImage(image, FEATURE_LOG + sbShape->GetName() + " F1. Rescale.png");
	
	image = SBFilterUtils::InvertImage(image);

	SBFileUtils::WriteImage(image, FEATURE_LOG + sbShape->GetName() + " F2. Invert.png");
	average = SBFilterUtils::GetGlobalMean(image);

	image=SBFilterUtils::ThresholdImage(image, 0, 4*average, 0, MAX_GRAY_VALUE);

	SBFileUtils::WriteImage(image, FEATURE_LOG + sbShape->GetName() + " F3. FirstThreshold.png");

	//image=SBFilterUtils::GaussianSmoothImage(image, 3);
	//average = SBFilterUtils::GetGlobalMean(image);
	
	//image=SBFilterUtils::ThresholdImage(image, 0, 2*average, 0, MAX_GRAY_VALUE);
	sbShape->SetImage(image);

}


void SBNoiseReduction::SetSBShape(SBShape* pSBShape) {
	sbShape = pSBShape;
}

