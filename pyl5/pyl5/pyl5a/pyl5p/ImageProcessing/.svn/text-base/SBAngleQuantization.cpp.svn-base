#include "SBAngleQuantization.h"
#include <math.h>
//#define PI 3.14159265

SBAngleQuantization::SBAngleQuantization(void)
{
	sbShape=NULL;
}


SBAngleQuantization::~SBAngleQuantization(void)
{
}

void SBAngleQuantization::SetSBShape(SBShape *pSBShape) {
	sbShape=pSBShape;
}

void SBAngleQuantization::SetK(int pK) {
	k=pK;
}

void SBAngleQuantization::SetStep(int pStep) {
	step=pStep;
}

void SBAngleQuantization::ClassifyAngleInBin(float angle) {
	
	if(angle>=0.0 && angle<bins[0]) {
		feature[0]++;
	}
	else {
		for(uint i=1; i<bins.size(); i++) {
			if(angle>=bins[i-1] && angle<bins[i]) {
				feature[i]++;
				break;
			}
		}
	}
}

/*void SBAngleQuantization::CalculateFeature() {
	
	
	float binAngle=2.0*M_PI/k;
	std::vector<float> normalizedFeature;
	float binAngleAccum=binAngle;
	for(int i=0; i<k; i++) {
		
		bins.push_back(binAngleAccum);
		binAngleAccum+=binAngle;
		feature.push_back(0);
	}

	std::vector<ImageType::IndexType> points=sbShape->GetPoints();
	std::vector<ImageType::IndexType> selectedPoints;

	for(uint i=0; i<points.size(); i+=step) 
		selectedPoints.push_back(points[i]);

	//std::cout << "Number of selected points: " << selectedPoints.size() << std::endl;
	
	for(uint i=1; i<selectedPoints.size(); i++) {
		
		ImageType::IndexType finalPoint=selectedPoints[i];
		ImageType::IndexType initialPoint=selectedPoints[i-1];
		
		int deltaX=finalPoint[0]-initialPoint[0];
		int deltaY=finalPoint[1]-initialPoint[1];

		float angle=0.0;

		if(deltaX<0) {
			//Vector is going left
			if(deltaY<0) {
				//Vector is going left/up
				angle=(M_PI/2.0)+atan(abs((float)deltaX/(float)deltaY));
			}
			else
				if(deltaY>0) {
					//Vector is going left/down
					angle=M_PI+atan(abs((float)deltaY/(float)deltaX));
				}
				else {
					//Vector is going exactly to the left
					angle=M_PI;
				}
		}
		else
			if(deltaX>0) {
				//Vector is going right
				if(deltaY<0) {
					//Vector is going right/up
					angle=atan(abs((float)deltaY/(float)deltaX));
				}
				else
					if(deltaY>0) {
						//Vector is going right/down
						angle=(3.0*M_PI/2.0)+atan(abs((float)deltaX/(float)deltaY));
					}
					else {
						//Vector is going exactly to the right
						angle=0;
					}
			}
			else {
				if(deltaY<0) {
					//Vector is going exactly up
					angle=M_PI/2.0;
				}
				else
					if(deltaY>0) {
						//Vector is going exactly down
						angle=3.0*M_PI/2.0;
					}
			}

		
		ClassifyAngleInBin(angle);
	}
	
	int numberOfVectors=selectedPoints.size()-1;

	for(uint i=0; i<feature.size(); i++) {
		normalizedFeature.push_back((float)feature[i]/(float)numberOfVectors);
	}

	//return normalizedFeature;
	sbShape->SetFeature(normalizedFeature);
}*/

void SBAngleQuantization::CalculateAdvancedFeature()
{
	float binAngle = 2.0*M_PI/k;
	std::vector<float> normalizedFeature;
	float binAngleAccum = binAngle;

	for(int i=0; i<k; i++)
	{
		bins.push_back(binAngleAccum);
		binAngleAccum += binAngle;
		feature.push_back(0);
	}
	
	vector<Path> paths = sbShape->GetPaths();
	int numberOfVectors = 0;
	
	for(uint p=0; p<paths.size(); p++)
	{
		Path path=paths[p];
		std::vector<ImageType::IndexType> points=path.points;
		std::vector<ImageType::IndexType> selectedPoints;

		for(uint i=0; i<points.size(); i+=step) 
			selectedPoints.push_back(points[i]);

		for(uint i=1; i<selectedPoints.size(); i++) {
		
			ImageType::IndexType finalPoint=selectedPoints[i];
			ImageType::IndexType initialPoint=selectedPoints[i-1];
		
			int deltaX=finalPoint[0]-initialPoint[0];
			int deltaY=finalPoint[1]-initialPoint[1];

			float angle=0.0;

			if(deltaX<0) {
				//Vector is going left
				if(deltaY<0) {
					//Vector is going left/up
					angle=(M_PI/2.0)+atan(abs((float)deltaX/(float)deltaY));
				}
				else
					if(deltaY>0) {
						//Vector is going left/down
						angle=M_PI+atan(abs((float)deltaY/(float)deltaX));
					}
					else {
						//Vector is going exactly to the left
						angle=M_PI;
					}
			}
			else
				if(deltaX>0) {
					//Vector is going right
					if(deltaY<0) {
						//Vector is going right/up
						angle=atan(abs((float)deltaY/(float)deltaX));
					}
					else
						if(deltaY>0) {
							//Vector is going right/down
							angle=(3.0*M_PI/2.0)+atan(abs((float)deltaX/(float)deltaY));
						}
						else {
							//Vector is going exactly to the right
							angle=0;
						}
				}
				else {
					if(deltaY<0) {
						//Vector is going exactly up
						angle=M_PI/2.0;
					}
					else
						if(deltaY>0) {
							//Vector is going exactly down
							angle=3.0*M_PI/2.0;
						}
				}

			ClassifyAngleInBin(angle);
		}
		numberOfVectors += selectedPoints.size()-1;
	}

	for(uint i=0; i<feature.size(); i++) {
		normalizedFeature.push_back((float)feature[i]/(float)numberOfVectors);
	}

	sbShape->SetFeature(normalizedFeature);
}
