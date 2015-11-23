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

#include "SBFeatureExtraction.h"
#include "SBNoiseReduction.h"
#include "SBThinning.h"
#include "SBPointTracker.h"
#include "SBAngleQuantization.h"
#include "SBFeatureComparison.h"
#include "SBFileUtils.h"
#include "SBNeighborUtils.h"
#include "SBFilterUtils.h"

SBFeatureExtraction::SBFeatureExtraction(void)
{
	sbShape = NULL;
}


SBFeatureExtraction::~SBFeatureExtraction(void)
{
}

void SBFeatureExtraction::SetSBShape(SBShape *pSBShape)
{
	sbShape = pSBShape;
}

void SBFeatureExtraction::ComputeFeature(int k, int step)
{
	ImageType::Pointer originalImage = sbShape->GetImage();
	
	SBNoiseReduction sbNoiseReduction;
	sbNoiseReduction.SetSBShape(sbShape);
	sbNoiseReduction.ReduceNoise();
	
	//SBFileUtils::WriteImage(sbShape->GetImage(), FEATURE_LOG + sbShape->GetName() + " F4. NoiseReduction.png");
	
	SBThinning sbThinning;
	sbThinning.SetSBShape(sbShape);
	sbThinning.ThinShape();

	SBFileUtils::WriteImage(sbShape->GetImage(), FEATURE_LOG + sbShape->GetName() + " F6. OnePixelThick.png");
	
	SBNeighborUtils::CalculateInterestPoints(sbShape);

	SBPointTracker sbPointTracker;
	sbPointTracker.SetSBShape(sbShape);

	if(sbShape->GetIntersectionPoints().size()>0)
	{
		sbPointTracker.TrackPaths();
	}
	else
	{
		sbPointTracker.TrackAdvancedPoints();
	}

	SBAngleQuantization sbAngleQuantization;
	sbAngleQuantization.SetSBShape(sbShape);
	sbAngleQuantization.SetK(k);
	sbAngleQuantization.SetStep(step);
	sbAngleQuantization.CalculateAdvancedFeature();
	
	sbShape->SetImage(originalImage);
}

