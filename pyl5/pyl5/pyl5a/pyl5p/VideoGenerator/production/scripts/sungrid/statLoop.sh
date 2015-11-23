#!/bin/bash
# send stats about what the sun grid is doing to the
# blender institute for inspection and monitoring
while [ 1 ]  ; do
	qstat -u $USER -xml > ~/qstat.log
	/opt/sfw/bin/rsync --progress -ave 'ssh -p 80'    ~/qstat.log    ~/production/jobs/*.done    wavemage@blender3d.dyndns.org:/shared/render/
	sleep 16
done