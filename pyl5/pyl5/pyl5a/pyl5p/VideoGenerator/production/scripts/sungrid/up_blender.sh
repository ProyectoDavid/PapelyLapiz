# downloads and extracts the blender archive from the blender institutes server to the sun grid
/opt/sfw/bin/rsync -ave 'ssh -p 80'  wavemage@blender3d.dyndns.org:/home/wavemage/blender_app.tar.bz2 ~/
cd ~
rm ./bin/blender
bunzip2 blender_app.tar.bz2
tar -xpf blender_app.tar
rm blender_app.tar

