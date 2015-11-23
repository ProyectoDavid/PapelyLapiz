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

#include "SBImageUtils.h"
#include "SBFeatureExtraction.h"


void SBImageUtils::CalculateFeature(SBShape *sbShape, int k, int step)
{
	SBFeatureExtraction sbFeatureExtraction;
	sbFeatureExtraction.SetSBShape(sbShape);
	sbFeatureExtraction.ComputeFeature(k, step);
}


ImageType::Pointer SBImageUtils::ResizeImage(ImageType::Pointer input, uint width, uint height)
{
	ResampleImageFilterType::Pointer resample = ResampleImageFilterType::New();
	
	ImageType::SizeType outputSize;
	outputSize.Fill(width);
	
	ImageType::SizeType inputSize = input->GetLargestPossibleRegion().GetSize();
	
	ImageType::SpacingType outputSpacing;
	outputSpacing[0] = input->GetSpacing()[0] * (static_cast<double>(inputSize[0]) / static_cast<double>(outputSize[0]));
	outputSpacing[1] = input->GetSpacing()[1] * (static_cast<double>(inputSize[1]) / static_cast<double>(outputSize[1]));
	
	//default will be white
	resample->SetDefaultPixelValue(0xFFFF);
	
	resample->SetInput(input);
	resample->SetSize(outputSize);
	resample->SetOutputSpacing(outputSpacing);
	resample->SetTransform(TransformType::New());
	resample->UpdateLargestPossibleRegion();
	
	return resample->GetOutput();
}


BoundingBoxType::Pointer SBImageUtils::GetBoundingBox(ImageType::Pointer image, int label)
{
	ConstIteratorType constIterator(image, image->GetLargestPossibleRegion());
	
	IteratorType iterator(image, image->GetLargestPossibleRegion());
	
	PointSetType::Pointer  pointSet = PointSetType::New();
	PointsContainerPointer  points = pointSet->GetPoints();
	int pointCounter=0;
	
	for (iterator.GoToBegin(), constIterator.GoToBegin(); !iterator.IsAtEnd(); ++iterator, ++constIterator) {
		
		if(constIterator.Value()==label) {
			
			ImageType::IndexType index = constIterator.GetIndex();
			PointType point;
			point[0] = index[0];
			point[1] = index[1];
			points->InsertElement(pointCounter, point);
			pointCounter++;
			
		}
	}
	
	BoundingBoxType::Pointer boundingBox = BoundingBoxType::New();
	boundingBox->SetPoints(points);
	boundingBox->ComputeBoundingBox();

	return boundingBox;
}


BoundingBoxType::Pointer SBImageUtils::GetBoundingBox(ImageType::Pointer image)
{
	ConstIteratorType constIterator(image, image->GetLargestPossibleRegion());
	
	IteratorType iterator(image, image->GetLargestPossibleRegion());
	
	PointSetType::Pointer  pointSet = PointSetType::New();
	PointsContainerPointer  points = pointSet->GetPoints();
	int pointCounter=0;
	
	for (iterator.GoToBegin(), constIterator.GoToBegin(); !iterator.IsAtEnd(); ++iterator, ++constIterator) {
		
		if(constIterator.Value() == 0)
		{
			ImageType::IndexType index = constIterator.GetIndex();
			PointType point;
			point[0] = index[0];
			point[1] = index[1];
			points->InsertElement(pointCounter, point);
			pointCounter++;
		}
	}
	
	BoundingBoxType::Pointer boundingBox = BoundingBoxType::New();
	boundingBox->SetPoints(points);
	boundingBox->ComputeBoundingBox();
	
	return boundingBox;
}

/*
ImageType::Pointer SBImageUtils::CropImage(ImageType::Pointer input)
{
	BoundingBoxType::Pointer bbox = GetBoundingBox(input);
	
	ImageType::SizeType cropSize;
	cropSize[0] = bbox->GetBounds()[0];
	cropSize[1] = bbox->GetBounds()[2];
	cropSize[2] = bbox->GetBounds()[1];
	cropSize[3] = bbox->GetBounds()[3];
	
	std:: cout << "crop(" << cropSize[0]  << ")" << std::endl;
	
	CropImageFilterType::Pointer cropFilter = CropImageFilterType::New();
	
	cropFilter->SetInput(input);
	cropFilter->SetBoundaryCropSize(cropSize);
	cropFilter->Update();
	
	return cropFilter->GetOutput();
}*/


