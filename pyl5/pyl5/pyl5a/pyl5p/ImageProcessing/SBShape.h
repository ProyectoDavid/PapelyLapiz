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
class SBShape
{

	//The image of this shape. It changes through the different filters
	ImageType::Pointer image;

	//The path of the image
	string path;

	//The filename of the image
	string name;

	//The original points of the 1-pixel-wide shape
	std::vector<ImageType::IndexType> points;
	
	//Normalized feature
	std::vector<float> feature;

	//The path and filename of the 3D asset
	string asset;

	//Possible animations if this is a model that also contains animations
	std::map<string, string> possibleAnimations;

	//Stores the bounding box and its center
	BoundingBoxType::Pointer boundingBox;

	//The label assigned to this connected component
	int label;

	//Number of foregound pixels that have only 1 foreground neighbor
	vector<ImageType::IndexType> endPoints;

	//Number of foregound pixels that have 3 or more foreground neighbors
	vector<ImageType::IndexType> intersectionPoints;

	//Number of paths of the stroke. A path is a sorted set of points between:
	//endPoint and endPoint
	//endPoint and intersectionPoint
	//intersectionPoint and intersectionPoint
	vector<Path> paths;

	//Where the 3d model is facing. The meanings are:
	//front=positive Z (outside the screen)
	//back=negative Z (inside the screen)
	//left=negative X
	//right=positive X
	string facing;

	//The scale offset the user wants to add to the size of the 3d model when it's rendered
	double scaleOffset;

public:

	SBShape(void);
	~SBShape(void);

	//Getters and setters

	ImageType::Pointer GetImage();

	void SetImage(ImageType::Pointer pImage);

	string GetPath();

	void SetPath(string pPath);

	string GetName();

	void SetName(string pName);

	std::vector<ImageType::IndexType> GetPoints();

	void SetPoints(std::vector<ImageType::IndexType> pPoints);

	std::vector<float> GetFeature();

	void SetFeature(std::vector<float> pFeature);

	bool PointExists(ImageType::IndexType point);

	string GetAsset();

	void SetAsset(string pAsset);

	std::map<string, string> GetPossibleAnimations();

	void SetPossibleAnimations(std::map<string, string> pPossibleAnimations);

	BoundingBoxType::Pointer GetBoundingBox();

	void SetBoundingBox(BoundingBoxType::Pointer pBoundingBox);

	int GetLabel();

	void SetLabel(int pLabel);

	vector<ImageType::IndexType> GetEndPoints();

	void SetEndPoints(vector<ImageType::IndexType> pEndPoints);

	vector<ImageType::IndexType> GetIntersectionPoints();

	void SetIntersectionPoints(vector<ImageType::IndexType> pIntersectionPoints);

	vector<Path> GetPaths();

	bool PointExistsInPaths(ImageType::IndexType point);

	bool EndPointExists(ImageType::IndexType point);

	bool IntersectionPointExists(ImageType::IndexType point);

	string GetFacing();
	void SetFacing(string pFacing);

	double GetScaleOffSet();
	void SetScaleOffset(double pScaleOffset);
	
	void SetPaths(vector<Path> pPaths);

};
