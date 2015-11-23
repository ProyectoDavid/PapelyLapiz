
#!/bin/bash

# Parameters:
#   Render LQ:    True/False
#   Render_Video: True/False
#   OutputPath:   Absolute path
#   InputFile:    Absolute path for script.xml
#   LogFile:      Absolute path and filename

{
echo Parameter 1: "$1"
echo Parameter 2: "$2"
echo Parameter 3: "$3"
echo Parameter 4: "$4"
echo Parameter 5: "$5"
echo Parameter 6: "$6"
echo Parameter 7: "$7"
echo Parameter 8: "$8"

date
echo

cd $3

#RENDER_LOW_QUALITY=$1 RENDER_VIDEO=$2 SCRIPT_XML_FILENAME=$3/$5 SCORE_XML_FILENAME=$8 MODELS_PATH=$7/VideoGenerator /opt/blender/blender -P $7/VideoGenerator/VideoGenerator.py -b $7/VideoGenerator/smellingfield.blend  empty_scene
RENDER_LOW_QUALITY=$1 RENDER_VIDEO=$2 SCRIPT_XML_FILENAME=../../$3/$5 SCORE_XML_FILENAME=../../$8 MODELS_PATH=$7/VideoGenerator /opt/blender/blender -P $7/VideoGenerator/VideoGenerator.py -b $7/VideoGenerator/smellingfield.blend

echo
date

} > "$3/$6" 2>&1

