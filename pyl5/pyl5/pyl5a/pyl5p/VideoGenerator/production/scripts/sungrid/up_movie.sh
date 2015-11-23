# Synchronises the production files on the sungrid with the files stored on the sungrid
ssh wavemage@blender3d.dyndns.org -p 80 'svn update /home/wavemage/production' 
ssh wavemage@blender3d.dyndns.org -p 80 'bash ~/production/scripts/generateJobs.sh'
/opt/sfw/bin/rsync --delete --progress --exclude .svn -avze 'ssh -p 80'  wavemage@blender3d.dyndns.org:/home/wavemage/production ~/
# find ~/production/ -exec touch {} \;
chmod +x ~/*.sh
