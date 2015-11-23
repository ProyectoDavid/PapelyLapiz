export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/shared/software/exr/lib
while [ 1 ]
do
	~/blender -b -P /home/wavemage/production/scripts/generateVideosExr.py
	sleep 2600
done