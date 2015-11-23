# This script downloads logs from the sun grid
/opt/sfw/bin/rsync --progress -ave 'ssh -p 80' _*.*  wavemage@blender3d.dyndns.org:/shared/render/
