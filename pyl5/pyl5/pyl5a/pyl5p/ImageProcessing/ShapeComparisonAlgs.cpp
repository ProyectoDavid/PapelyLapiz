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

#include <itkHausdorffDistanceImageFilter.h>

#include <SBImageUtils.h>
#include <SBFileUtils.h>
#include <SBFilterUtils.h>
#include <ShapeComparisonAlgs.h>

double ShapeComparisonAlgs::calculateCommonBlackPixels(ImageType::Pointer& im1, ImageType::Pointer& im2)
{
	// Cantidad de figura en la imagen 1
	int cantidadTotal = 0;
	// Cantidad de figura comunes
	int cantidadIguales = 0;

	for (int i=0; i!=TEMPLATE_SIZE*TEMPLATE_SIZE; i++)
	{
		ImageType::IndexType index;
		index[0] = i/TEMPLATE_SIZE;
		index[1] = i%TEMPLATE_SIZE;
		
		// Si es BG ignore este pixel
		if (im1->GetPixel(index) == 0x0000)
			continue;
		
		cantidadTotal ++;
		
		// Si no es BG entonces hay figura en ambas imagenes
		if(im2->GetPixel(index) != 0x0000)
			cantidadIguales ++;
	}
	
	// Retorna un porcentaje
	return cantidadIguales / (double)cantidadTotal;
}


double ShapeComparisonAlgs::calculateCommonBlackAndWhitePixels(ImageType::Pointer& im1, ImageType::Pointer& im2)
{
	// Cantidad de negros y blancos
	int cantidad = 0;
	
	for (int i=0; i!=TEMPLATE_SIZE*TEMPLATE_SIZE; i++)
	{
		ImageType::IndexType index;
		index[0] = i/TEMPLATE_SIZE;
		index[1] = i%TEMPLATE_SIZE;
		
		// Si ambos son del mismo color
		if (im1->GetPixel(index) == im2->GetPixel(index))
		{
			cantidad ++;
		}
	}
	
	// Retorna un porcentaje
	return cantidad / ((double)TEMPLATE_SIZE*TEMPLATE_SIZE);
}

/*
double ShapeComparisonAlgs::calculateHausdorffDistance(ImageType::Pointer& im1, ImageType::Pointer& im2)
{
	double max_distance = 0;
	
	for (int i=0; i!=TEMPLATE_SIZE*TEMPLATE_SIZE; i++)
	{
		int xi = i/TEMPLATE_SIZE, yi = i%TEMPLATE_SIZE;
		ImageType::IndexType index_i;
		index_i[0] = xi;
		index_i[1] = yi;
		
		if (im1->GetPixel(index_i))
			continue;
		
		double min_distance = INFINITY;
		
		// Calcular la menor distancia de un pixel i a cualquier pixel j
		for (int j=0; j!=TEMPLATE_SIZE*TEMPLATE_SIZE; j++)
		{
			int xj = j/TEMPLATE_SIZE, yj = j%TEMPLATE_SIZE;
			ImageType::IndexType index_j;
			index_j[0] = xj;
			index_j[1] = yj;
			
			if (im2->GetPixel(index_j))
				continue;
			
			// Calcular la distancia
			double distance = (xi-xj)*(xi-xj) + (yi-yj)*(yi-yj);
			min_distance = MIN(min_distance, distance);
		}
		
		max_distance = MAX(max_distance, min_distance);
	}
	
	//std::cout <<  max_distance << std::endl;
	
	// max_distance es un número entre 0 y 5000, lo convierto entre 0 y 1
	max_distance = MIN(max_distance, 250); // trunco los valores
	max_distance = max_distance / 250; // normalizo los valores
	
	// Retorna un porcentaje
	return 1 - max_distance;
}


double ShapeComparisonAlgs::calculateModifiedHausdorffDistance(ImageType::Pointer& im1, ImageType::Pointer& im2)
{
	// Cantidad de pixeles negros en la imagen origen
	int num_pixels = 0;
	double avg_distance = 0;
	
	for (int i=0; i!=TEMPLATE_SIZE*TEMPLATE_SIZE; i++)
	{
		int xi = i/TEMPLATE_SIZE, yi = i%TEMPLATE_SIZE;
		ImageType::IndexType index_i;
		index_i[0] = xi;
		index_i[1] = yi;
		
		if (im1->GetPixel(index_i))
			continue;
			
		num_pixels++;
		
		double min_distance = INFINITY;
		
		// Calcular la menor distancia de un pixel i a cualquier pixel j
		for (int j=0; j!=TEMPLATE_SIZE*TEMPLATE_SIZE; j++)
		{
			int xj = j/TEMPLATE_SIZE, yj = j%TEMPLATE_SIZE;
			ImageType::IndexType index_j;
			index_j[0] = xj;
			index_j[1] = yj;
			
			if (im2->GetPixel(index_j))
				continue;
			
			// Calcular la distancia
			double distance = (xi-xj)*(xi-xj) + (yi-yj)*(yi-yj);
			min_distance = MIN(min_distance, distance);
		}
		
		avg_distance += min_distance;
	}
	
	avg_distance /= num_pixels;
	
	//std::cout << avg_distance << std::endl;
	
	// max_distance es un número entre 0 y 5000, lo convierto entre 0 y 1
	avg_distance = MIN(avg_distance, 100); // trunco los valores
	avg_distance = avg_distance / 100; // normalizo los valores
	
	// Retorna un porcentaje
	return 1 - avg_distance;
}
*/

int ShapeComparisonAlgs::GetMostSimilarTrainingShape(ImageType::Pointer& anImage, vector<SBShape>* trainingShapes, int algorithm, double* pHowCommon)
{
	uint mostCommonShape;
	double maxHowCommon = 0;
	itk::HausdorffDistanceImageFilter<ImageType, ImageType>::Pointer hausdoffFilter;
	
	if (algorithm==3 || algorithm==4)
	{
		hausdoffFilter = itk::HausdorffDistanceImageFilter<ImageType, ImageType>::New();
		hausdoffFilter->SetInput1(anImage);
	}
	
	for (uint i=0; i!=trainingShapes->size(); i++)
	{
		ImageType::Pointer aTemplateImage = (*trainingShapes)[i].GetImage();
		
		double howCommon;
		switch (algorithm)
		{
			case 1:
				howCommon = ShapeComparisonAlgs::calculateCommonBlackPixels(anImage, aTemplateImage);
				break;
			case 2:
				howCommon = ShapeComparisonAlgs::calculateCommonBlackAndWhitePixels(anImage, aTemplateImage);
				break;
			case 3:
				hausdoffFilter->SetInput2(aTemplateImage);
				hausdoffFilter->Update();
				howCommon = hausdoffFilter->GetHausdorffDistance();
				
				howCommon = howCommon > 100 ? 0 : (1 - howCommon/100);
				break;
			default:
				hausdoffFilter->SetInput2(aTemplateImage);
				hausdoffFilter->Update();
				howCommon = hausdoffFilter->GetAverageHausdorffDistance();
				
				howCommon = howCommon > 100 ? 0 : (1 - howCommon/100);
		}
		
		if (howCommon > maxHowCommon)
		{
			maxHowCommon = howCommon;
			mostCommonShape = i;
		}
	}
	
	bool dontPredict = false;
	
	// Si el algoritmo no esta muy seguro no hago ninguna prediccion
	/*switch (algorithm)
	{
		case 1:
			dontPredict = (maxHowCommon < 0.5);
			break;
		case 2:
			dontPredict = (maxHowCommon < 0.8);
			break;
		case 3:
			dontPredict = (maxHowCommon < 0.7);
			break;
		default:
			dontPredict = (maxHowCommon < 0.7);
			break;
	}*/
	
	if (dontPredict)
	{
		maxHowCommon = 1 - maxHowCommon;
		mostCommonShape = -1;
	}
	
	*pHowCommon = maxHowCommon;
	return mostCommonShape;
}

int ShapeComparisonAlgs::GetMostSimilarTrainingShape(SBShape* aShape, vector<SBShape>* trainingShapes)
{
	ImageType::Pointer anImage = aShape->GetImage();
	
	//Resize
	anImage = SBImageUtils::ResizeImage(anImage, TEMPLATE_SIZE, TEMPLATE_SIZE);
	//Again to binary
	int threshold = SBFilterUtils::GetOtsuThreshold(anImage);
	anImage = SBFilterUtils::ThresholdImage(anImage, 0, threshold, 0, MAX_GRAY_VALUE);
	anImage = SBFilterUtils::InvertImage(anImage);
	//Save evidence
	SBFileUtils::WriteImage(anImage, IMAGE_LOG "LabelsResized/" + aShape->GetName() +"-resized.png");
	
	double d1,d2,d3,d4;
	
	int b = GetMostSimilarTrainingShape(anImage, trainingShapes, 1, &d1);
	int bw = GetMostSimilarTrainingShape(anImage, trainingShapes, 2, &d2);
	int hdd = GetMostSimilarTrainingShape(anImage, trainingShapes, 3, &d3);
	int mhdd = GetMostSimilarTrainingShape(anImage, trainingShapes, 4, &d4);
	
	std::cout << b << "("<< d1;
	if (b!=-1) std::cout << (*trainingShapes)[b].GetAsset();
	std::cout <<") " << bw << "("<< d2;
	if (bw!=-1) std::cout << (*trainingShapes)[bw].GetAsset();
	std::cout <<") " << hdd << "("<< d3;
	if (hdd!=-1) std::cout << (*trainingShapes)[hdd].GetAsset();
	std::cout <<") " << mhdd << "("<< d4;
	if (mhdd!=-1) std::cout << (*trainingShapes)[mhdd].GetAsset();
	std::cout <<") "<< std::endl;
	
	if (b==-1 && bw==-1 && hdd==mhdd)
		return hdd;
	
	if (b==bw || b==hdd || b==mhdd)
		return b;
	
	if (bw==hdd || bw==mhdd)
		return bw;
	
	if (hdd==mhdd)
		return hdd;
	
	return -1;
}
