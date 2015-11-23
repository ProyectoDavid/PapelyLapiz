/*
 *  ShapeComparisonAlgs.h
 *  Thesis
 *
 *  Created by Daniel Wilches on 4/15/12.
 *  Copyright 2012 __MyCompanyName__. All rights reserved.
 *
 */

#include <SBDefinitions.h>
#include <SBShape.h>


#define HAUSDORFF_TRUNC_VAL 10 //(TEMPLATE_SIZE*TEMPLATE_SIZE/2)

#define MIN(x,y) (x<y ? x : y)
#define MAX(x,y) (x>y ? x : y)


class ShapeComparisonAlgs
{
	static double calculateCommonBlackPixels(ImageType::Pointer& im1, ImageType::Pointer& im2);
		
	static double calculateCommonBlackAndWhitePixels(ImageType::Pointer& im1, ImageType::Pointer& im2);
		
	static double calculateHausdorffDistance(ImageType::Pointer& im1, ImageType::Pointer& im2);
		
	static double calculateModifiedHausdorffDistance(ImageType::Pointer& im1, ImageType::Pointer& im2);
	
	static int GetMostSimilarTrainingShape(ImageType::Pointer& aShape, vector<SBShape>* trainingShapes, int algorithm, double*);
	
public:
	static int GetMostSimilarTrainingShape(SBShape* aShape, vector<SBShape>* trainingShapes);

};