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

#include "SBGeometryUtils.h"


SBGeometryUtils::SBGeometryUtils(void)
{
}


SBGeometryUtils::~SBGeometryUtils(void)
{
}

double SBGeometryUtils::GetDistanceBetween2Points(ImageType::IndexType point1, ImageType::IndexType point2)
{
	itk::Point<double, 2> p1, p2;
	
	p1[0]=point1[0];
	p1[1]=point1[1];

	p2[0]=point2[0];
	p2[1]=point2[1];

	return p2.EuclideanDistanceTo(p1);
}

double SBGeometryUtils::GetMinDistanceBetweenPointAndPointSet(ImageType::IndexType point, vector<ImageType::IndexType> pointSet)
{
	double minDistance=GetDistanceBetween2Points(point, pointSet[0]);

	for(uint i=1; i<pointSet.size(); i++)
	{
		double distance=GetDistanceBetween2Points(point, pointSet[i]);
		if(distance<minDistance)
			minDistance=distance;
	}
	
	return minDistance;
}

double SBGeometryUtils::GetMinDistanceBetween2PointSets(vector<ImageType::IndexType> pointSet1, vector<ImageType::IndexType> pointSet2)
{
	double minDistance=GetMinDistanceBetweenPointAndPointSet(pointSet1[0], pointSet2);
	for(uint i=1; i<pointSet1.size(); i++)
	{
		double distance=GetMinDistanceBetweenPointAndPointSet(pointSet1[i], pointSet2);
		if(distance<minDistance)
			minDistance=distance;
	}
	
	return minDistance;
}

vector<ImageType::IndexType> SBGeometryUtils::GetBoundBoxPointSet(BoundingBoxType::Pointer boundingBox)
{
	vector<ImageType::IndexType> pointSet;

	int left=boundingBox->GetBounds()[0];
	int right=boundingBox->GetBounds()[1];
	int top=boundingBox->GetBounds()[2];
	int bottom=boundingBox->GetBounds()[3];

	for(int i=left; i<right; i++)
	{
		ImageType::IndexType index;
		index[0]=i;
		index[1]=top;
		pointSet.push_back(index);
	}

	for(int i=top; i<bottom; i++)
	{
		ImageType::IndexType index;
		index[0]=right;
		index[1]=i;
		pointSet.push_back(index);
	}

	for(int i=right; i>left; i--)
	{
		ImageType::IndexType index;
		index[0]=i;
		index[1]=bottom;
		pointSet.push_back(index);
	}

	for(int i=bottom; i>top; i--)
	{
		ImageType::IndexType index;
		index[0]=left;
		index[1]=i;
		pointSet.push_back(index);
	}

	return pointSet;
}

vector<ImageType::IndexType> SBGeometryUtils::GetBoundBoxPointSet(BoundingBoxType::Pointer boundingBox, unsigned int numberOfSegmentsPerSide)
{

	vector<ImageType::IndexType> pointSet;

	int left=boundingBox->GetBounds()[0];
	int right=boundingBox->GetBounds()[1];
	int top=boundingBox->GetBounds()[2];
	int bottom=boundingBox->GetBounds()[3];
	
	int horizontalStep=(right-left)/numberOfSegmentsPerSide;
	int verticalStep=(bottom-top)/numberOfSegmentsPerSide;

	for(int i=left; i<right; i+=horizontalStep)
	{
		ImageType::IndexType index;
		index[0]=i;
		index[1]=top;
		pointSet.push_back(index);
	}

	for(int i=top; i<bottom; i+=verticalStep)
	{
		ImageType::IndexType index;
		index[0]=right;
		index[1]=i;
		pointSet.push_back(index);
	}

	for(int i=right; i>left; i-=horizontalStep)
	{
		ImageType::IndexType index;
		index[0]=i;
		index[1]=bottom;
		pointSet.push_back(index);
	}

	for(int i=bottom; i>top; i-=verticalStep)
	{
		ImageType::IndexType index;
		index[0]=left;
		index[1]=i;
		pointSet.push_back(index);
	}

	return pointSet;
}
