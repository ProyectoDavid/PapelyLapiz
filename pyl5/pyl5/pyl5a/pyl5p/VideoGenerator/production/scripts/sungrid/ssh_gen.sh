#!/bin/bash
# setup ssh trust between the sun grid and the server at the blender institute studio
ssh-keygen -t dsa
/opt/sfw/bin/rsync -ave 'ssh -p 80' ~/.ssh/id_dsa.pub  wavemage@blender3d.dyndns.org:/home/wavemage/.ssh/id_dsa_sungrid.pub
ssh wavemage@blender3d.dyndns.org -p 80 'cat ~/.ssh/id_dsa_sungrid.pub >> ~/.ssh/authorized_keys' 
 

