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

#include "SBTrainingBuilder.h"
#include "tinyxml.h"
#include "SBFileUtils.h"
#include "SBImageUtils.h"
#include "SBFilterUtils.h"

//DWM:
bool checkFileExistance(const char* filename);


bool SBTrainingBuilder::BuildTrainingShapes(vector<SBShape> &trainingShapes)
{
	TiXmlDocument doc( "vocabulary.xml" );
	bool loadOkay = doc.LoadFile();
	
	if (!loadOkay)
		std::cout << "There was a problem loading the vocabulary file ... continuing anyway" << std::endl;
	
	TiXmlNode* objectsNode = doc.FirstChild("objects");
	
	for (TiXmlNode* objectNode = objectsNode->IterateChildren("object", 0 ); objectNode; objectNode = objectsNode->IterateChildren("object", objectNode))
	{
		
		TiXmlElement *objectElement = objectNode->ToElement();
		SBShape sbShape;
		
		//Iterate the attributes of the current <object>
		for (TiXmlAttribute* attribute=objectElement->FirstAttribute(); attribute; attribute=attribute->Next())
		{
			string name = attribute->Name();
			string value = attribute->Value();
			
			if (name.compare("shape")==0)
			{
				//DWM:
				if (!checkFileExistance(value.c_str()))
				{
					std::cout << "Can't find file: " << value << std::endl;
					return false;
				}
				
				string path="", filename="";
				SBFileUtils::SplitPath(value, path, filename);
				sbShape.SetPath(path);
				sbShape.SetName(filename);
				
				ImageType::Pointer tmpImage = SBFileUtils::ReadImage(value);
				tmpImage = SBFilterUtils::RescaleImage(SBFilterUtils::InvertImage(tmpImage), 0, MAX_GRAY_VALUE);
				sbShape.SetImage(tmpImage);
				
				if (USE_ANGLE_QUANTIZATION)
					SBImageUtils::CalculateFeature(&sbShape, 16, 4);
			}
			
			if (name.compare("asset") == 0)				
				sbShape.SetAsset(value);		
			
			if (name.compare("facing") == 0)
				sbShape.SetFacing(value);

			if (name.compare("scaleOffset") == 0)
			{
				double scaleOffset = 1.0f;
				if (!value.empty())
					attribute->QueryDoubleValue(&scaleOffset);
				sbShape.SetScaleOffset(scaleOffset);
			}
		}
		
		TiXmlNode *actionsNode = objectElement->FirstChild("actions");
		
		if (actionsNode != NULL)
		{
			std::map<string, string> possibleAnimations;

			//Iterate over the <action> elements inside an <object>
			for (actionsNode = actionsNode->IterateChildren( 0 ); actionsNode; actionsNode = actionsNode->IterateChildren( actionsNode ))
			{
				TiXmlElement *actionElement=actionsNode->ToElement();
				//Iterate over the attributes of the actual <action>
				string lastText="";
				for(TiXmlAttribute* attribute=actionElement->FirstAttribute(); attribute; attribute=attribute->Next())
				{
					string name=attribute->Name();
					string value=attribute->Value();
					
					if (name.compare("text") == 0)
					{
						lastText = value;
					}
					else if (name.compare("animation") == 0)
					{
						possibleAnimations.insert(std::pair<string, string>(lastText, value));
					}	
				}
			}

			sbShape.SetPossibleAnimations(possibleAnimations);
			
		}

		trainingShapes.push_back(sbShape);
	}
	
	return true;
}
