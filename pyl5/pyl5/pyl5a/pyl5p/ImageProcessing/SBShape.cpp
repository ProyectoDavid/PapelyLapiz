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

#include "SBShape.h"

SBShape::SBShape(void)
{
	name="";
	asset="";
	facing="";
	scaleOffset=1.0f;
}


SBShape::~SBShape(void)
{
}

ImageType::Pointer SBShape::GetImage() {
		return this->image;
}

void SBShape::SetImage(ImageType::Pointer pImage) {
	image=pImage;
}

string SBShape::GetPath() {
	return path;
}

void SBShape::SetPath(string pPath) {
	path=pPath;
}

std::string SBShape::GetName() {
	return name;
}

void SBShape::SetName(string pName) {
	name=pName;
}

std::vector<ImageType::IndexType> SBShape::GetPoints() {
	return points;
}

void SBShape::SetPoints(std::vector<ImageType::IndexType> pPoints) {
	points=pPoints;
}

std::vector<float> SBShape::GetFeature() {
	return feature;
}

void SBShape::SetFeature(std::vector<float> pFeature) {
	feature=pFeature;
}

bool SBShape::PointExists(ImageType::IndexType point) {

	for (uint i = 0; i <points.size(); i++) {
		ImageType::IndexType index = points[i];
		if (index[0] == point[0] && index[1] == point[1])
			return true;
	}
	return false;
}

string SBShape::GetAsset() {
	return asset;
}

void SBShape::SetAsset(string pAsset) {
	asset=pAsset;
}

std::map<string, string> SBShape::GetPossibleAnimations() {
	return possibleAnimations;
}

void SBShape::SetPossibleAnimations(std::map<string, string> pPossibleAnimations) {
	possibleAnimations=pPossibleAnimations;
}

BoundingBoxType::Pointer SBShape::GetBoundingBox() {
	return boundingBox;
}

void SBShape::SetBoundingBox(BoundingBoxType::Pointer pBoundingBox) {
	boundingBox=pBoundingBox;
}

int SBShape::GetLabel() {
	return label;
}

void SBShape::SetLabel(int pLabel) {
	label=pLabel;
}

vector<ImageType::IndexType> SBShape::GetEndPoints() {
	return endPoints;
}

void SBShape::SetEndPoints(vector<ImageType::IndexType> pEndPoints) {
	endPoints=pEndPoints;
}

vector<ImageType::IndexType> SBShape::GetIntersectionPoints() {
	return intersectionPoints;
}

void SBShape::SetIntersectionPoints(vector<ImageType::IndexType> pIntersectionPoints) {
	intersectionPoints=pIntersectionPoints;
}

vector<Path> SBShape::GetPaths(){
	return paths;
}

void SBShape::SetPaths(vector<Path> pPaths) {
	paths=pPaths;
}


bool SBShape::PointExistsInPaths(ImageType::IndexType point) {
	
	for (uint p = 0; p < paths.size(); p++) {
		Path path = paths[p];
		for (uint i = 0; i < path.points.size(); i++) {
			ImageType::IndexType index = path.points[i];
			if (index[0] == point[0] && index[1] == point[1])
				return true;
		}
	}

	return false;
}

bool SBShape::EndPointExists(ImageType::IndexType point) {
	for (uint i = 0; i <endPoints.size(); i++) {
		ImageType::IndexType index = endPoints[i];
		if (index[0] == point[0] && index[1] == point[1])
			return true;
	}
	return false;
}

bool SBShape::IntersectionPointExists(ImageType::IndexType point) {
	for (uint i = 0; i <intersectionPoints.size(); i++) {
		ImageType::IndexType index = intersectionPoints[i];
		if (index[0] == point[0] && index[1] == point[1])
			return true;
	}
	return false;
}

string SBShape::GetFacing()
{
	return facing;
}

void SBShape::SetFacing(string pFacing)
{
	facing=pFacing;
}

double SBShape::GetScaleOffSet()
{
	return scaleOffset;
}
	
void SBShape::SetScaleOffset(double pScaleOffset)
{
	scaleOffset=pScaleOffset;
}
