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

#include "SBWord.h"


SBWord::SBWord(void)
{
	text="";
}


SBWord::~SBWord(void)
{
}

ImageType::Pointer SBWord::GetImage() {
	return image;
}

void SBWord::SetImage(ImageType::Pointer pImage) {
	image=pImage;
}
	
int SBWord::GetContainerLabel() {
	return containerLabel;
}

void SBWord::SetContainerLabel(int pContainerLabel) {
	containerLabel=pContainerLabel;
}

vector<int> SBWord::GetLetterLabels() {
	return letterLabels;
}

void SBWord::SetLetterLabels(vector<int> pLetterLabels) {
	letterLabels=pLetterLabels;
}

string SBWord::GetText() {
	return text;
}

void SBWord::SetText(string pText) {
	text=pText;
}

BoundingBoxType::Pointer SBWord::GetBoundingBox() {
	return boundingBox;
}

void SBWord::SetBoundingBox(BoundingBoxType::Pointer pBoundingBox) {
	boundingBox=pBoundingBox;
}
