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
#include "itkImage.h"
#include "itkImageFileReader.h"
#include "itkImageFileWriter.h"
#include "itkRescaleIntensityImageFilter.h"
#include "itkInvertIntensityImageFilter.h"
#include "itkScalarImageToListAdaptor.h"
#include "itkMeanCalculator.h"
#include "itkBinaryThresholdImageFilter.h"
#include "itkBinaryThinningImageFilter.h"
#include "itkConnectedThresholdImageFilter.h"
#include "itkXorImageFilter.h"
#include "itkDiscreteGaussianImageFilter.h"
#include "itkCastImageFilter.h"
#include "itkConnectedComponentImageFilter.h"
#include "itkMeanImageFilter.h"
#include "itkMinimumMaximumImageCalculator.h"
#include "itkBinaryPruningImageFilter.h"
#include <itkAdaptiveHistogramEqualizationImageFilter.h>
//DWM:INI
#include <itkOtsuMultipleThresholdsCalculator.h>
#include <itkScalarImageToHistogramGenerator.h>
#include <itkRGBAPixel.h>
#include "itkPNGImageIO.h"

#include "itkIdentityTransform.h"
#include "itkResampleImageFilter.h"
#include "itkCropImageFilter.h"

//DWM:END

#include "itkPoint.h"
#include "itkPointSet.h"
#include "itkBoundingBox.h"

#define MAX_GRAY_VALUE ((1<<16)-1)

#define IMAGE_LOG "Log/"
#define FEATURE_LOG IMAGE_LOG "Features/"
#define LABEL_LOG IMAGE_LOG "Labels/"

#define USE_ANGLE_QUANTIZATION 0

#define TEMPLATE_SIZE 50
#define NOISE_MAX_SIZE 15


#if MAX_GRAY_VALUE == 255
typedef itk::Image<unsigned char, 2> ImageType;
#else
typedef itk::Image<unsigned short, 2> ImageType;
#endif

typedef itk::Image<float, 2> SignedImageType;


typedef itk::ImageFileReader<ImageType> ReaderType;	
typedef itk::ImageFileWriter<ImageType> WriterType;

typedef itk::Statistics::ScalarImageToListAdaptor<ImageType> SampleType;
typedef itk::Statistics::MeanCalculator<SampleType> MeanAlgorithmType;

typedef itk::ImageRegionConstIterator<ImageType> ConstIteratorType;
typedef itk::ImageRegionIterator<ImageType> IteratorType;

typedef itk::InvertIntensityImageFilter<ImageType> InverterType;
typedef itk::RescaleIntensityImageFilter<ImageType, ImageType> RescaleFilterType;
typedef itk::BinaryThresholdImageFilter<ImageType, ImageType> BinaryThresholdFilterType;
typedef itk::DiscreteGaussianImageFilter<ImageType, SignedImageType> GaussianFilterType;
typedef itk::CastImageFilter<SignedImageType, ImageType> CastFilterType;
typedef itk::BinaryThinningImageFilter<ImageType, ImageType> ThinningType;
typedef itk::ConnectedThresholdImageFilter<ImageType, ImageType> ConnectedFilterType;
typedef itk::XorImageFilter<ImageType, ImageType> XorFilterType;
typedef itk::ConnectedComponentImageFilter <ImageType, ImageType> ConnectedComponentImageFilterType;
typedef itk::MeanImageFilter<ImageType, ImageType > MeanFilterType;
typedef itk::MinimumMaximumImageCalculator <ImageType> ImageCalculatorFilterType;

typedef itk::PointSet< float, 2 >   PointSetType;
typedef PointSetType::PointType PointType;
typedef PointSetType::PointsContainerPointer PointsContainerPointer;
typedef itk::BoundingBox<unsigned long, 2, float> BoundingBoxType;
typedef itk::BinaryPruningImageFilter<ImageType, ImageType> BinaryPrunningFilterType;

struct CBPair {
	ImageType::IndexType c;
	ImageType::IndexType b;
};

struct Path {
	std::vector<ImageType::IndexType> points;
};

//DWM:
typedef itk::Statistics::ScalarImageToHistogramGenerator<ImageType> ScalarImageToHistogramGeneratorType;
typedef itk::OtsuMultipleThresholdsCalculator<ScalarImageToHistogramGeneratorType::HistogramType> OtsuCalculatorType;

typedef itk::IdentityTransform<double, 2> TransformType;
typedef itk::ResampleImageFilter<ImageType, ImageType> ResampleImageFilterType;

typedef itk::CropImageFilter <ImageType, ImageType> CropImageFilterType;

/*
typedef itk::RGBAPixel<unsigned char> XPixelType;
typedef itk::Image<XPixelType, 2> XImageType;
typedef itk::ImageFileReader<XImageType> XReaderType;
typedef itk::ImageFileWriter<XImageType> XWriterType;
*/


//typedef itk::RGBAPixel<unsigned char> PixelType;
