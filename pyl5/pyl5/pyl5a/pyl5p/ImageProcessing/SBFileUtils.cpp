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

#include "SBFileUtils.h"




ImageType::Pointer SBFileUtils::ReadImage(string filename)
{
	ReaderType::Pointer reader = ReaderType::New();
	reader->SetFileName(filename);
	reader->Update();
	
	return reader->GetOutput();
}



void SBFileUtils::WriteImage(ImageType::Pointer image, std::string filename)
{
	WriterType::Pointer writer = WriterType::New();
	writer->SetFileName(filename);
	writer->SetInput(image);
	writer->Update();
}



void SBFileUtils::SplitPath(const string& pathAndFilename, string& path, string& filename) {

	string fullPath(pathAndFilename);
	replace(fullPath.begin(),fullPath.end(),'\\','/');
	string::size_type lastSlashPos=fullPath.find_last_of('/');
	
	if (lastSlashPos==std::string::npos)
	{
		path="";
		filename=fullPath;
	}
	else
	{
		path=fullPath.substr(0,lastSlashPos);
		filename=fullPath.substr(lastSlashPos+1,fullPath.size()-lastSlashPos-1);
	}
}

/*
 typedef  itk::PNGImageIO TIFFIOType;
 
 TIFFIOType::Pointer tiffIO = TIFFIOType::New();
 //tiffIO->SetPixelType(itk::ImageIOBase::RGBA);
 
 XImageType::Pointer imgdss;
 XReaderType::Pointer reader = XReaderType::New();
 reader->SetFileName(inputFilename);
 //reader->SetImageIO(tiffIO);
 reader->Update();
 imgdss = reader->GetOutput();
 
 
 XWriterType::Pointer writer = XWriterType::New();
 writer->SetFileName("Log/000.png");
 writer->SetInput(imgdss);
 
 
 
 tiffIO->SetPixelType(itk::ImageIOBase::RGB);
 writer->SetImageIO(tiffIO);
 
 writer->Update();
		*/
