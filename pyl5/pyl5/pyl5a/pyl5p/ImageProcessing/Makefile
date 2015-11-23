
CC=g++

SOURCES=$(shell ls *.cpp)
OBJECTS=$(patsubst %.cpp, build/%.o, $(SOURCES))

ITK_INCLUDE_BASE=/home/dwilches/InsightToolkit-3.20.1
ITK_INCLUDE=/home/dwilches/InsightToolkit-3.20.1/Code
OPENFOAM_DIR=/home/imagine/OpenFOAM/ThirdParty/ParaView3.3-cvs

LDFLAGS=-Wno-deprecated  -ftemplate-depth-50 -Wall -Wno-deprecated -rdynamic -L$(OPENFOAM_DIR)/platforms/linux64Gcc/bin -L$(ITK_INCLUDE_BASE)/bin -lITKIO -lITKCommon -lITKBasicFilters -lITKNumerics -lITKStatistics   -lITKNrrdIO -litkgdcm -litkjpeg12 -litkjpeg16 -litkopenjpeg -luuid -litkpng -litktiff -litkjpeg8 -lITKSpatialObject -lITKMetaIO -lITKDICOMParser -lITKEXPAT -lITKniftiio -lITKznz -litkzlib -lITKCommon -lpthread -lm -litkvnl_inst -litkvnl_algo -litkvnl -litkvcl -litkv3p_lsqr -litksys -ldl -litkNetlibSlatec -litkv3p_netlib -lm -Wl,-rpath,$(OPENFOAM_DIR)/platforms/linux64Gcc/bin:$(ITK_INCLUDE_BASE)/bin:/usr/lib64/openmpi/1.2.7-gcc/lib

CFLAGS=-Wno-deprecated  -ftemplate-depth-50 -Wall -Wno-deprecated -I$(ITK_INCLUDE_BASE) -I$(ITK_INCLUDE_BASE)/Utilities/gdcm/src -I$(ITK_INCLUDE_BASE)/Utilities/gdcm -I$(ITK_INCLUDE_BASE)/Utilities/vxl/core -I$(ITK_INCLUDE_BASE)/Utilities/vxl/vcl -I$(ITK_INCLUDE_BASE)/Utilities/vxl/v3p/netlib -I$(ITK_INCLUDE)/Numerics/Statistics -I$(ITK_INCLUDE_BASE)/Utilities -I$(ITK_INCLUDE_BASE)/Utilities/itkExtHdrs -I$(ITK_INCLUDE_BASE)/Utilities/nifti/znzlib -I$(ITK_INCLUDE_BASE)/Utilities/nifti/niftilib -I$(ITK_INCLUDE_BASE)/Utilities/expat -I$(ITK_INCLUDE_BASE)/Utilities/DICOMParser -I$(ITK_INCLUDE_BASE)/Utilities/NrrdIO -I$(ITK_INCLUDE_BASE)/Utilities/MetaIO -I$(ITK_INCLUDE)/SpatialObject -I$(ITK_INCLUDE)/Numerics/NeuralNetworks -I$(ITK_INCLUDE)/Numerics/FEM -I$(ITK_INCLUDE)/IO -I$(ITK_INCLUDE)/Numerics -I$(ITK_INCLUDE)/Common -I$(ITK_INCLUDE)/BasicFilters -I$(ITK_INCLUDE)/Algorithms -I$(ITK_INCLUDE) -I$(OPENFOAM_DIR)/platforms/linux64Gcc/VTK -I$(OPENFOAM_DIR)/platforms/linux64Gcc/VTK/Common -I$(OPENFOAM_DIR)/platforms/linux64Gcc/VTK/Utilities -I$(OPENFOAM_DIR)/platforms/linux64Gcc/VTK/VolumeRendering -I$(OPENFOAM_DIR)/platforms/linux64Gcc/VTK/Rendering -I$(OPENFOAM_DIR)/VTK/Infovis -I$(OPENFOAM_DIR)/VTK/Geovis -I$(OPENFOAM_DIR)/VTK/Views -I$(OPENFOAM_DIR)/VTK/Parallel -I$(OPENFOAM_DIR)/VTK/VolumeRendering -I$(OPENFOAM_DIR)/VTK/Hybrid -I$(OPENFOAM_DIR)/VTK/Widgets -I$(OPENFOAM_DIR)/VTK/Rendering -I$(OPENFOAM_DIR)/VTK/Rendering/Testing/Cxx -I$(OPENFOAM_DIR)/VTK/IO -I$(OPENFOAM_DIR)/VTK/Imaging -I$(OPENFOAM_DIR)/VTK/Graphics -I$(OPENFOAM_DIR)/VTK/GenericFiltering -I$(OPENFOAM_DIR)/VTK/Filtering -I$(OPENFOAM_DIR)/VTK/Common -I$(OPENFOAM_DIR)/VTK/Utilities -I$(OPENFOAM_DIR)/VTK/Common/Testing/Cxx -I$(OPENFOAM_DIR)/platforms/linux64Gcc/VTK/Utilities/DICOMParser -I$(OPENFOAM_DIR)/VTK/Utilities/DICOMParser -I$(OPENFOAM_DIR)/platforms/linux64Gcc/VTK/Utilities/vtkfreetype/include -I$(OPENFOAM_DIR)/VTK/Utilities/vtkfreetype/include -I$(OPENFOAM_DIR)/platforms/linux64Gcc/VTK/Utilities/vtknetcdf -I$(OPENFOAM_DIR)/VTK/Utilities/vtknetcdf -I$(OPENFOAM_DIR)/platforms/linux64Gcc/VTK/Utilities/vtkexodus2/include -I$(OPENFOAM_DIR)/VTK/Utilities/vtkexodus2/include -I$(OPENFOAM_DIR)/platforms/linux64Gcc/VTK/Utilities/MaterialLibrary -I$(OPENFOAM_DIR)/VTK/Utilities/MaterialLibrary -I$(OPENFOAM_DIR)/platforms/linux64Gcc/VTK/Utilities/verdict -I$(OPENFOAM_DIR)/VTK/Utilities/verdict -I$(OPENFOAM_DIR)/VTK/GUISupport/Qt -I$(OPENFOAM_DIR)/platforms/linux64Gcc/VTK/GUISupport/Qt -I$(OPENFOAM_DIR)/VTK/GUISupport/Qt/Chart -I$(OPENFOAM_DIR)/platforms/linux64Gcc/VTK/GUISupport/Qt/Chart -I/usr/lib64/openmpi/1.2.7-gcc/include -I/usr/include/python2.4 -I. -I$(ITK_INCLUDE)/Review

bin/ImageProcessing: $(OBJECTS)
	@echo -ne "\033[35m"
	@echo "Por fin termino de compilar !!!! ahora a usar ld"
	@echo -ne "\033[00m"
	@$(CC) $(OBJECTS) -o bin/ImageProcessing $(LDFLAGS)

build/%.o: %.cpp
	@echo -ne "\033[35m"
	@echo Compilando $<
	@echo -ne "\033[00m"
	@$(CC) -c $< -o $@ $(CFLAGS)

clean:
	-@rm bin/Log/* bin/ImageProcessing build/*
	
