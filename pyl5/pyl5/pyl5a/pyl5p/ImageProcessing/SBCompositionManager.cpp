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
#include "SBCompositionManager.h"
#include "tinyxml.h"
SBCompositionManager::SBCompositionManager(void)
{
}

SBCompositionManager::~SBCompositionManager(void)
{
	for(uint i=0; i<compositions.size(); i++)
	{
		delete compositions[i];
	}
	compositions.clear();
}

vector<SBComposition*> SBCompositionManager::GetCompositions()
{
	return compositions;
}

void SBCompositionManager::AddComposition(SBComposition* composition)
{
	compositions.push_back(composition);
}

void SBCompositionManager::ToXml(string filename, int width, int height)
{
	TiXmlDocument doc;
	TiXmlElement * compositionsElement = new TiXmlElement( "compositions" );
	doc.LinkEndChild(compositionsElement);

	for(uint c=0; c<compositions.size(); c++)
	{
		TiXmlElement * compositionElement = new TiXmlElement( "composition" );
		compositionsElement->LinkEndChild(compositionElement);
		
		vector<SBActor*> actors=compositions[c]->GetActors();
		TiXmlElement * actorsElement = new TiXmlElement( "actors" );

		compositionElement->LinkEndChild(actorsElement);

		for(uint a=0; a<actors.size(); a++)
		{
			SBActor* actor=actors[a];

			TiXmlElement * actorElement = new TiXmlElement( "actor" );
			actorElement->SetAttribute("asset", actor->GetAsset().c_str());
			if ( actor->GetAnimation().empty() )
			{
				actorElement->SetAttribute("animation", "-default-");
			}else
			{
				actorElement->SetAttribute("animation", actor->GetAnimation().c_str());
			}
			actorElement->SetAttribute("facing", actor->GetFacing().c_str());
			std::stringstream ss;
			ss<<actor->GetScaleOffSet();
			actorElement->SetAttribute("scaleOffset", ss.str().c_str());

			actorsElement->LinkEndChild(actorElement);

			TiXmlElement * positionElement = new TiXmlElement( "position" );
			positionElement->SetDoubleAttribute("x", actor->GetBoundingBox()->GetCenter()[0] / (double)width);
			positionElement->SetDoubleAttribute("z", actor->GetBoundingBox()->GetCenter()[1] / (double)height);
			actorElement->LinkEndChild(positionElement);

			vector<ImageType::IndexType> points=actor->GetTrajectory().GetPath().points;
			
			if(points.size()>0)
			{
				TiXmlElement * trajectoryElement = new TiXmlElement( "trajectory" );
				actorElement->LinkEndChild(trajectoryElement);
				
				for(uint p=0; p<points.size(); p++)
				{
					TiXmlElement * pointElement = new TiXmlElement( "point" );
					pointElement->SetDoubleAttribute("x", points[p][0] / (double)width);
					pointElement->SetDoubleAttribute("z", points[p][1] / (double)height);
					trajectoryElement->LinkEndChild(pointElement);
				}
			}


		}
	}
	
	doc.SaveFile( filename.c_str() );

}
