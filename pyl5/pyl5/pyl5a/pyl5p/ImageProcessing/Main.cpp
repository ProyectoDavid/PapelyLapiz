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

#include "SBDefinitions.h"
#include "SBFilterUtils.h"
#include "SBFileUtils.h"
#include "SBShape.h"
#include "SBFeatureComparison.h"
#include "SBFeatureExtraction.h"
#include "SBTrainingBuilder.h"
#include "SBImageUtils.h"
#include "SBWordManager.h"
#include "SBNeighborUtils.h"
#include "SBArrow.h"
#include "SBGeometryUtils.h"
#include "SBCompositionManager.h"
#include "ShapeComparisonAlgs.h"


//DWM:INI
#include <sys/stat.h>
#include <sys/types.h>
#include <dirent.h>
#include <unistd.h>
#include <string>

#define DEFAULT_INPUT_FILENAME "Test.png"
#define DEFAULT_OUTPUT_FILENAME "script.xml"
#define ARROW_HEAD_MAX_PIXELS 25


//DWM:END

#include <iostream>
#include <fstream>
#include <ctime>
#include <stdio.h>

double image_width;
double image_height;

bool LabelExists(std::vector<int> labels, int label) {

	for (uint i=0; i<labels.size(); i++)
	{
		if (labels[i]==label)
			return true;
	}
	return false;
}


std::vector<int> GetLabels(ImageType::Pointer &image)
{
	ConstIteratorType constIterator(image, image->GetLargestPossibleRegion());
	IteratorType iterator(image, image->GetLargestPossibleRegion());
	
	std::vector<int> labels;

	for (iterator.GoToBegin(), constIterator.GoToBegin(); !iterator.IsAtEnd(); ++iterator, ++constIterator) {

		if(!LabelExists(labels, constIterator.Value()))
			labels.push_back(constIterator.Value());
	}

	return labels;
}


/*
void Compare2Shapes(char *filename1, char *filename2) {	
	
	string path="", filename="";

	SBFileUtils::SplitPath(filename1, path, filename);
	//std::cout << "Path:" << path << std::endl;
	//std::cout << "Filename:" << filename << std::endl;

	SBShape sbShape1;
	sbShape1.SetImage(SBFileUtils::ReadImage(filename1));
	sbShape1.SetName(filename);

	SBFileUtils::SplitPath(filename2, path, filename);
	SBShape sbShape2;
	sbShape2.SetImage(SBFileUtils::ReadImage(filename2));
	sbShape2.SetName(filename);
	
	cout<<"Data of:"<<sbShape1.GetName()<<endl;
	
	SBFeatureExtraction sbFeatureExtraction1;
	sbFeatureExtraction1.SetSBShape(&sbShape1);
	sbFeatureExtraction1.ComputeFeature(16, 4);

	
	
	std::cout << std::endl;

	cout<<"Data of:"<<sbShape2.GetName()<<endl;
	SBFeatureExtraction sbFeatureExtraction2;
	sbFeatureExtraction1.SetSBShape(&sbShape2);
	sbFeatureExtraction1.ComputeFeature(16, 4);

	SBFeatureComparison sbFeatureComp;
	sbFeatureComp.SetFeature1(sbShape1.GetFeature());
	sbFeatureComp.SetFeature2(sbShape2.GetFeature());

	float metric = sbFeatureComp.CompareWithRotations();

	std::cout << "Metric:" << metric << std::endl;

}*/



ImageType::Pointer CreateImage(unsigned int width, unsigned int height) {

	ImageType::Pointer newImage = ImageType::New();
	ImageType::RegionType region;
	ImageType::IndexType start;
	start[0] = 0;
	start[1] = 0;
 
	ImageType::SizeType size;
	
	size[0] = width;
	size[1] = height;
 
	region.SetSize(size);
	region.SetIndex(start);
 
	newImage->SetRegions(region);
	newImage->Allocate();

	ConstIteratorType constIterator(newImage, newImage->GetLargestPossibleRegion());
	IteratorType iterator(newImage, newImage->GetLargestPossibleRegion());

	for (iterator.GoToBegin(), constIterator.GoToBegin(); !iterator.IsAtEnd(); ++iterator, ++constIterator) {
		iterator.Set(MAX_GRAY_VALUE);
	}

	return newImage;
}

void FillImage(ImageType::Pointer data, BoundingBoxType::BoundsArrayType dataBoundingBox, int offsetWidth, int offsetHeight, ImageType::Pointer &newImage, int label)
{
	ConstIteratorType constIterator(data, data->GetLargestPossibleRegion());
	IteratorType iterator(data, data->GetLargestPossibleRegion());

	int dataInitialX = dataBoundingBox[0];
	int dataInitialY = dataBoundingBox[2];

	for (iterator.GoToBegin(), constIterator.GoToBegin(); !iterator.IsAtEnd(); ++iterator, ++constIterator)
	{
		if(constIterator.Value() == label)
		{
			ImageType::IndexType dataIndex = constIterator.GetIndex();

			ImageType::IndexType newImageIndex;
			newImageIndex[0] = dataIndex[0]-dataInitialX+offsetWidth;
			newImageIndex[1] = dataIndex[1]-dataInitialY+offsetHeight;

			newImage->SetPixel(newImageIndex, 0); // 0 here means BLACK
		}
	}
	
	
}

void FillImage(ImageType::Pointer data, BoundingBoxType::BoundsArrayType dataBoundingBox, int offsetWidth, int offsetHeight, ImageType::Pointer &newImage, vector<int> labels) {

	ConstIteratorType constIterator(data, data->GetLargestPossibleRegion());
	IteratorType iterator(data, data->GetLargestPossibleRegion());

	int dataInitialX=dataBoundingBox[0];
	int dataInitialY=dataBoundingBox[2];

	//int width=newImage->GetLargestPossibleRegion().GetSize()[0];
	//int height=newImage->GetLargestPossibleRegion().GetSize()[1];
	
	for (iterator.GoToBegin(), constIterator.GoToBegin(); !iterator.IsAtEnd(); ++iterator, ++constIterator)
	{
		//if(constIterator.Value()==label) {
		if(LabelExists(labels, constIterator.Value())) {

			ImageType::IndexType dataIndex=constIterator.GetIndex();

			ImageType::IndexType newImageIndex;
			newImageIndex[0]=dataIndex[0]-dataInitialX+offsetWidth;
			newImageIndex[1]=dataIndex[1]-dataInitialY+offsetHeight;

			newImage->SetPixel(newImageIndex, 0);
		}
	}

}

bool IsBoundingBoxInside(BoundingBoxType::BoundsArrayType bBox1, BoundingBoxType::BoundsArrayType bBox2) {

	bool isXInside=bBox1[0]>bBox2[0] && bBox1[0]<bBox2[1] && bBox1[1]>bBox2[0] && bBox1[1]<bBox2[1];

	bool isYInside=bBox1[2]>bBox2[2] && bBox1[2]<bBox2[3] && bBox1[3]>bBox2[2] && bBox1[3]<bBox2[3];

	if(isXInside && isYInside)
		return true;

	return false;
}


float Compare2Features(vector<float> feature1, vector<float> feature2) {
	SBFeatureComparison sbFeatureComp;
	sbFeatureComp.SetFeature1(feature1);
	sbFeatureComp.SetFeature2(feature2);

	float metric = sbFeatureComp.CompareWithRotations();
	return metric;
}

string GetTextFromFile(string pathAndFilename){
	
	string line="", text="";
	ifstream infile;
	infile.open(pathAndFilename.c_str());//DWM:
	while(!infile.eof())
	{
		getline(infile,line);
		if(!line.empty()) {
	
			text=line;
			//cout<<"Word text before: "<<text<<endl;
			break;
		}
	}
	infile.close();
	
	return text;
}

string RemoveSpaces(string text) {
	for(uint i=0; i<text.length(); i++) {
		if(text[i]==' ') {
			text.replace(i, 1, "");
		}
	}
	return text;
}

void EraseElementFromVector(vector<SBShape> &elements, int labelToErase) {
	
	for(uint i=0; i<elements.size(); i++) {
		
		if(elements[i].GetLabel()==labelToErase) {
			elements.erase(elements.begin()+i);
			break;
		}
	}
}

Path ReversePath(Path path)
{
	Path reversedPath;

	for(int i=path.points.size()-1; i>=0; i--)
	{
		reversedPath.points.push_back(path.points[i]);
	}

	return reversedPath;
}

Path CalculateAbsolutePath(BoundingBoxType::Pointer absoluteBoundingBox, BoundingBoxType::Pointer localBoundingBox, Path localPath)
{
	BoundingBoxType::PointType absCenter=absoluteBoundingBox->GetCenter();
	BoundingBoxType::PointType localCenter=localBoundingBox->GetCenter();
	int xLocalDistanceToCenter=0, yLocalDistanceToCenter=0, absoluteX=0, absoluteY=0;
	for(uint i=0; i<localPath.points.size(); i++)
	{
		ImageType::IndexType localPoint=localPath.points[i];
		

		xLocalDistanceToCenter=localPoint[0]-localCenter[0];
		yLocalDistanceToCenter=localPoint[1]-localCenter[1];

		absoluteX=absCenter[0]+xLocalDistanceToCenter;
		absoluteY=absCenter[1]+yLocalDistanceToCenter;

		ImageType::IndexType absolutePoint;
		absolutePoint[0]=absoluteX;
		absolutePoint[1]=absoluteY;

		localPath.points[i]=absolutePoint;
	}

	return localPath;

}

void PrintInformation(SBCompositionManager *compManager)
{
	cout << endl;
	vector<SBComposition*> compositions=compManager->GetCompositions();
	for(uint i=0; i<compositions.size(); i++)
	{
		cout << endl << "Composition: " << i << endl << endl;
		
		vector<SBActor*>actors = compositions[i]->GetActors();
		
		for(uint i=0; i<actors.size(); i++)
		{
			SBActor* actor = actors[i];
			cout << "# Type: Actor" << endl;
			cout << "# Label: " << actor->GetLabel() << endl;
			cout << "# Asset: " << actor->GetAsset() << endl;
			cout << "# Image: " << actor->GetImageName() << endl;
			printf("# Bounds: (%f,%f,%f,%f)\n", actor->GetBoundingBox()->GetBounds()[0] / image_width,
				actor->GetBoundingBox()->GetBounds()[2] / image_height,
				actor->GetBoundingBox()->GetBounds()[1] / image_width,
				actor->GetBoundingBox()->GetBounds()[3] / image_height);

			cout << "# Animation: " << actor->GetAnimation() << endl;
			
			/*if(actor->GetTrajectory().GetPath().points.size()>0)
			{
				cout<<"Trajectory (Arrow) label:"<<actor->GetTrajectory().GetLabel()<<endl;
				cout<<"Trajectory start point: "<<actor->GetTrajectory().GetPath().points[0]<<endl;
			}*/

			cout << endl;
		}
	}
		
}


//DWM: INI
bool checkFileExistance(const char* filename)
{
	FILE *file = fopen(filename, "r");
	
	if (file == NULL)
	{
		std::cout << "The following file couldn't be opened: " << filename << std::endl;
		perror ("The error encountered was");
		return false;
	}
	
	fclose(file);
	return true;
}

bool ensureDirectoryExistance(const char* dirname)
{
	DIR *dir = opendir(dirname);
	
	if (dir == NULL)
	{
		perror ("Directory doesn't exist");
		std::cout << "Creating directory: " << dirname << std::endl;
		
		if (mkdir(dirname, 0755) == -1)
		{
			perror(dirname);
			return false;
		}
	}
	else {
		closedir(dir);
	}
	
	return true;
}


vector<SBShape> searchArrowsFromActors(vector<SBShape> &possibleArrows, vector<SBArrow> *arrows)
{
	std::cout << std::endl;
	std::cout << "##Etapa de busqueda de FLECHAS##" << std::endl << std::endl;
	vector<SBShape> notRecognized;
	vector<int> arrowsLabels;
	//Iterate over the possible arrows
	for (uint i=0; i<possibleArrows.size(); i++)
	{
		SBShape sbShape = possibleArrows[i];
		
		cout << "Lets see if " << sbShape.GetName() << " is an arrow...";
		
		// Si no se estaba usando Angle Quantization entonces el Feature no se ha calculado, asi que lo calculo
		if (!USE_ANGLE_QUANTIZATION)
			SBImageUtils::CalculateFeature(&sbShape, 16, 4);
		
		vector<Path> paths = sbShape.GetPaths();
		
		//When an arrow is totally thinned (1 pixel wide), it has 3 end points, 3 paths and 1 intersection point where the 
		//3 paths encounter. Of those 3 paths we are interested in analyzing the longest one because that's the one the object
		//is going to follow
		bool isAnArrow = paths.size()==3 && sbShape.GetEndPoints().size()==3 && sbShape.GetIntersectionPoints().size()==1;
		
		
		// Si parece una flecha, reviso que la punta de la cabeza este en los limites empiricos
		if (isAnArrow)
		{
			int acum = 0;
			
			if (paths[0].points.size() >= ARROW_HEAD_MAX_PIXELS)
				acum++;
			if (paths[1].points.size() >= ARROW_HEAD_MAX_PIXELS)
				acum++;
			if (paths[2].points.size() >= ARROW_HEAD_MAX_PIXELS)
				acum++;
			
			if (acum > 1)
			{
				isAnArrow = false;
				cout << sbShape.GetName() << " looked like an arrow, but its head was too big: (" <<
					paths[0].points.size() << ","<<paths[1].points.size() << "," << paths[2].points.size() << ")" << endl;
			}
		}
		
		if (!isAnArrow)
		{
			std::cout << "nope." << std::endl;
			notRecognized.push_back(sbShape);
			continue;
		}
		
		// Imprimo informacion sobre la imagen
		//{
		SBFileUtils::WriteImage(sbShape.GetImage(), IMAGE_LOG "Arrows/" + sbShape.GetName());
		
		std::cout << "yep." << std::endl;
		std::cout << "# Type: Arrow" << std::endl;
		std::cout << "# Image: " << sbShape.GetName() << std::endl;
		std::cout << "# Label: " << sbShape.GetLabel() << std::endl;
		
		printf("# Bounds: (%f,%f,%f,%f)\n", sbShape.GetBoundingBox()->GetBounds()[0] / image_width,
			   sbShape.GetBoundingBox()->GetBounds()[2] / image_height,
			   sbShape.GetBoundingBox()->GetBounds()[1] / image_width,
			   sbShape.GetBoundingBox()->GetBounds()[3] / image_height);
		
		//std::cout << std::endl;
		//}
		
		
		Path longestPath;
		uint maxPoints = 0;
		
		for (uint p=0; p<paths.size(); p++)
		{
			Path path=paths[p];
			
			ImageType::IndexType firstPoint = path.points[0], lastPoint=path.points[path.points.size()-1];
			bool arrowCase1 = sbShape.EndPointExists(firstPoint) && sbShape.IntersectionPointExists(lastPoint);
			bool arrowCase2 = sbShape.EndPointExists(lastPoint) && sbShape.IntersectionPointExists(firstPoint);
			
			if (arrowCase1 || arrowCase2)
			{
				if (path.points.size() > maxPoints)
				{
					maxPoints = path.points.size();
					longestPath = path;
				}
				
				if (arrowCase2)
					longestPath = ReversePath(longestPath);
			}
		}
		
		BoundingBoxType::Pointer localBoundingBox = SBImageUtils::GetBoundingBox(sbShape.GetImage(), MAX_GRAY_VALUE);
		BoundingBoxType::Pointer absoluteBoundingBox = sbShape.GetBoundingBox();
		
		Path absolutePath = CalculateAbsolutePath(absoluteBoundingBox, localBoundingBox, longestPath);

		SBArrow arrow;				
		arrow.SetPath(absolutePath);
		arrow.SetLabel(sbShape.GetLabel());

		arrows->push_back(arrow);
		arrowsLabels.push_back(sbShape.GetLabel());
	}
	
	for (uint j=0; j<arrowsLabels.size(); j++) {
		EraseElementFromVector(possibleArrows, arrowsLabels[j]);
	}
	std::cout << "------------------------------------------------" << std::endl;
	std::cout << "## Total FLECHAS Encontradas: " << arrowsLabels.size() << std::endl;
	return notRecognized;
}


vector<SBShape> searchArrows(vector<SBShape> possibleArrows, vector<SBArrow> *arrows)
{
	vector<SBShape> notRecognized;
	//Iterate over the possible arrows
	for (uint i=0; i<possibleArrows.size(); i++)
	{
		SBShape sbShape = possibleArrows[i];
		
		cout << "Lets see if " << sbShape.GetName() << " is an arrow" << endl;
		
		// Si no se estaba usando Angle Quantization entonces el Feature no se ha calculado, asi que lo calculo
		if (!USE_ANGLE_QUANTIZATION)
			SBImageUtils::CalculateFeature(&sbShape, 16, 4);
		
		vector<Path> paths = sbShape.GetPaths();
		
		//When an arrow is totally thinned (1 pixel wide), it has 3 end points, 3 paths and 1 intersection point where the 
		//3 paths encounter. Of those 3 paths we are interested in analyzing the longest one because that's the one the object
		//is going to follow
		bool isAnArrow = paths.size()==3 && sbShape.GetEndPoints().size()==3 && sbShape.GetIntersectionPoints().size()==1;
		
		
		// Si parece una flecha, reviso que la punta de la cabeza este en los limites empiricos
		if (isAnArrow)
		{
			int acum = 0;
			
			if (paths[0].points.size() >= ARROW_HEAD_MAX_PIXELS)
				acum++;
			if (paths[1].points.size() >= ARROW_HEAD_MAX_PIXELS)
				acum++;
			if (paths[2].points.size() >= ARROW_HEAD_MAX_PIXELS)
				acum++;
			
			if (acum > 1)
			{
				isAnArrow = false;
				cout << sbShape.GetName() << " looked like an arrow, but its head was too big: (" <<
					paths[0].points.size() << ","<<paths[1].points.size() << "," << paths[2].points.size() << ")" << endl;
			}
		}
		
		if (!isAnArrow)
		{
			notRecognized.push_back(sbShape);
			continue;
		}
		
		// Imprimo informacion sobre la imagen
		//{
		SBFileUtils::WriteImage(sbShape.GetImage(), IMAGE_LOG "Arrows/" + sbShape.GetName());
		
		std::cout << std::endl;
		std::cout << "# Type: Arrow" << std::endl;
		std::cout << "# Image: " << sbShape.GetName() << std::endl;
		std::cout << "# Label: " << sbShape.GetLabel() << std::endl;
		
		printf("# Bounds: (%f,%f,%f,%f)\n", sbShape.GetBoundingBox()->GetBounds()[0] / image_width,
			   sbShape.GetBoundingBox()->GetBounds()[2] / image_height,
			   sbShape.GetBoundingBox()->GetBounds()[1] / image_width,
			   sbShape.GetBoundingBox()->GetBounds()[3] / image_height);
		
		std::cout << std::endl;
		//}
		
		
		Path longestPath;
		uint maxPoints = 0;
		
		for (uint p=0; p<paths.size(); p++)
		{
			Path path=paths[p];
			
			ImageType::IndexType firstPoint = path.points[0], lastPoint=path.points[path.points.size()-1];
			bool arrowCase1 = sbShape.EndPointExists(firstPoint) && sbShape.IntersectionPointExists(lastPoint);
			bool arrowCase2 = sbShape.EndPointExists(lastPoint) && sbShape.IntersectionPointExists(firstPoint);
			
			if (arrowCase1 || arrowCase2)
			{
				if (path.points.size() > maxPoints)
				{
					maxPoints = path.points.size();
					longestPath = path;
				}
				
				if (arrowCase2)
					longestPath = ReversePath(longestPath);
			}
		}
		
		BoundingBoxType::Pointer localBoundingBox = SBImageUtils::GetBoundingBox(sbShape.GetImage(), MAX_GRAY_VALUE);
		BoundingBoxType::Pointer absoluteBoundingBox = sbShape.GetBoundingBox();
		
		Path absolutePath = CalculateAbsolutePath(absoluteBoundingBox, localBoundingBox, longestPath);

		SBArrow arrow;				
		arrow.SetPath(absolutePath);
		arrow.SetLabel(sbShape.GetLabel());

		arrows->push_back(arrow);
	}
	
	return notRecognized;
}


vector<SBShape> searchWords(vector<SBShape> &possibleWords, vector<SBShape> &detectedElements, ImageType::Pointer image, vector<SBWord*> *words)
{
	vector<SBShape> notRecognized;
	int fakeRectangles = 0;
	SBWordManager* sbWordMng = new SBWordManager();
	std::string rectangle = "SBRectangle";
	std::cout << std::endl;
	std::cout << "##Etapa de Busqueda de PALABRAS Dentro de los Rectangulos##" << std::endl << std::endl;
	//Iterate over the possible letters and arrows
	for (uint i=0; i<possibleWords.size(); i++)
	{
		SBShape otherElement = possibleWords[i];
		bool isInsideAnother = false;
		
		for (uint w=0; w<detectedElements.size(); w++)
		{
			SBShape detectedElement = detectedElements[w];
			
			//If the current element bound box is TOTALLY contained in any of the detected elements bounding box,
			//then it might be a letter inside a whole word or even noise
			if (IsBoundingBoxInside(otherElement.GetBoundingBox()->GetBounds(), detectedElement.GetBoundingBox()->GetBounds()))
			{
				std::cout << otherElement.GetName() << " esta dentro de " << detectedElement.GetName() << std::endl;
				std::cout << otherElement.GetLabel() << " esta dentro de " << detectedElement.GetLabel() << std::endl;
				
				if (otherElement.GetAsset()==rectangle && otherElement.GetName()!="")
				{
					string sFilename = IMAGE_LOG "Actors/" + otherElement.GetName();
					fakeRectangles=fakeRectangles+1;
					if(remove(sFilename.c_str()) == 0)
					{
						std::cout << "*Se ha removido falso rectangulo del log: " << sFilename << std::endl;
					}
					else
					{
						std::cout << "**********ADVERTENCIA, no se ha podido remover falso rectangulo del log: " << sFilename << std::endl;
					}
				}
				SBWord* word = sbWordMng->GetWord(detectedElement.GetLabel());
				if (word == NULL)
				{
					word = new SBWord();
					word->SetContainerLabel(detectedElement.GetLabel());
					word->SetBoundingBox(detectedElement.GetBoundingBox());
					sbWordMng->AddWord(word);
				}
				vector<int> letterLabels = word->GetLetterLabels();
				letterLabels.push_back(otherElement.GetLabel());
				word->SetLetterLabels(letterLabels);
				isInsideAnother = true;
				
				break;
			}
		}
		
		//If the current element is not inside in any of the detected elements then it's probably an arrow or noise
		if(!isInsideAnother) {
			notRecognized.push_back(otherElement);
		}
	}
	
	
	// Copy the words
	vector<SBWord*> wordsTmp = sbWordMng->GetWords();
	for (uint i=0; i!=wordsTmp.size(); i++){
		words->push_back(wordsTmp[i]);
	//delete sbWordMng;
	}
	
	//Iterate over the possible words
	for (uint i=0; i<words->size(); i++)
	{
		SBWord* word = (*words)[i];
		vector<int> letters = word->GetLetterLabels();
		
		//Create an image for the word
		BoundingBoxType::Pointer boundingBox = word->GetBoundingBox();
		unsigned int width = boundingBox->GetBounds()[1]-boundingBox->GetBounds()[0];
		unsigned int height = boundingBox->GetBounds()[3]-boundingBox->GetBounds()[2];
		unsigned int offsetWidth = 8;
		unsigned int offsetHeight = 8;
		ImageType::Pointer newImage = CreateImage(width+2*offsetWidth, height+2*offsetHeight);
		FillImage(image, boundingBox->GetBounds(), offsetWidth, offsetHeight, newImage, letters);
		
		word->SetImage(newImage);
		
		std::stringstream ss;
		ss << word->GetContainerLabel();
		string wordFile = "Word"+ss.str()+".tif";
		string outputFile = "Output"+ss.str();
		SBFileUtils::WriteImage(word->GetImage(), IMAGE_LOG + wordFile);
		
		//Analyze this image with Tesseract OCR to detect the letters
		string command="/usr/local/bin/tesseract " IMAGE_LOG + wordFile + " " IMAGE_LOG + outputFile + " -l eng";
		system(command.c_str());
		
		//Because Tesseract OCR writes the detected text to a .txt file we have to read it and obtain the text
		string textWithoutSpaces = RemoveSpaces(GetTextFromFile(IMAGE_LOG + outputFile + ".txt"));
		
		word->SetText(textWithoutSpaces);
		
		//If the word text is empty it's probably because it was noise inside some detected element
		//If there was detected a word, then erase its container rectangle from the detected elements
		
		if (!word->GetText().empty()) {   
		
			//EraseElementFromVector(detectedElements, word->GetContainerLabel());
			EraseElementFromVector(possibleWords, word->GetContainerLabel());
			
			for (uint j=0; j<letters.size(); j++) {
			
				//EraseElementFromVector(detectedElements, letters[j]);
				EraseElementFromVector(possibleWords, letters[j]);
			}
		}
		
		for (uint j=0; j<detectedElements.size(); j++)
		{
				std::cout << "# un detectado es: " << detectedElements[j].GetLabel() << std::endl;	
		}
		std::cout << "# Type: Text" << std::endl;
		//std::cout << "# Image: " << word.GetName() << std::endl;
		std::cout << "# Text: " << word->GetText() << std::endl;
		std::cout << "# Inside Label: " << word->GetContainerLabel() << std::endl;
	}
	std::cout << "--------------------------------------------------" << std::endl;
	std::cout << "## Total FALSOS RECTANGULOS: " << fakeRectangles << std::endl;
	std::cout << "## Total PALABRAS Encontradas: " << words->size() << std::endl << std::endl;
	
	//delete sbWordMng;
	//return notRecognized;
	return possibleWords;
}

vector<SBShape> searchRectangles(vector<SBShape> possibleActors, vector<SBShape> trainingShapes, ImageType::Pointer image, vector<SBShape> *detectedActors)
{
	vector<SBShape> notRecognized;
	std::string rectangle = "SBRectangle";
	std::cout << std::endl;
	std::cout << "##Etapa de busqueda de RECTANGULOS##" << std::endl << std::endl;
	//Iterate over every connected component
	for (uint i=0; i<possibleActors.size(); i++)
	{
		SBShape sbShape = possibleActors[i];
		if (true)
		{
			
			bool shapeSimilarToTraining = false;
			bool foundFirstSimilarShape = false;
			float minMetric;
			SBShape mostSimilarTrainingShape;
			
			if (USE_ANGLE_QUANTIZATION)
			{
				//Calculate the feature of this connected component using angle quantization
				SBImageUtils::CalculateFeature(&sbShape, 16, 4); //OJO: Calculate is a Set method
				
				//Iterate over the training images (vocabulary.xml)
				for (uint j=0; j<trainingShapes.size(); j++)
				{
					SBShape trainingShape = trainingShapes[j];
					//Compare the current connected component with all of the training images to check if it is
					//similar to any of them. If it is, we store it in the "detectedElements" vector
					float metric = Compare2Features(trainingShape.GetFeature(), sbShape.GetFeature());
					if (metric <= 0.02) //OJO
					{
						shapeSimilarToTraining = true;
						
						if (!foundFirstSimilarShape)
						{
							minMetric = metric;
							mostSimilarTrainingShape = trainingShape;
							foundFirstSimilarShape = true;
						}
						
						if(metric<minMetric)
						{
							minMetric = metric;
							mostSimilarTrainingShape = trainingShape;
						}
					}
				}
			}
			else
			{
				int iMostSimilarTrainingShape = ShapeComparisonAlgs::GetMostSimilarTrainingShape(&sbShape, &trainingShapes);
				
				if (iMostSimilarTrainingShape != -1)
				{
					mostSimilarTrainingShape = trainingShapes[iMostSimilarTrainingShape];
					if (mostSimilarTrainingShape.GetAsset()==rectangle)
					{
						shapeSimilarToTraining = true;
						
						char filename[100];
						sprintf(filename, "Label%d==%s.png", sbShape.GetLabel(), mostSimilarTrainingShape.GetAsset().c_str());
						
						std::cout << "Actor: " << filename << std::endl;
						sbShape.SetName(filename);
						
						string sFilename = filename;
						
						SBFileUtils::WriteImage(sbShape.GetImage(), IMAGE_LOG "Actors/" + sFilename);
					}
				}
			}
			
			//If the current connected component wasn't similar to any training image, then it might be a letter
			//or an arrow, or even noise. So we add it to the "otherElements" vector
			if (!shapeSimilarToTraining)
			{
				notRecognized.push_back(sbShape);
			}
			else
			{
				sbShape.SetAsset(mostSimilarTrainingShape.GetAsset());
				sbShape.SetPossibleAnimations(mostSimilarTrainingShape.GetPossibleAnimations());
				sbShape.SetFacing(mostSimilarTrainingShape.GetFacing());
				sbShape.SetScaleOffset(mostSimilarTrainingShape.GetScaleOffSet());
				detectedActors->push_back(sbShape);
				notRecognized.push_back(sbShape); //I do this so I can find "rectangles" inside "rectangles" for the next step.
			}
		}
	}
	std::cout << "----------------------------------------------------------------------------------------" << std::endl;
	std::cout << "## RECTANGULOS Encontrados: " << detectedActors->size() << std::endl;
	return notRecognized;
}

vector<SBShape> searchActors(vector<SBShape> possibleActors, vector<SBShape> ctrainingShapes, ImageType::Pointer image, vector<SBShape> *detectedActors)
{
	vector<SBShape> notRecognized;
	vector<SBShape> trainingShapes;
	std::string rectangle = "SBRectangle";
	
	//remuevo el rectangulo, probablemente minimice conflictos entre actores....
	for (uint i=0; i<ctrainingShapes.size(); i++)
	{
		if (ctrainingShapes[i].GetAsset()!=rectangle)
		{
			trainingShapes.push_back(ctrainingShapes[i]);
		}
	}
	
	std::cout << std::endl;
	std::cout << "# Etapa de busqueda de ACTORES #" << std::endl << std::endl;
	//Iterate over every connected component
	for (uint i=0; i<possibleActors.size(); i++)
	{
		SBShape sbShape = possibleActors[i];
		
		if (true)
		{
			
			bool shapeSimilarToTraining = false;
			bool foundFirstSimilarShape = false;
			float minMetric;
			SBShape mostSimilarTrainingShape;
			
			if (USE_ANGLE_QUANTIZATION)
			{
				//Calculate the feature of this connected component using angle quantization
				SBImageUtils::CalculateFeature(&sbShape, 16, 4); //OJO: Calculate is a Set method
				
				//Iterate over the training images (vocabulary.xml)
				for (uint j=0; j<trainingShapes.size(); j++)
				{
					SBShape trainingShape = trainingShapes[j];
					
					//Compare the current connected component with all of the training images to check if it is
					//similar to any of them. If it is, we store it in the "detectedElements" vector
					float metric = Compare2Features(trainingShape.GetFeature(), sbShape.GetFeature());
					if (metric <= 0.02) //OJO
					{
						shapeSimilarToTraining = true;
						
						if (!foundFirstSimilarShape)
						{
							minMetric = metric;
							mostSimilarTrainingShape = trainingShape;
							foundFirstSimilarShape = true;
						}
						
						if(metric<minMetric)
						{
							minMetric = metric;
							mostSimilarTrainingShape = trainingShape;
						}
					}
				}
			}
			else
			{
				int iMostSimilarTrainingShape = ShapeComparisonAlgs::GetMostSimilarTrainingShape(&sbShape, &trainingShapes);
				
				if (iMostSimilarTrainingShape != -1)
				{
					mostSimilarTrainingShape = trainingShapes[iMostSimilarTrainingShape];
					shapeSimilarToTraining = true;
					
					char filename[100];
					sprintf(filename, "Label%d==%s.png", sbShape.GetLabel(), mostSimilarTrainingShape.GetAsset().c_str());
					
					std::cout << "Actor: " << filename << std::endl;
					sbShape.SetName(filename);
					
					string sFilename = filename;
					
					SBFileUtils::WriteImage(sbShape.GetImage(), IMAGE_LOG "Actors/" + sFilename);
				}
			}
			
			//If the current connected component wasn't similar to any training image, then it might be a letter
			//or an arrow, or even noise. So we add it to the "otherElements" vector
			if (!shapeSimilarToTraining)
			{
				notRecognized.push_back(sbShape);
			}
			else
			{
				sbShape.SetAsset(mostSimilarTrainingShape.GetAsset());
				sbShape.SetPossibleAnimations(mostSimilarTrainingShape.GetPossibleAnimations());
				sbShape.SetFacing(mostSimilarTrainingShape.GetFacing());
				sbShape.SetScaleOffset(mostSimilarTrainingShape.GetScaleOffSet());
				detectedActors->push_back(sbShape);
			}
		}
	}
	std::cout << std::endl;
	std::cout << "----------------------------------------------------------------------------------------" << std::endl;
	std::cout << "## Numero de ACTORES Encontrados:" << detectedActors->size() << std::endl;
	
	return notRecognized;
}

vector<SBShape> searchNoise(vector<int> labels, ImageType::Pointer image, vector<SBShape> *detectedNoise)
{
	vector<SBShape> notNoise;
	
	//Iterate over every connected component
	for (uint i=0; i<labels.size(); i++)
	{
		std::cout << "# Verificando el label " << labels[i] << std::endl;
		if (labels[i] == 0)
			continue;
		
		//Calculate the bounding box of the current connected component
		BoundingBoxType::Pointer boundingBox = SBImageUtils::GetBoundingBox(image, labels[i]);
		
		// Convert the int to string
		std::stringstream ss;
		ss << labels[i];
		SBShape sbShape;
		sbShape.SetName("Label" + ss.str() + ".png");
		sbShape.SetBoundingBox(boundingBox);
		sbShape.SetLabel(labels[i]);
		
		unsigned int width = boundingBox->GetBounds()[1] - boundingBox->GetBounds()[0];
		unsigned int height = boundingBox->GetBounds()[3] - boundingBox->GetBounds()[2];
		unsigned int offsetWidth = 2;
		unsigned int offsetHeight = 2;
		
		//Create an all-white (MAX_GRAY_VALUE graylevel) new image for extracting the connected component
		//We add an offset (more space) to the bounding box
		ImageType::Pointer newImage = CreateImage(width + 2*offsetWidth, height + 2*offsetHeight);
		
		//Copy the contents of the connected component (represented by its UNIQUE label) to the new image
		FillImage(image, boundingBox->GetBounds(), offsetWidth, offsetHeight, newImage, labels[i]);
		
		sbShape.SetImage(newImage);
		
		SBFileUtils::WriteImage(newImage, LABEL_LOG + sbShape.GetName());
		
		// Images that are less than 5x5 pixels are considered noise
		if (width > NOISE_MAX_SIZE || height > NOISE_MAX_SIZE)
		{
			notNoise.push_back(sbShape);
		}
		else
		{		
			SBFileUtils::WriteImage(newImage, IMAGE_LOG "Noise/" + sbShape.GetName());
			
			std::cout << std::endl;
			std::cout << "# Type: Noise" << std::endl;
			std::cout << "# Image: " << sbShape.GetName() << std::endl;
			std::cout << "# Label: " << sbShape.GetLabel() << std::endl;
			
			printf("# Bounds: (%f,%f,%f,%f)\n", sbShape.GetBoundingBox()->GetBounds()[0] / image_width,
				   sbShape.GetBoundingBox()->GetBounds()[2] / image_height,
				   sbShape.GetBoundingBox()->GetBounds()[1] / image_width,
				   sbShape.GetBoundingBox()->GetBounds()[3] / image_height);
			
			std::cout << std::endl;
			
			detectedNoise->push_back(sbShape);
		}
	}
	
	return notNoise;
}

//DWM: END



int main(int argc, char **argv)
{
	const char *inputFilename;
	const char *outputFilename;
	const char *workingDirectory;

	vector<SBShape> trainingShapes;

	for (int i=0; i<argc; i++)
		cout << "Parameter " << i << " is: " << argv[i] << endl;
	
	std::cout << "--== STARTING PROCESS ==--" << std::endl;

	//DWM: INI
	{
		// Print current working directory
		char cwd[200];
		if (getcwd(cwd, sizeof(cwd)))
		{
			std::cout << "Current working directory is: " << cwd << std::endl;
		}
		
		if (chdir("../Execution"))
		{
			perror("Unable to change to directory ../Execution");
			return 1;
		}
		
		if (getcwd(cwd, sizeof(cwd)))
		{
			std::cout << "Now the working directory is: " << cwd << std::endl;
		}

		// Check that all the necessary files exist
		if (!checkFileExistance("vocabulary.xml"))
		{
			return 3;
		}

		try
		{
			std::cout << "Loading vocabulary file ..." << std::endl;
			if (!SBTrainingBuilder::BuildTrainingShapes(trainingShapes))
			{
				return 7;
			}
			
			std::cout << "DONE." << std::endl;
		}
		catch (itk::ExceptionObject exc)
		{
			std::cout << "Error loading vocabulary and assets" << std::endl << exc.what() << std::endl;
		}

		
		// Validate parameters passed into the program
		if (argc != 4)
		{
			std::cout << "Usage: " << std::endl;
			std::cout << "	" << argv[0] << " <Imagen>" << std::endl;

			inputFilename = DEFAULT_INPUT_FILENAME;
			outputFilename = DEFAULT_OUTPUT_FILENAME;
			workingDirectory = ".";
		}
		else
		{
			inputFilename = argv[1];
			workingDirectory = argv[2];
			outputFilename = argv[3];
		}
		
		if (chdir(workingDirectory))
		{
			perror("Unable to change to directory passed as second parameter");
			return 1;
		}

		if (getcwd(cwd, sizeof(cwd)))
		{
			std::cout << "Now the working directory is: " << cwd << std::endl;
		}
		
		
		// Check that the image exists as a file
		if (!checkFileExistance(inputFilename))
		{
			return 2;
		}
		
		
		// Check that all the necessary directories exist, if no, create them
		if (!ensureDirectoryExistance(IMAGE_LOG))
		{
			return 4;
		}
		if (!ensureDirectoryExistance(FEATURE_LOG))
		{
			return 4;
		}
		if (!ensureDirectoryExistance(LABEL_LOG))
		{
			return 4;
		}
		if (!ensureDirectoryExistance("Training"))
		{
			return 5;
		}
		if (!ensureDirectoryExistance("Training/Default"))
		{
			return 5;
		}
		if (!ensureDirectoryExistance("Log/LabelsResized"))
		{
			return 5;
		}
		if (!ensureDirectoryExistance("Log/Noise"))
		{
			return 5;
		}
		if (!ensureDirectoryExistance("Log/Actors"))
		{
			return 5;
		}
		if (!ensureDirectoryExistance("Log/NotRecognized"))
		{
			return 5;
		}
		if (!ensureDirectoryExistance("Log/Arrows"))
		{
			return 5;
		}
		
		// Erase files from previous execution
		system("rm Log/??.*.png Log/Features/* Log/Labels/* Log/LabelsResized/* Log/Noise/* Log/Actors/* Log/NotRecognized/* Log/Arrows/* 2>/dev/null");
	}
	
	//DWM: END
	
	std::cout << std::endl;
	
	try
	{
		std::clock_t start = std::clock();

		SBCompositionManager* compManager = new SBCompositionManager();
		
		//Read the composition
		std::cout << "Preprocessing image ..." << std::endl;
		ImageType::Pointer image = SBFileUtils::ReadImage(inputFilename);
		
		
		std::cout << "... scaling" << std::endl;
		image = SBFilterUtils::RescaleImage(image, 0, MAX_GRAY_VALUE);
		SBFileUtils::WriteImage(image, IMAGE_LOG "01. Rescaled.png");
		
		
		std::cout << "... filtering noise" << std::endl;
		image = SBFilterUtils::PerformMeanFilter(image);
		SBFileUtils::WriteImage(image, IMAGE_LOG "05. Smoothed.png");
		
		
		std::cout << "... inverting" << std::endl;
		image = SBFilterUtils::InvertImage(image);
		SBFileUtils::WriteImage(image, IMAGE_LOG "10. Inverted.png");
		
		
		//std::cout << "... equalizing" << std::endl;
		//image = SBFilterUtils::PerformHistogramEqualization(image);
		//SBFileUtils::WriteImage(image, IMAGE_LOG "20. Equalized.png");
		
		
		//std::cout << "... scaling" << std::endl;
		//image = SBFilterUtils::RescaleImage(image, 0, MAX_GRAY_VALUE);
		//SBFileUtils::WriteImage(image, IMAGE_LOG "30. Rescaled.png");
		
		
		//std::cout << "... thresholding" << std::endl;
		//int threshold = SBFilterUtils::GetOtsuThreshold(image);
		//image = SBFilterUtils::ThresholdImage(image, 0, threshold, 0, MAX_GRAY_VALUE);
		//SBFileUtils::WriteImage(image, IMAGE_LOG "35. Thresholded.png");
		
		
		//std::cout << "... filtering noise" << std::endl;
		//image = SBFilterUtils::PerformMeanFilter(image);
		//SBFileUtils::WriteImage(image, IMAGE_LOG "40. Smoothed.png");
		
		
		std::cout << "... thresholding" << std::endl;
		int threshold = SBFilterUtils::GetOtsuThreshold(image);
		image = SBFilterUtils::ThresholdImage(image, 0, threshold, 0, MAX_GRAY_VALUE);
		SBFileUtils::WriteImage(image, IMAGE_LOG "45. Thresholded.png");
		
		std::cout << "DONE." << std::endl;

		
		//Calculate the connected components
		std::cout << "Getting connected components ..." << std::endl;
		
		image = SBFilterUtils::GetConnectedComponents(image, true);
		
		std::cout << "DONE." << std::endl;
		
		image_width = image->GetLargestPossibleRegion().GetSize()[0];
		image_height = image->GetLargestPossibleRegion().GetSize()[1];

		vector<int> labels = GetLabels(image);
		std::cout << "LABELS QUE HE OBTENIDO: " << labels.size() << std::endl;
		vector<SBShape> notRecognized;
		
		
		// Remove noise
		//{
		vector<SBShape> iThinkItsNoise;
		notRecognized = searchNoise(labels, image, &iThinkItsNoise);
		//}
		
		
		// Detection of rectangle
		//{
		vector<SBShape> detectedRectangles;
		notRecognized = searchRectangles(notRecognized, trainingShapes, image, &detectedRectangles);
		//}
		
		// Detection of words
		//{
		vector<SBWord*> words;
		//vector<SBShape> copyOfDetectedActors = detectedRectangles; // Detect letters among actors
		//notRecognized = searchWords(copyOfDetectedActors, detectedRectangles, image, &words);
		notRecognized = searchWords(notRecognized, detectedRectangles, image, &words);
		//}
		
		// Detection of arrows
		//{
		vector<SBArrow> arrows;
		//notRecognized = searchArrows(notRecognized, &arrows);
		searchArrowsFromActors(notRecognized, &arrows);		//tengo que revisar mejor esto, puede tener inconsistencias....
		//}
		
		// Detection of actors
		//{
		vector<SBShape> detectedActors;
		notRecognized = searchActors(notRecognized, trainingShapes, image, &detectedActors);
		//}
		
		
		
		// Finally print everything that couldn't be recognized
		//{
		for (uint i=0; i!=notRecognized.size(); i++)
		{
			SBShape sbShape = notRecognized[i];
			
			SBFileUtils::WriteImage(sbShape.GetImage(), IMAGE_LOG "NotRecognized/" + sbShape.GetName());
			
			std::cout << std::endl;
			std::cout << "# Type: NotRecognized" << std::endl;
			std::cout << "# Image: " << sbShape.GetName() << std::endl;
			std::cout << "# Label: " << sbShape.GetLabel() << std::endl;
			
			printf("# Bounds: (%f,%f,%f,%f)\n", sbShape.GetBoundingBox()->GetBounds()[0] / image_width,
				   sbShape.GetBoundingBox()->GetBounds()[2] / image_height,
				   sbShape.GetBoundingBox()->GetBounds()[1] / image_width,
				   sbShape.GetBoundingBox()->GetBounds()[3] / image_height);
			
			std::cout << std::endl;
		}
		//}
		

		SBComposition* composition = new SBComposition();

		for (uint i=0; i<detectedActors.size(); i++)
		{
			SBShape detectedElement = detectedActors[i];
			SBActor* actor = new SBActor(detectedElement);
			composition->AddActor(actor);
		}

		vector<SBActor*> actors = composition->GetActors();


		//RELATIONS BETWEEN ACTORS AND WORDS
		for (uint i=0; i<words.size(); i++)
		{
			if (!words[i]->GetText().empty())
			{
				vector<ImageType::IndexType> wordPointSet=SBGeometryUtils::GetBoundBoxPointSet(words[i]->GetBoundingBox(), 4);
				SBActor* closestActor=actors[0];
				vector<ImageType::IndexType> actorPointSet=SBGeometryUtils::GetBoundBoxPointSet(closestActor->GetBoundingBox(), 4);
			
				double minDistanceToActor=SBGeometryUtils::GetMinDistanceBetween2PointSets(wordPointSet, actorPointSet);
				double distance=0;
				for (uint j=1; j<actors.size(); j++)
				{
					if (actors[j]->GetAnimation().empty())
					{
						actorPointSet=SBGeometryUtils::GetBoundBoxPointSet(actors[j]->GetBoundingBox(), 4);
						distance=SBGeometryUtils::GetMinDistanceBetween2PointSets(wordPointSet, actorPointSet);
						if (distance<minDistanceToActor)
						{
							minDistanceToActor=distance;
							closestActor=actors[j];
						}
					}
				}
				closestActor->SetAnimation(words[i]->GetText());
				std::map<string, string> animationSet=closestActor->GetAnimationSet();
				if (animationSet.size()>0) 
				{
					std::map<string, string>::const_iterator end=animationSet.end();
					for(std::map<string, string>::const_iterator it=animationSet.begin(); it!=end; ++it)
					{
						string key= it->first;
						string value=it->second;

						if(words[i]->GetText().find(key)!=string::npos || key.find(words[i]->GetText())!=string::npos)
						{
							closestActor->SetAnimation(value);
							break;
						}
					}
				}
				
			}
		}



		//RELATIONS BETWEEN ACTORS AND TRAJECTORIES
		for (uint i=0; i<arrows.size(); i++)
		{
			ImageType::IndexType startPoint = arrows[i].GetPath().points[0];
			SBActor* closestActor = actors[0];
			vector<ImageType::IndexType> actorPointSet = SBGeometryUtils::GetBoundBoxPointSet(closestActor->GetBoundingBox(), 4);
			double minDistanceToActor = SBGeometryUtils::GetMinDistanceBetweenPointAndPointSet(startPoint, actorPointSet);
			double distance = 0;

			for (uint j=1; j<actors.size(); j++)
			{
				if (actors[j]->GetTrajectory().GetPath().points.size() == 0)
				{
					actorPointSet = SBGeometryUtils::GetBoundBoxPointSet(actors[j]->GetBoundingBox(), 4);
					distance = SBGeometryUtils::GetMinDistanceBetweenPointAndPointSet(startPoint, actorPointSet);

					if (distance<minDistanceToActor)
					{
						minDistanceToActor = distance;
						closestActor = actors[j];
					}
				}
			}

			closestActor->SetTrajectory(arrows[i]);
		}


		compManager->AddComposition(composition);

		image = SBFilterUtils::RescaleImage(image, 0, MAX_GRAY_VALUE);

		SBFileUtils::WriteImage(image, IMAGE_LOG "50. CompLabelsX.png");

		//Outside the big composition loop. This loop is not done yet
		PrintInformation(compManager);
		compManager->ToXml(outputFilename, image_width, image_height);
		delete compManager;

		std::cout << "Execution time: " 
					<< ((std::clock() - start) / (double) CLOCKS_PER_SEC)
					<< " seconds.\n";
	}
	catch (itk::ExceptionObject exc)
	{
		std::cout << "Aucccchhhhhh !!!! " << std::endl
					<< exc.what() << std::endl;
	}
	
	return 0;
}

